from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

PROBE = Path("_mw/research/evidence/source-probe")
OUT = Path("_mw/research/evidence/research-pack")


def cell_key(c: dict) -> tuple[int, int]:
    return int(c.get("row", 0)), int(c.get("column", 0))


def compact(value: str, limit: int = 220) -> str:
    s = " ".join(str(value).replace("\n", " ").replace("\r", " ").split())
    return s if len(s) <= limit else s[: limit - 1] + "…"


def load_sources() -> list[dict]:
    sources = []
    for path in sorted(PROBE.glob("*.json")):
        if path.name == "MANIFEST.json":
            continue
        sources.append(json.loads(path.read_text(encoding="utf-8")))
    return sources


def header_and_axis_cells(sheet: dict) -> list[dict]:
    cells = sorted(sheet.get("text_cells", []), key=cell_key)
    # Preserve the most informative framing surfaces: title/header rows and label axes.
    selected = [c for c in cells if c.get("row", 99999) <= 15 or c.get("column", 99999) <= 5]
    if len(selected) <= 500:
        return selected
    # Keep all top rows, then a deterministic spread down the left axis.
    top = [c for c in selected if c.get("row", 99999) <= 15]
    left = [c for c in selected if c.get("row", 99999) > 15]
    budget = max(0, 500 - len(top))
    if budget and len(left) > budget:
        step = len(left) / budget
        left = [left[min(int(i * step), len(left) - 1)] for i in range(budget)]
    return (top + left)[:500]


def source_section(src: dict) -> str:
    s = src["source"]
    acq = src.get("acquisition", {})
    lines = [
        f"## `{s['source_id']}` — {s['registry_label']}",
        "",
        f"- Registry family hint: `{s['family_hint']}`",
        f"- Workbook SHA-256: `{acq.get('sha256','')}`",
        f"- Sheets: {len(src.get('sheets', []))}",
        "",
    ]
    for sh in src.get("sheets", []):
        counts = sh.get("cell_type_counts", {})
        b = sh.get("actual_nonempty_bounds", {})
        lines += [
            f"### Sheet `{sh['title']}`",
            "",
            f"Bounds `{b.get('min_row')}:{b.get('max_row')} × {b.get('min_column')}:{b.get('max_column')}`; "
            f"non-empty {sh.get('nonempty_cells',0)}; text {counts.get('text',0)}; numeric {counts.get('numeric',0)}; "
            f"date {counts.get('date',0)}; formula {counts.get('formula',0)}; merged {len(sh.get('merged_ranges',[]))}.",
            "",
        ]
        nfs = sh.get("number_formats_top", [])[:8]
        if nfs:
            lines.append("Number-format signals: " + "; ".join(f"`{compact(fmt,60)}`×{count}" for fmt, count in nfs) + ".")
            lines.append("")
        axes = header_and_axis_cells(sh)
        if axes:
            lines += ["Header/axis text evidence (exact source text):", ""]
            for c in axes:
                lines.append(f"- `{c['coordinate']}` — {compact(c['value'])}")
            lines.append("")
        dates = sh.get("date_examples", [])[:20]
        if dates:
            lines += ["Date anchors:", ""]
            for d in dates:
                lines.append(f"- `{d['coordinate']}` — `{d['value']}` (`{compact(d.get('number_format',''),70)}`)")
            lines.append("")
        nums = sh.get("numeric_examples", [])[:20]
        if nums:
            lines += ["Numeric anchors:", ""]
            for n in nums:
                lines.append(f"- `{n['coordinate']}` — `{n['value']}` (`{compact(n.get('number_format',''),70)}`)")
            lines.append("")
        formulas = sh.get("formula_cells", [])[:15]
        if formulas:
            lines += ["Formula anchors:", ""]
            for f in formulas:
                lines.append(f"- `{f['coordinate']}` — `{compact(f['formula'],160)}`")
            lines.append("")
    return "\n".join(lines)


