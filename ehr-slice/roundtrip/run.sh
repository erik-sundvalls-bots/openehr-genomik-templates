#!/usr/bin/env bash
# FHIR -> openEHR -> FHIR round-trip through a running openFHIR engine.
# Prerequisites: engine running (../engine/docker-compose.yml) and mappings loaded
# (../engine/bootstrap.sh). Usage: ./run.sh [engine-base-url]
set -euo pipefail
cd "$(dirname "$0")"
BASE="${1:-http://localhost:8080}"
OUT=out; mkdir -p "$OUT"
EX=../examples
run() { # $1 = short name, $2 = template id, $3 = input bundle
  local n="$1" tid="$2" in="$3" q; q=$(python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1]))' "$tid")
  for fmt in flat canonical; do
    curl -sf -X POST "$BASE/\$toopenehr?format=$fmt&templateId=$q" -H 'Content-Type: application/fhir+json' \
      --data @"$in" -o "$OUT/$n.toopenehr.$fmt.parameters.json"
    python3 - "$OUT/$n.toopenehr.$fmt.parameters.json" "$EX/openehr/$n.$fmt.json" <<'PY'
import json, sys
p = json.load(open(sys.argv[1]))
comp = next(x for x in p["parameter"] if x["name"] == "composition")["valueString"]
json.dump(json.loads(comp), open(sys.argv[2], "w"), indent=2, ensure_ascii=False)
PY
  done
  curl -sf -X POST "$BASE/openfhir/tofhir?templateId=$q" -H 'Content-Type: application/json' \
    --data @"$EX/openehr/$n.canonical.json" | python3 -m json.tool --no-ensure-ascii > "$OUT/$n.tofhir.bundle.json"
  # second pass: the exported FHIR goes back to openEHR, to compare openEHR with openEHR
  curl -sf -X POST "$BASE/\$toopenehr?format=flat&templateId=$q" -H 'Content-Type: application/fhir+json' \
    --data @"$OUT/$n.tofhir.bundle.json" -o "$OUT/$n.second-pass.flat.parameters.json"
  echo "$n: FHIR -> openEHR (flat, canonical) -> FHIR -> openEHR done"
}
mkdir -p "$EX/openehr"
run T2-request "Genomics request" "$EX/fhir/T2-request-bundle.json"
run T1-report "Genomics cancer report" "$EX/fhir/T1-report-bundle.json"
python3 compare.py
