from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .raw import workbook_sha256
from .registry import SOURCES, SourceSpec, get_source


class AcquisitionError(RuntimeError):
    pass


def _session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=4,
        connect=4,
        read=4,
        status=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset({"GET", "HEAD"}),
        respect_retry_after_header=True,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.headers.update({
        "User-Agent": "CBR-Unified-Statistics/0.1 (+https://github.com/ForestTiger-GH/madaraii-pilot-2)"
    })
    return session


def _revision_id(source_id: str, sha256: str) -> str:
    return f"{source_id}@sha256:{sha256}"


def download_sources(
    destination: str | Path,
    *,
    sources: Sequence[SourceSpec] = SOURCES,
    timeout: tuple[int, int] = (20, 180),
    require_complete: bool = True,
) -> list[dict[str, object]]:
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=True)
    session = _session()
    manifest: list[dict[str, object]] = []

    for spec in sources:
        record: dict[str, object] = {
            "source_id": spec.source_id,
            "requested_url": spec.url,
            "registry_filename": spec.filename,
            "status": "pending",
        }
        try:
            response = session.get(spec.url, timeout=timeout, allow_redirects=True)
            record.update({
                "http_status": response.status_code,
                "resolved_url": response.url,
                "etag": response.headers.get("ETag", ""),
                "last_modified": response.headers.get("Last-Modified", ""),
                "content_type": response.headers.get("Content-Type", ""),
            })
            response.raise_for_status()
            content = response.content
            if content[:2] != b"PK":
                raise AcquisitionError(f"{spec.source_id}: downloaded content is not XLSX/OOXML")
            target = dest / f"{spec.source_id}.xlsx"
            target.write_bytes(content)
            sha = workbook_sha256(target)
            record.update({
                "status": "ok",
                "local_path": str(target),
                "bytes": len(content),
                "sha256": sha,
                "source_revision_id": _revision_id(spec.source_id, sha),
                "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
            })
        except Exception as exc:
            record.update({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)})
        manifest.append(record)

    failures = [r for r in manifest if r["status"] != "ok"]
    if failures and require_complete:
        ids = ", ".join(str(r["source_id"]) for r in failures)
        raise AcquisitionError(f"Failed to acquire {len(failures)}/{len(manifest)} sources: {ids}")
    return manifest


def bind_local_sources(
    input_dir: str | Path,
    *,
    sources: Sequence[SourceSpec] = SOURCES,
    explicit_paths: Mapping[str, str | Path] | None = None,
    copy_to: str | Path | None = None,
    require_complete: bool = True,
) -> list[dict[str, object]]:
    root = Path(input_dir)
    explicit_paths = explicit_paths or {}
    copy_root = Path(copy_to) if copy_to is not None else None
    if copy_root:
        copy_root.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, object]] = []
    for spec in sources:
        candidates: list[Path] = []
        if spec.source_id in explicit_paths:
            candidates.append(Path(explicit_paths[spec.source_id]))
        candidates.extend([root / f"{spec.source_id}.xlsx", root / spec.filename])
        existing = []
        seen = set()
        for p in candidates:
            key = str(p.resolve()) if p.exists() else str(p)
            if key not in seen and p.exists() and p.is_file():
                existing.append(p)
                seen.add(key)
        if len(existing) != 1:
            manifest.append({
                "source_id": spec.source_id,
                "requested_url": spec.url,
                "registry_filename": spec.filename,
                "status": "failed",
                "error_type": "LocalBindingError",
                "error": f"Expected exactly one local binding; found {len(existing)}: {[str(x) for x in existing]}",
            })
            continue
        source_path = existing[0]
        target = source_path
        if copy_root is not None:
            target = copy_root / f"{spec.source_id}.xlsx"
            if source_path.resolve() != target.resolve():
                shutil.copy2(source_path, target)
        sha = workbook_sha256(target)
        manifest.append({
            "source_id": spec.source_id,
            "requested_url": spec.url,
            "resolved_url": "local",
            "registry_filename": spec.filename,
            "status": "ok",
            "local_path": str(target),
            "bytes": target.stat().st_size,
            "sha256": sha,
            "source_revision_id": _revision_id(spec.source_id, sha),
            "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
        })

    failures = [r for r in manifest if r["status"] != "ok"]
    if failures and require_complete:
        ids = ", ".join(str(r["source_id"]) for r in failures)
        raise AcquisitionError(f"Failed to bind {len(failures)}/{len(manifest)} local sources: {ids}")
    return manifest


def save_manifest(records: list[dict[str, object]], path: str | Path) -> None:
    Path(path).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def load_manifest(path: str | Path) -> list[dict[str, object]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest(records: list[dict[str, object]], *, require_complete: bool = True) -> None:
    by_id = {str(r["source_id"]): r for r in records}
    if len(by_id) != len(records):
        raise AcquisitionError("Duplicate source_id in manifest")
    expected = {s.source_id for s in SOURCES}
    present = set(by_id)
    if require_complete and present != expected:
        raise AcquisitionError(f"Manifest source set mismatch; missing={sorted(expected-present)} extra={sorted(present-expected)}")
    for sid, record in by_id.items():
        get_source(sid)
        if record.get("status") != "ok":
            raise AcquisitionError(f"Source {sid} is not successfully bound")
        path = Path(str(record["local_path"]))
        if not path.exists():
            raise AcquisitionError(f"Source file missing for {sid}: {path}")
        actual = workbook_sha256(path)
        if actual != record.get("sha256"):
            raise AcquisitionError(f"Hash mismatch for {sid}: manifest={record.get('sha256')} actual={actual}")
