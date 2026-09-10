from __future__ import annotations

import hashlib
import posixpath
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"m": MAIN_NS, "r": REL_NS, "pr": PKG_REL_NS}


def _text_from_si(si: ET.Element) -> str:
    parts: list[str] = []
    for node in si.iter(f"{{{MAIN_NS}}}t"):
        parts.append(node.text or "")
    return "".join(parts)


def _shared_strings(zf: zipfile.ZipFile) -> list[str]:
    name = "xl/sharedStrings.xml"
    if name not in zf.namelist():
        return []
    root = ET.fromstring(zf.read(name))
    return [_text_from_si(si) for si in root.findall("m:si", NS)]


def _sheet_targets(zf: zipfile.ZipFile) -> list[tuple[str, str]]:
    workbook = ET.fromstring(zf.read("xl/workbook.xml"))
    rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    rel_map = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("pr:Relationship", NS)
    }
    out: list[tuple[str, str]] = []
    for sheet in workbook.findall("m:sheets/m:sheet", NS):
        title = sheet.attrib["name"]
        rid = sheet.attrib[f"{{{REL_NS}}}id"]
        target = rel_map[rid].replace("\\", "/")
        if target.startswith("/"):
            xml_path = target.lstrip("/")
        else:
            xml_path = posixpath.normpath(posixpath.join("xl", target))
        out.append((title, xml_path))
    return out


def _cell_resolved_value(cell: ET.Element, shared: list[str]) -> tuple[str | None, str | None, str | None]:
    """Return raw <v>, resolved text if applicable, and formula text."""
    cell_type = cell.attrib.get("t")
    v = cell.find("m:v", NS)
    raw_v = v.text if v is not None else None
    f = cell.find("m:f", NS)
    formula = f.text if f is not None else None
    resolved: str | None = None

    if cell_type == "s" and raw_v is not None:
        try:
            resolved = shared[int(raw_v)]
        except (ValueError, IndexError):
            resolved = None
    elif cell_type == "inlineStr":
        inline = cell.find("m:is", NS)
        resolved = _text_from_si(inline) if inline is not None else ""
    elif cell_type in {"str", "e", "b"}:
        resolved = raw_v
    return raw_v, resolved, formula


def raw_cell_id(source_revision_id: str, sheet: str, coordinate: str) -> str:
    payload = f"{source_revision_id}\x1f{sheet}\x1f{coordinate}".encode("utf-8")
    return "rc_" + hashlib.sha256(payload).hexdigest()[:24]


def extract_raw_cells(
    xlsx_path: str | Path,
    *,
    source_id: str,
    source_revision_id: str,
    file_sha256: str,
) -> list[dict[str, object]]:
    """Extract every non-empty OOXML cell without coercing its stored lexical value."""
    path = Path(xlsx_path)
    rows: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as zf:
        shared = _shared_strings(zf)
        for sheet_title, sheet_xml in _sheet_targets(zf):
            root = ET.fromstring(zf.read(sheet_xml))
            for cell in root.findall(".//m:sheetData/m:row/m:c", NS):
                coord = cell.attrib.get("r")
                if not coord:
                    continue
                raw_v, resolved, formula = _cell_resolved_value(cell, shared)
                # A formula with no cached value is still material source content.
                if raw_v is None and resolved is None and formula is None:
                    continue
                cell_type = cell.attrib.get("t") or "n"
                rows.append(
                    {
                        "raw_cell_id": raw_cell_id(source_revision_id, sheet_title, coord),
                        "source_id": source_id,
                        "source_revision_id": source_revision_id,
                        "file_sha256": file_sha256,
                        "sheet_exact": sheet_title,
                        "cell_coordinate": coord,
                        "ooxml_type": cell_type,
                        "style_index": cell.attrib.get("s", ""),
                        "value_lexical": raw_v if raw_v is not None else "",
                        "text_resolved": resolved if resolved is not None else "",
                        "formula": formula if formula is not None else "",
                    }
                )
    return rows


def raw_index(rows: Iterable[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    return {(str(r["sheet_exact"]), str(r["cell_coordinate"])): r for r in rows}


def workbook_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
