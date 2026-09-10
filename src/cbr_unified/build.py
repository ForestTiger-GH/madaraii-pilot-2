from __future__ import annotations

import json
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


def build_database(
    output_dir: str | Path,
    *,
    input_dir: str | Path | None = None,
    explicit_paths: Mapping[str, str | Path] | None = None,
    sources: Sequence[SourceSpec] = SOURCES,
    require_complete: bool = True,
) -> BuildResult:
    """Build the unified database from the complete registry universe.

    If ``input_dir`` is omitted, source workbooks are downloaded from the reviewed
    registry URLs. If it is supplied, exactly one local workbook must resolve for
    each requested source. Bound inputs are copied into ``output_dir/sources`` so a
    successful build is replayable from its own immutable-by-hash source set.
    """
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    source_dir = root / "sources"
    data_dir = root / "data"
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
    manifest_path = root / "source_manifest.json"
    save_manifest(manifest, manifest_path)

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
        observations, source_concepts, source_members, dispositions, diag = parse_source_checked(
            path,
            spec=spec,
            source_revision_id=revision,
            file_sha256=sha,
            raw_cells=raw_cells,
        )
        all_raw.extend(raw_cells)
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
    finished = datetime.now(timezone.utc).isoformat()
    build_meta = {
        "status": "passed",
        "started_at_utc": started,
        "finished_at_utc": finished,
        "acquisition_mode": acquisition_mode,
        "requested_source_count": len(sources),
        "require_complete": require_complete,
        "source_manifest": str(manifest_path),
        "validation": validation,
        "source_diagnostics": diagnostics,
    }
    (root / "build.json").write_text(json.dumps(build_meta, ensure_ascii=False, indent=2), encoding="utf-8")

    paths = persist_bundle(
        data_dir,
        manifest=manifest,
        raw_cells=all_raw,
        concepts=concept_rows,
        dimension_members=member_rows,
        observations=all_observations,
        dispositions=all_dispositions,
        diagnostics=diagnostics,
        validation=validation,
    )
    return BuildResult(
        output_dir=root,
        sqlite_path=Path(paths["sqlite"]),
        validation_path=Path(paths["validation"]),
        manifest_path=manifest_path,
        source_count=len(manifest),
        raw_cell_count=len(all_raw),
        observation_count=len(all_observations),
    )