def structural_signature(src: dict) -> str:
    parts = []
    for sh in src.get("sheets", []):
        b = sh.get("actual_nonempty_bounds", {})
        c = sh.get("cell_type_counts", {})
        parts.append(
            f"{sh.get('title_presentation_signature')}:{b.get('max_row')}x{b.get('max_column')}:"
            f"t{c.get('text',0)}:n{c.get('numeric',0)}:d{c.get('date',0)}:f{c.get('formula',0)}"
        )
    return "|".join(parts)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    by_family: dict[str, list[dict]] = defaultdict(list)
    for src in sources:
        by_family[src["source"]["family_hint"]].append(src)

    index_lines = [
        "# RT-CBR-001 human-readable research pack",
        "",
        "Derived from the complete mechanical probe. This surface preserves exact source labels for research navigation; it does not declare semantic equivalence.",
        "",
    ]
    for family, items in sorted(by_family.items()):
        filename = f"FAMILY-{family}.md"
        body = [f"# Source family evidence — `{family}`", ""]
        for src in items:
            body.append(source_section(src))
        (OUT / filename).write_text("\n".join(body) + "\n", encoding="utf-8")
        index_lines.append(f"- `{filename}` — {len(items)} source workbooks")

    # Cross-source presentation-normalization collision candidates.
    label_groups: dict[str, dict[str, set[tuple[str, str, str]]]] = defaultdict(lambda: defaultdict(set))
    sheet_groups: dict[str, set[tuple[str, str]]] = defaultdict(set)
    with (PROBE / "LABEL_INDEX.csv").open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            sig = row.get("presentation_signature", "")
            exact = row.get("value", "")
            if sig and exact:
                label_groups[sig][exact].add((row.get("source_id", ""), row.get("sheet", ""), row.get("coordinate", "")))
    with (PROBE / "SHEET_INDEX.csv").open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            sig = row.get("sheet_signature", "")
            if sig:
                sheet_groups[sig].add((row.get("source_id", ""), row.get("sheet", "")))

    collision_lines = [
        "# Presentation-normalization collision candidates",
        "",
        "Groups below share a punctuation/spacing-insensitive signature. They are discovery candidates only; equality of signatures does not establish semantic identity.",
        "",
        "## Sheet-title variants",
        "",
    ]
    for sig, refs in sorted(sheet_groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        exacts = sorted({sheet for _, sheet in refs})
        if len(exacts) > 1:
            collision_lines.append(f"- `{sig}` → " + " | ".join(f"`{x}`" for x in exacts))

    candidates = []
    for sig, exact_map in label_groups.items():
        if len(exact_map) > 1:
            refs_count = sum(len(v) for v in exact_map.values())
            candidates.append((refs_count, sig, exact_map))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    collision_lines += ["", "## Cell-label variants", ""]
    for refs_count, sig, exact_map in candidates[:1500]:
        exacts = sorted(exact_map)
        collision_lines.append(f"### `{sig}` — {refs_count} occurrences / {len(exacts)} exact forms")
        collision_lines.append("")
        for exact in exacts[:30]:
            examples = sorted(exact_map[exact])[:4]
            where = ", ".join(f"`{a}/{b}!{c}`" for a, b, c in examples)
            collision_lines.append(f"- {compact(exact,260)} — {where}")
        collision_lines.append("")
    (OUT / "PRESENTATION-COLLISIONS.md").write_text("\n".join(collision_lines) + "\n", encoding="utf-8")

    clusters: dict[str, list[str]] = defaultdict(list)
    for src in sources:
        clusters[structural_signature(src)].append(src["source"]["source_id"])
    cluster_lines = [
        "# Exact structural-signature clusters",
        "",
        "These clusters use sheet signatures, bounds and cell-type counts. They indicate structurally identical workbooks, not semantic identity.",
        "",
    ]
    for sig, ids in sorted(clusters.items(), key=lambda kv: (-len(kv[1]), kv[1])):
        if len(ids) > 1:
            cluster_lines.append(f"- **{len(ids)} sources:** " + ", ".join(f"`{x}`" for x in ids))
            cluster_lines.append(f"  - signature: `{sig}`")
    (OUT / "STRUCTURAL-CLUSTERS.md").write_text("\n".join(cluster_lines) + "\n", encoding="utf-8")

    index_lines += [
        "- `PRESENTATION-COLLISIONS.md` — exact-form variants sharing conservative presentation signatures.",
        "- `STRUCTURAL-CLUSTERS.md` — exact geometry/type clusters for adapter research.",
        "",
        f"Total source workbooks: **{len(sources)}**.",
    ]
    (OUT / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
