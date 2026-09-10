from __future__ import annotations

import csv
import json
import posixpath
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "pr": PKG_REL_NS}


def _text_from_si(si: ET.Element) -> str:
    return "".join((node.text or "") for node in si.iter(f"{{{MAIN_NS}}}t"))


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in zf.namelist():
        return []
    root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    return [_text_from_si(si) for si in root.findall("m:si", NS)]


def _sheets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    wb = ET.fromstring(zf.read("xl/workbook.xml"))
    rel_root = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rels = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rel_root.findall("pr:Relationship", NS)}
    out = []
    for sheet in wb.findall("m:sheets/m:sheet", NS):
        title = sheet.attrib["name"]
        target = rels[sheet.attrib[f"{{{REL_NS}}}id"]].replace("\\", "/")
        xml_path = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
        out.append((title, xml_path))
    return out


def independently_extract(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    out: dict[tuple[str, str], dict[str, str]] = {}
    with zipfile.ZipFile(path) as zf:
        shared = _shared_strings(zf)
        for sheet, xml_path in _sheets(zf):
            root = ET.fromstring(zf.read(xml_path))
            for cell in root.findall(".//m:sheetData/m:row/m:c", NS):
                coord = cell.attrib.get("r")
                if not coord:
                    continue
                ctype = cell.attrib.get("t") or "n"
                v = cell.find("m:v", NS)
                lexical = v.text if v is not None and v.text is not None else ""
                formula_node = cell.find("m:f", NS)
                formula = formula_node.text if formula_node is not None and formula_node.text is not None else ""
                resolved = ""
                if ctype == "s" and lexical:
                    resolved = shared[int(lexical)]
                elif ctype == "inlineStr":
                    inline = cell.find("m:is", NS)
                    resolved = _text_from_si(inline) if inline is not None else ""
                elif ctype in {"str", "e", "b"}:
                    resolved = lexical
                if not lexical and not resolved and not formula:
                    continue
                key = (sheet, coord)
                if key in out:
                    raise AssertionError(f"Duplicate OOXML cell locator {key} in {path}")
                out[key] = {
                    "ooxml_type": ctype,
                    "style_index": cell.attrib.get("s", ""),
                    "value_lexical": lexical,
                    "text_resolved": resolved,
                    "formula": formula,
                }
    return out


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    build_root = Path(argv[0]) if argv else Path("_verification/live")
    manifest = json.loads((build_root / "source_manifest.json").read_text(encoding="utf-8"))
    raw_rows = read_csv(build_root / "data" / "raw_cells.csv")
    obs_rows = read_csv(build_root / "data" / "observations.csv")

    raw_by_source: dict[str, dict[tuple[str, str], dict[str, str]]] = {}
    for row in raw_rows:
        raw_by_source.setdefault(row["source_id"], {})[(row["sheet_exact"], row["cell_coordinate"])] = row

    mismatches: list[dict[str, object]] = []
    independent_counts: Counter[str] = Counter()
    independently_by_source: dict[str, dict[tuple[str, str], dict[str, str]]] = {}
    for record in manifest:
        sid = record["source_id"]
        path = Path(record["local_path"])
        independent = independently_extract(path)
        independently_by_source[sid] = independent
        independent_counts[sid] = len(independent)
        product = raw_by_source.get(sid, {})
        if set(independent) != set(product):
            missing = sorted(set(independent) - set(product))[:20]
            extra = sorted(set(product) - set(independent))[:20]
            mismatches.append({"source_id": sid, "kind": "locator_set", "missing": missing, "extra": extra})
            continue
        for locator, expected in independent.items():
            actual = product[locator]
            for field in ("ooxml_type", "style_index", "value_lexical", "text_resolved", "formula"):
                if str(actual.get(field, "")) != str(expected[field]):
                    mismatches.append({
                        "source_id": sid,
                        "kind": "field",
                        "sheet": locator[0],
                        "cell": locator[1],
                        "field": field,
                        "expected": expected[field],
                        "actual": actual.get(field, ""),
                    })
                    if len(mismatches) >= 100:
                        break
            if len(mismatches) >= 100:
                break
        if len(mismatches) >= 100:
            break

    observation_value_mismatches: list[dict[str, object]] = []
    for obs in obs_rows:
        sid = obs["source_id"]
        locator = (obs["sheet_exact"], obs["cell_coordinate"])
        independent = independently_by_source[sid][locator]
        expected_value = independent["value_lexical"] or independent["text_resolved"]
        if obs["value_exact"] != expected_value:
            observation_value_mismatches.append({
                "observation_id": obs["observation_id"],
                "source_id": sid,
                "sheet": locator[0],
                "cell": locator[1],
                "expected": expected_value,
                "actual": obs["value_exact"],
            })
            if len(observation_value_mismatches) >= 100:
                break

    if mismatches:
        raise AssertionError(f"Independent raw preservation verification failed; sample={mismatches[:3]}")
    if observation_value_mismatches:
        raise AssertionError(f"Observation value/source lexical mismatch; sample={observation_value_mismatches[:3]}")

    report = {
        "status": "passed",
        "source_count": len(manifest),
        "independently_extracted_raw_cell_count": sum(independent_counts.values()),
        "product_raw_cell_count": len(raw_rows),
        "observation_count_checked_against_independent_ooxml": len(obs_rows),
        "raw_locator_coverage": 1.0,
        "raw_field_equality": 1.0,
        "observation_source_value_equality": 1.0,
        "per_source_raw_counts": dict(sorted(independent_counts.items())),
    }
    report_path = build_root.parent / "independent-preservation-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
