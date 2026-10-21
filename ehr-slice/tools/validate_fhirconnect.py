"""Structural validation of all FHIRconnect files against the published JSON Schemas,
plus cross-reference checks (context -> model/extension names, extends targets)."""
import json, pathlib, sys, yaml, jsonschema

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent / "fhirconnect"
model_s = json.load(open(HERE / "schema" / "model-mapping.schema.json"))
ctx_s = json.load(open(HERE / "schema" / "contextual-mapping.schema.json"))
names, contexts, errors = {}, [], 0
for f in sorted(list(ROOT.rglob("*.yml")) + list(ROOT.rglob("*.yaml"))):
    doc = yaml.safe_load(open(f))
    schema = ctx_s if doc.get("type") == "context" else model_s
    errs = sorted(jsonschema.Draft7Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
    rel = f.relative_to(ROOT)
    upstream = "openehr-lib" in str(rel)
    for e in errs:
        if upstream:   # unchanged upstream file: report, but do not fail on known schema lag
            print(f"WARN(upstream) {rel}: {'/'.join(map(str, e.path))}: {e.message[:200]}")
        else:
            errors += 1; print(f"SCHEMA {rel}: {'/'.join(map(str, e.path))}: {e.message[:200]}")
    if doc["type"] == "context": contexts.append((rel, doc))
    else: names[doc["metadata"]["name"]] = (rel, doc)
    print(f"{'OK ' if not errs else ('WRN' if upstream else 'ERR')} {doc['type']:9} {rel}")
for n, (rel, d) in names.items():
    ext = d["spec"].get("extends")
    if ext and ext not in names:
        errors += 1; print(f"XREF {rel}: extends unknown model '{ext}'")
for rel, d in contexts:
    c = d["context"]
    for n in c.get("archetypes", []) + c.get("extensions", []) + [c["start"]]:
        if n not in names:
            errors += 1; print(f"XREF {rel}: references unknown mapping '{n}'")
print(f"\n{len(names)} model/extension + {len(contexts)} context files, {errors} problem(s)")
sys.exit(1 if errors else 0)
