"""Work-around for a gap in the OPT 1.4 export used to build ../build/opt14.

The exported OPTs omit term_definitions for structural LOCATABLE nodes (ITEM_TREE,
HISTORY, ...). Most OPT consumers tolerate that, but the EHRbase SDK web-template parser
used by openFHIR (OPTParser.buildNode) throws a NullPointerException on any locatable
node without a term. This script copies the missing terms from the CKM ADL 1.4 source
archetypes (falling back to a generic text per RM type) and writes repaired copies to
ehr-slice/templates/opt14/. The originals in build/opt14 are left untouched; the proper
fix belongs in the OPT exporter (ehrtslib#142 fixed only ADL 1.4 input; ADL2 input
is ehrtslib#145). Retested 2026-10-22: still needed.
"""
import re, pathlib, xml.etree.ElementTree as ET
HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
SRC, DST = REPO / "build" / "opt14", HERE.parent / "templates" / "opt14"
NS = "http://schemas.openehr.org/v1"; XSI = "http://www.w3.org/2001/XMLSchema-instance"
ET.register_namespace("", NS); ET.register_namespace("xsi", XSI)
T = lambda n: f"{{{NS}}}{n}"; XT = f"{{{XSI}}}type"
GENERIC = {"ITEM_TREE": "Tree", "HISTORY": "History", "ITEM_LIST": "List", "CLUSTER": "Cluster"}

def adl14_terms(aid):
    for d in ("ckm", "drafts"):
        p = REPO / "archetypes" / d / f"{aid}.adl"
        if p.exists():
            txt = p.read_text(encoding="utf-8")
            en = txt.split('["en"] = <', 1)[1] if '["en"] = <' in txt.split("term_definitions", 1)[-1] else ""
            return {m[0]: (m[1], m[2]) for m in re.findall(
                r'\["(at[0-9.]+)"\]\s*=\s*<\s*text\s*=\s*<"([^"]*)">\s*description\s*=\s*<"([^"]*)">', en)}
    return {}

def repair(path):
    tree = ET.parse(path); root = tree.getroot(); added = []
    roots = [root.find(T("definition"))] + [e for e in root.iter(T("children")) if e.get(XT) == "C_ARCHETYPE_ROOT"]
    for r in roots:
        aid = r.findtext(f"{T('archetype_id')}/{T('value')}")
        tds = r.findall(T("term_definitions")); have = {t.get("code") for t in tds}
        missing = []
        def walk(o):
            for a in o.findall(T("attributes")):
                for c in a.findall(T("children")):
                    if c.get(XT) == "C_ARCHETYPE_ROOT": continue
                    nid, rm = c.findtext(T("node_id")), c.findtext(T("rm_type_name"))
                    if nid and nid not in have and rm in GENERIC and nid not in [m[0] for m in missing]:
                        missing.append((nid, rm))
                    walk(c)
        walk(r)
        if not missing: continue
        src = adl14_terms(aid); idx = list(r).index(tds[-1]) + 1
        for nid, rm in missing:
            text, desc = src.get(nid, (GENERIC[rm], "@ internal @"))
            td = ET.Element(T("term_definitions"), {"code": nid})
            ET.SubElement(td, T("items"), {"id": "text"}).text = text
            ET.SubElement(td, T("items"), {"id": "description"}).text = desc
            r.insert(idx, td); idx += 1; added.append(f"{aid} {nid} {rm} -> {text!r}")
    DST.mkdir(parents=True, exist_ok=True)
    tree.write(DST / path.name, xml_declaration=True, encoding="UTF-8")
    return added

for p in sorted(SRC.glob("*.opt")):
    for a in repair(p): print(p.name, a)
