from __future__ import annotations

import csv
import json
import shutil
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Sequence

from .acquisition import bind_local_sources, download_sources, save_manifest, validate_manifest
from .persistence import persist_bundle
from .processing import parse_source_checked
from .raw import extract_raw_cells
from .registry import SOURCES, SourceSpec, get_source
from .validation import validate_bundle


@dataclass(frozen=True)
class BuildResult:
    output_dir: Path
    sqlite_path: Path
    validation_path: Path
    manifest_path: Path
    source_count: int
    raw_cell_count: int
    observation_count: int


def _merge_unique(
    target: dict[str, dict[str, object]],
    rows: Sequence[Mapping[str, object]],
    *,
    key: str,
    label: str,
) -> None:
    for row in rows:
        identity = str(row[key])
        materialized = dict(row)
        existing = target.get(identity)
        if existing is not None and existing != materialized:
            raise RuntimeError(f"Conflicting {label} identity {identity}")
        target[identity] = materialized


def _write_failure_raw(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = (
        "raw_cell_id",
        "source_id",
        "source_revision_id",
        "file_sha256",
        "sheet_exact",
        "cell_coordinate",
        "ooxml_type",
        "style_index",
        "value_lexical",
        "text_resolved",
        "formula",
    )
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def _rebase_manifest_paths(
    manifest: list[dict[str, object]],
    *,
    final_root: Path,
) -> list[dict[str, object]]:
    rebased: list[dict[str, object]] = []
    for record in manifest:
        row = dict(record)
        if row.get("status") == "ok":
            row["local_path"] = str(final_root / "sources" / f"{row['source_id']}.xlsx")
        rebased.append(row)
    return rebased


def _promote(staging: Path, final_root: Path) -> None:
    backup = final_root.with_name(f".{final_root.name}.previous-{uuid.uuid4().hex[:10]}")
    had_previous = final_root.exists()
    if had_previous:
        final_root.rename(backup)
    try:
        staging.rename(final_root)
    except Exception:
        if had_previous and backup.exists() and not final_root.exists():
            backup.rename(final_root)
        raise
    else:
        if backup.exists():
            shutil.rmtree(backup)


def _build_into_staging(
    staging: Path,
    final_root: Path,
    *,
    input_dir: str | Path | None,
    explicit_paths: Mapping[str, str | Path] | None,
    sources: Sequence[SourceSpec],
    require_complete: bool,
) -> BuildResult:
    source_dir = staging / "sources"
    data_dir = staging / "data"
    source_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    started = datetime.now(timezone.utc).isoformat()
    if input_dir is None:
        manifest = download_sources(source_dir, sources=sources, require_complete=require_complete)
        acquisition_mode = "download"
    else:
        manifest = bind_local_sources(
            input_dir,
            sources=sources,
            explicit_paths=explicit_paths,
            copy_to=source_dir,
            require_complete=require_complete,
        )
        acquisition_mode = "local_binding"
    validate_manifest(manifest, require_complete=require_complete and len(sources) == len(SOURCES))
    # Save the acquisition-state manifest early. If semantic work fails, the
    # retained staging directory still contains exact acquired files and lineage.
    save_manifest(manifest, staging / "source_manifest.acquisition.json")

    all_raw: list[dict[str, object]] = []
    all_observations: list[dict[str, object]] = []
    all_dispositions: list[dict[str, str]] = []
    concepts: dict[str, dict[str, object]] = {}
    members: dict[str, dict[str, object]] = {}
    diagnostics: list[dict[str, object]] = []

    for record in manifest:
        if record.get("status") != "ok":
            if require_complete:
                raise RuntimeError(f"Source {record.get('source_id')} was not bound")
            continue
        sid = str(record["source_id"])
        spec = get_source(sid)
        path = Path(str(record["local_path"]))
        revision = str(record["source_revision_id"])
        sha = str(record["sha256"])
        raw_cells = extract_raw_cells(
            path,
            source_id=sid,
            source_revision_id=revision,
            file_sha256=sha,
        )
        all_raw.extend(raw_cells)
        try:
            observations, source_concepts, source_members, dispositions, diag = parse_source_checked(
                path,
                spec=spec,
                source_revision_id=revision,
                file_sha256=sha,
                raw_cells=raw_cells,
            )
        except Exception as exc:
            _write_failure_raw(staging / "failure-evidence" / f"{sid}-raw.csv", raw_cells)
            failure = {
                "status": "failed",
                "source_id": sid,
                "source_revision_id": revision,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "raw_evidence": str(staging / "failure-evidence" / f"{sid}-raw.csv"),
                "failed_at_utc": datetime.now(timezone.utc).isoformat(),
            }
            (staging / "failure.json").write_text(json.dumps(failure, ensure_ascii=False, indent=2), encoding="utf-8")
            raise
        all_observations.extend(observations)
        all_dispositions.extend(dispositions)
        _merge_unique(concepts, source_concepts, key="source_concept_id", label="source concept")
        _merge_unique(members, source_members, key="dimension_member_id", label="dimension member")
        diagnostics.append(diag)

    concept_rows = list(concepts.values())
    member_rows = list(members.values())
    validation = validate_bundle(
        manifest=manifest,
        raw_cells=all_raw,
        concepts=concept_rows,
        dimension_members=member_rows,
        observations=all_observations,
        dispositions=all_dispositions,
        diagnostics=diagnostics,
        require_complete=require_complete and len(sources) == len(SOURCES),
    )

    # Persist final-path locators only after all source processing and validation
    # have passed. Promotion makes those paths true atomically with the product.
    final_manifest = _rebase_manifest_paths(manifest, final_root=final_root)
    manifest_path = staging / "source_manifest.json"
    save_manifest(final_manifest, manifest_path)
    finished = datetime.now(timezone.utc).isoformat()
    build_meta = {
        "status": "passed",
        "started_at_utc": started,
        "finished_at_utc": finished,
        "acquisition_mode": acquisition_mode,
        "requested_source_count": len(sources),
        "require_complete": require_complete,
        "source_manifest": str(final_root / "source_manifest.json"),
        "validation": validation,
        "source_diagnostics": diagnostics,
    }
    (staging / "build.json").write_text(json.dumps(build_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    paths = persist_bundle(
        data_dir,
        manifest=final_manifest,
        raw_cells=all_raw,
        concepts=concept_rows,
        dimension_members=member_rows,
        observations=all_observations,
        dispositions=all_dispositions,
        diagnostics=diagnostics,
        validation=validation,
    )
    return BuildResult(
        output_dir=final_root,
        sqlite_path=final_root / "data" / Path(paths["sqlite"]).name,
        validation_path=final_root / "data" / Path(paths["validation"]).name,
        manifest_path=final_root / "source_manifest.json",
        source_count=len(manifest),
        raw_cell_count=len(all_raw),
        observation_count=len(all_observations),
    )


def build_database(
    output_dir: str | Path,
    *,
    input_dir: str | Path | None = None,
    explicit_paths: Mapping[str, str | Path] | None = None,
    sources: Sequence[SourceSpec] = SOURCES,
    require_complete: bool = True,
) -> BuildResult:
    """Build, validate and atomically promote one unified database candidate.

    A sibling staging directory is used for every attempt. Existing successful
    output is replaced only after full validation and persistence succeed. On a
    failed attempt the staging directory is retained with acquired source files,
    the acquisition manifest and source-local raw failure evidence where available.
    """
    final_root = Path(output_dir)
    final_root.parent.mkdir(parents=True, exist_ok=True)
    staging = final_root.with_name(f".{final_root.name}.staging-{uuid.uuid4().hex[:10]}")
    staging.mkdir(parents=True, exist_ok=False)
    try:
        result = _build_into_staging(
            staging,
            final_root,
            input_dir=input_dir,
            explicit_paths=explicit_paths,
            sources=sources,
            require_complete=require_complete,
        )
    except Exception as exc:
        failure_path = staging / "failure.json"
        if not failure_path.exists():
            failure_path.write_text(
                json.dumps(
                    {
                        "status": "failed",
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                        "staging_dir": str(staging),
                        "failed_at_utc": datetime.now(timezone.utc).isoformat(),
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        raise RuntimeError(f"Build failed; evidence retained in {staging}: {exc}") from exc
    _promote(staging, final_root)
    return result
