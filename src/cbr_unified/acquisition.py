from __future__ import annotations

import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence
from urllib.parse import urlparse

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
        "User-Agent": "CBR-Unified-Statistics/0.2 (+https://github.com/ForestTiger-GH/madaraii-pilot-2)"
    })
    return session


def _revision_id(source_id: str, sha256: str) -> str:
    return f"{source_id}@sha256:{sha256}"


def _trusted_cbr_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    return host == "cbr.ru" or host.endswith(".cbr.ru")


def _validate_ooxml_workbook(path: str | Path) -> None:
    workbook = Path(path)
    if not zipfile.is_zipfile(workbook):
        raise AcquisitionError(f"{workbook}: file is not a ZIP/OOXML package")
    try:
        with zipfile.ZipFile(workbook) as archive:
            names = set(archive.namelist())
            required = {
                "[Content_Types].xml",
                "xl/workbook.xml",
                "xl/_rels/workbook.xml.rels",
            }
            missing = sorted(required - names)
            worksheets = [name for name in names if name.startswith("xl/worksheets/") and name.endswith(".xml")]
            if missing or not worksheets:
                raise AcquisitionError(
                    f"{workbook}: incomplete OOXML workbook; missing={missing} worksheets={len(worksheets)}"
                )
            bad_member = archive.testzip()
            if bad_member:
                raise AcquisitionError(f"{workbook}: corrupt OOXML member {bad_member}")
    except zipfile.BadZipFile as exc:
        raise AcquisitionError(f"{workbook}: invalid OOXML ZIP package") from exc


def _failure_summary(failures: Sequence[Mapping[str, object]]) -> str:
    parts: list[str] = []
    for record in failures:
        source_id = str(record.get("source_id", "?"))
        error_type = str(record.get("error_type", "Error"))
        error = str(record.get("error", "unknown failure"))
        http_status = record.get("http_status")
        resolved_url = str(record.get("resolved_url", ""))
        suffix = ""
        if http_status not in (None, ""):
            suffix += f"; http={http_status}"
        if resolved_url:
            suffix += f"; resolved={resolved_url}"
        parts.append(f"{source_id}[{error_type}]: {error}{suffix}")
    return " | ".join(parts)


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
            if not _trusted_cbr_url(spec.url):
                raise AcquisitionError(f"{spec.source_id}: registry URL is outside the CBR domain")
            response = session.get(spec.url, timeout=timeout, allow_redirects=True)
            record.update({
                "http_status": response.status_code,
                "resolved_url": response.url,
                "etag": response.headers.get("ETag", ""),
                "last_modified": response.headers.get("Last-Modified", ""),
                "content_type": response.headers.get("Content-Type", ""),
            })
            response.raise_for_status()
            if not _trusted_cbr_url(response.url):
                raise AcquisitionError(
                    f"{spec.source_id}: resolved URL left the CBR trust domain: {response.url}"
                )
            content = response.content
            target = dest / f"{spec.source_id}.xlsx"
            target.write_bytes(content)
            _validate_ooxml_workbook(target)
            sha = workbook_sha256(target)
            record.update({
                "status": "ok",
                "local_path": str(target),
                "bytes": len(content),
                "sha256": sha,
                "source_revision_id": _revision_id(spec.source_id, sha),
                "acquired_at_utc": datetime.now(timezone.utc).isoformat(),
                "trust_status": "cbr_domain_ooxml_validated",
            })
        except Exception as exc:
            record.update({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)})
        manifest.append(record)

    failures = [record for record in manifest if record["status"] != "ok"]
    if failures and require_complete:
        raise AcquisitionError(
            f"Failed to acquire {len(failures)}/{len(manifest)} sources: {_failure_summary(failures)}"
        )
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
        existing: list[Path] = []
        seen: set[str] = set()
        for path in candidates:
            key = str(path.resolve()) if path.exists() else str(path)
            if key not in seen and path.exists() and path.is_file():
                existing.append(path)
                seen.add(key)
        if len(existing) != 1:
            manifest.append({
                "source_id": spec.source_id,
                "requested_url": spec.url,
                "registry_filename": spec.filename,
                "status": "failed",
                "error_type": "LocalBindingError",
                "error": f"Expected exactly one local binding; found {len(existing)}: {[str(path) for path in existing]}",
            })
            continue

        try:
            source_path = existing[0]
            target = source_path
            if copy_root is not None:
                target = copy_root / f"{spec.source_id}.xlsx"
                if source_path.resolve() != target.resolve():
                    shutil.copy2(source_path, target)
            _validate_ooxml_workbook(target)
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
                "trust_status": "local_ooxml_validated",
            })
        except Exception as exc:
            manifest.append({
                "source_id": spec.source_id,
                "requested_url": spec.url,
                "registry_filename": spec.filename,
                "status": "failed",
                "error_type": type(exc).__name__,
                "error": str(exc),
            })

    failures = [record for record in manifest if record["status"] != "ok"]
    if failures and require_complete:
        raise AcquisitionError(
            f"Failed to bind {len(failures)}/{len(manifest)} local sources: {_failure_summary(failures)}"
        )
    return manifest


def save_manifest(records: list[dict[str, object]], path: str | Path) -> None:
    Path(path).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def load_manifest(path: str | Path) -> list[dict[str, object]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_manifest(records: list[dict[str, object]], *, require_complete: bool = True) -> None:
    by_id = {str(record["source_id"]): record for record in records}
    if len(by_id) != len(records):
        raise AcquisitionError("Duplicate source_id in manifest")
    expected = {source.source_id for source in SOURCES}
    present = set(by_id)
    if require_complete and present != expected:
        raise AcquisitionError(f"Manifest source set mismatch; missing={sorted(expected-present)} extra={sorted(present-expected)}")
    for source_id, record in by_id.items():
        get_source(source_id)
        if record.get("status") != "ok":
            raise AcquisitionError(f"Source {source_id} is not successfully bound")
        path = Path(str(record["local_path"]))
        if not path.exists():
            raise AcquisitionError(f"Source file missing for {source_id}: {path}")
        _validate_ooxml_workbook(path)
        actual = workbook_sha256(path)
        if actual != record.get("sha256"):
            raise AcquisitionError(f"Hash mismatch for {source_id}: manifest={record.get('sha256')} actual={actual}")
