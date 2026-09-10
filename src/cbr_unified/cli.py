from __future__ import annotations

import argparse
import json
from pathlib import Path

from .build import build_database
from .query import UnifiedDatabase


def _dims(values: list[str] | None) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in values or []:
        if "=" not in item:
            raise SystemExit(f"Invalid --dim {item!r}; expected key=value")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise SystemExit("Dimension key cannot be empty")
        out[key] = value.strip()
    return out


def _add_observation_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--source", action="append", dest="sources", help="source_id; repeatable")
    p.add_argument("--concept", action="append", dest="concepts", help="source_concept_id; repeatable")
    p.add_argument("--start", help="minimum ISO period anchor YYYY-MM-DD")
    p.add_argument("--end", help="maximum ISO period anchor YYYY-MM-DD")
    p.add_argument("--frequency", action="append", help="frequency; repeatable")
    p.add_argument("--period-role", action="append", help="stock/flow/published_change/source_defined")
    p.add_argument("--dim", action="append", help="dimension filter key=value; repeatable")
    p.add_argument("--language", choices=("ru", "en"), default="ru")


def _observation_kwargs(args: argparse.Namespace) -> dict[str, object]:
    return {
        "source_ids": args.sources,
        "concept_ids": args.concepts,
        "start": args.start,
        "end": args.end,
        "frequency": args.frequency,
        "period_role": args.period_role,
        "dimensions": _dims(args.dim),
        "language": args.language,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cbr-unified", description="Build and query the registry-defined Bank of Russia unified statistics database")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("build", help="download/bind all sources and build CSV + SQLite outputs")
    p.add_argument("--output", required=True, help="output directory")
    p.add_argument("--input-dir", help="local source directory for offline/replay build")

    p = sub.add_parser("validate", help="show embedded validation result from a built database")
    p.add_argument("--db", required=True)

    p = sub.add_parser("sources", help="list source revisions")
    p.add_argument("--db", required=True)
    p.add_argument("--csv", help="optional output CSV")

    p = sub.add_parser("indicators", help="list/search source concepts")
    p.add_argument("--db", required=True)
    p.add_argument("--text")
    p.add_argument("--language", choices=("ru", "en"), default="ru")
    p.add_argument("--source", action="append", dest="sources")
    p.add_argument("--csv")

    p = sub.add_parser("query", help="filter semantic observations")
    p.add_argument("--db", required=True)
    _add_observation_filters(p)
    p.add_argument("--csv")
    p.add_argument("--limit", type=int, default=50)

    p = sub.add_parser("pivot", help="build a fail-closed pivot from selected observations")
    p.add_argument("--db", required=True)
    _add_observation_filters(p)
    p.add_argument("--index", action="append", default=None, help="pivot index column; repeatable")
    p.add_argument("--columns", action="append", default=None, help="pivot column; repeatable")
    p.add_argument("--csv")

    p = sub.add_parser("lineage", help="show exact source lineage for one observation")
    p.add_argument("--db", required=True)
    p.add_argument("observation_id")
    return parser


def _emit_frame(df, csv_path: str | None, limit: int | None = None) -> None:
    if csv_path:
        Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=True if getattr(df.index, "nlevels", 1) > 1 or df.index.name else False, encoding="utf-8-sig")
        print(csv_path)
        return
    if limit is not None:
        df = df.head(limit)
    print(df.to_string(index=False) if not df.empty else "<empty>")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "build":
        result = build_database(args.output, input_dir=args.input_dir)
        print(json.dumps({
            "status": "passed",
            "build_id": result.build_id,
            "output_dir": str(result.output_dir),
            "sqlite": str(result.sqlite_path),
            "source_count": result.source_count,
            "raw_cell_count": result.raw_cell_count,
            "observation_count": result.observation_count,
        }, ensure_ascii=False, indent=2))
        return 0

    db = UnifiedDatabase(args.db)
    if args.command == "validate":
        print(json.dumps(db.validation(), ensure_ascii=False, indent=2))
    elif args.command == "sources":
        _emit_frame(db.sources(), args.csv)
    elif args.command == "indicators":
        _emit_frame(db.indicators(args.text, language=args.language, source_ids=args.sources), args.csv)
    elif args.command == "query":
        _emit_frame(db.observations(**_observation_kwargs(args)), args.csv, args.limit)
    elif args.command == "pivot":
        frame = db.pivot(
            index=args.index or "period",
            columns=args.columns or "indicator",
            **_observation_kwargs(args),
        )
        if args.csv:
            frame.to_csv(args.csv, encoding="utf-8-sig")
            print(args.csv)
        else:
            print(frame.to_string())
    elif args.command == "lineage":
        print(json.dumps(db.lineage(args.observation_id), ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
