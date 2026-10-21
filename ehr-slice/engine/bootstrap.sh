#!/usr/bin/env bash
# Copy the slice's FHIRconnect mappings and OPT 1.4 templates into ./bootstrap and ask the
# running engine to (re)load them. Usage: ./bootstrap.sh [engine-base-url]
set -euo pipefail
cd "$(dirname "$0")"
BASE="${1:-http://localhost:8080}"
SLICE=..; REPO=../..
mkdir -p bootstrap && find bootstrap -mindepth 1 -delete && mkdir -p bootstrap/mappings bootstrap/templates  # keep the bind-mounted dir itself
cp -r "$SLICE/fhirconnect/model" "$SLICE/fhirconnect/projects" bootstrap/mappings/
find bootstrap/mappings -type f ! -name '*.yml' ! -name '*.yaml' -delete
python3 "$SLICE/tools/repair_opt_terms.py" >/dev/null && cp "$SLICE"/templates/opt14/*.opt bootstrap/templates/
curl -sf -X POST "$BASE/\$bootstrap" | python3 -c 'import json,sys;d=json.load(sys.stdin);print({k:d[k] for k in ("created","updated","unchanged","failed")});[print(" ",f["outcome"],f["path"],f.get("message") or "") for f in d["files"] if f["outcome"]!="UNCHANGED"]'
