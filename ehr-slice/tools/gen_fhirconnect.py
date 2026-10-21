"""Expand generated code-mapping blocks in FHIRconnect sources.

Copies tools/fhirconnect-src/** to fhirconnect/**, replacing each line
`__MANUAL_CC:<TABLE>[:<fhir prefix>]__` with one FHIRconnect `manual` entry per row of
code_tables.<TABLE> (local openEHR at-code <-> FHIR Coding in a CodeableConcept),
indented like the marker. `__MANUAL_CODE:<TABLE>:<fhir path>__` does the same for a plain
FHIR code element such as DiagnosticReport.status.

For a repeating element put the marker in a followedBy child with relative paths
($fhirRoot / $openehrRoot) so each repetition is matched on its own; see
se_genomics_service_request.yml. Everything else is copied verbatim.
"""
import pathlib, re, shutil
import code_tables as ct

HERE = pathlib.Path(__file__).resolve().parent
SRC, DST = HERE / "fhirconnect-src", HERE.parent / "fhirconnect"

def yq(s):
    s = str(s)
    if re.fullmatch(r"[0-9.]+", s) or s[:1] in "*&!%@[{|>#-?" or ": " in s or " #" in s or s.endswith(":") or "'" in s:
        return '"' + s.replace('"', '\\"') + '"'
    return s

def manual_cc(table, ind, prefix=""):
    pre = prefix + "." if prefix else ""
    rows = getattr(ct, table)
    out = []
    for r in rows:
        p = " " * ind
        out += [f"{p}- name: {yq(table.lower() + '_' + r['at'])}",
                f"{p}  openehrCondition:",
                f"{p}    targetRoot: $openehrRoot",
                f"{p}    targetAttribute: defining_code/code_string",
                f"{p}    operator: one of",
                f"{p}    criteria: {r['at']}",
                f"{p}  openehr:",
                f"{p}    - path: defining_code/terminology_id",
                f"{p}      value: local",
                f"{p}    - path: defining_code/code_string",
                f"{p}      value: {r['at']}",
                f"{p}    - path: value",
                f"{p}      value: {yq(r['at_text'])}",
                f"{p}  fhirCondition:",
                f"{p}    targetRoot: $fhirRoot.{pre}coding",
                f"{p}    targetAttribute: code",
                f"{p}    operator: one of",
                f"{p}    criteria: {yq(r['code'])}",
                f"{p}  fhir:",
                f"{p}    - path: {pre}coding.system",
                f"{p}      value: {yq(r['system'])}",
                f"{p}    - path: {pre}coding.code",
                f"{p}      value: {yq(r['code'])}",
                f"{p}    - path: {pre}coding.display",
                f"{p}      value: {yq(r['display'])}"]
    return out

def manual_code(table, ind, fhirpath):
    """Local at-code <-> plain FHIR code (e.g. a status element), one manual entry per row."""
    p = " " * ind; out = []
    for r in getattr(ct, table):
        out += [f"{p}- name: {yq(table.lower() + '_' + r['code'])}",
                f"{p}  openehrCondition:",
                f"{p}    targetRoot: $openehrRoot",
                f"{p}    targetAttribute: defining_code/code_string",
                f"{p}    operator: one of",
                f"{p}    criteria: {r['at']}",
                f"{p}  openehr:",
                f"{p}    - path: defining_code/terminology_id",
                f"{p}      value: local",
                f"{p}    - path: defining_code/code_string",
                f"{p}      value: {r['at']}",
                f"{p}    - path: value",
                f"{p}      value: {yq(r['at_text'])}",
                f"{p}  fhirCondition:",
                f"{p}    targetRoot: $fhirRoot",
                f"{p}    targetAttribute: {fhirpath}",
                f"{p}    operator: one of",
                f"{p}    criteria: {yq(r['code'])}",
                f"{p}  fhir:",
                f"{p}    - path: {fhirpath}",
                f"{p}      value: {yq(r['code'])}"]
    return out

if DST.exists():
    for p in DST.rglob("*"):
        if p.is_file() and (SRC / p.relative_to(DST)).exists(): p.unlink()
for src in SRC.rglob("*"):
    if src.is_dir(): continue
    dst = DST / src.relative_to(SRC); dst.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for line in src.read_text().splitlines():
        m = re.fullmatch(r"(\s*)__MANUAL_CC:(\w+)(?::([\w.()]+))?__\s*", line)
        m2 = re.fullmatch(r"(\s*)__MANUAL_CODE:(\w+):([\w.]+)__\s*", line)
        if m: lines += manual_cc(m.group(2), len(m.group(1)), m.group(3) or "")
        elif m2: lines += manual_code(m2.group(2), len(m2.group(1)), m2.group(3))
        else: lines.append(line)
    head = "# GENERATED from ehr-slice/tools/fhirconnect-src by gen_fhirconnect.py; edit the source, not this file.\n"
    txt = "\n".join(lines) + "\n"
    dst.write_text(head + txt if "__MANUAL_C" in src.read_text() else txt)
    print("wrote", dst.relative_to(HERE.parent))
