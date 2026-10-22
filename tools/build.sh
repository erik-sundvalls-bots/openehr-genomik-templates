#!/usr/bin/env bash
# Rebuild all derived artefacts. Requires: JDK17 (JAVA_HOME), deno, Ehrtslib checkout, Archie fork checkout (built with ./gradlew jar).
set -euo pipefail
G="$(cd "$(dirname "$0")/.." && pwd)"
EHRTSLIB="${EHRTSLIB:-/workspace/ehrtslib}"; ARCHIE="${ARCHIE:-/workspace/archie}"; XSD="${XSD:-/workspace/xsd14/AM/Release-1.4}"; OET_XSD="${OET_XSD:-/workspace/openehr-spec/specifications-ITS-XML/components/OET/latest/CompositionTemplate.xsd}"
if [[ -z "${ARCHIE_CP:-}" ]]; then
  echo "allprojects { tasks.register('printCp') { doLast { if (project.name=='tools') println 'CP=' + project.sourceSets.main.runtimeClasspath.asPath } } }" > /tmp/printcp.gradle
  (cd "$ARCHIE" && ./gradlew -q jar -x test >/dev/null && ./gradlew -q -I /tmp/printcp.gradle :tools:printCp) | sed -n 's/^CP=//p' > /tmp/archie.cp
  ARCHIE_CP="$(cat /tmp/archie.cp):$ARCHIE/referencemodels/build/libs/referencemodels-3.21.0.jar:$ARCHIE/openehr-rm/build/libs/openehr-rm-3.21.0.jar"
fi
CP="$ARCHIE_CP"
echo "== Archie full validation (parse + flatten + validate)"
java -cp "$CP" "$G/tools/ArchieValidateAll.java" "$G/archetypes/ckm-adl2" "$G/archetypes/drafts" "$G/templates/adl2" 2>/dev/null > "$G/build/archie-validation.raw" || true
{ grep -v "^total=" "$G/build/archie-validation.raw" | sort; grep "^total=" "$G/build/archie-validation.raw"; } > "$G/build/archie-validation.txt"; rm -f "$G/build/archie-validation.raw"; tail -1 "$G/build/archie-validation.txt"
TMP=$(mktemp -d); cp -r "$G/archetypes" "$TMP/"
echo "== Ehrtslib OPT/OET 1.4 (ehrtslib $(git -C "$EHRTSLIB" rev-parse --short HEAD))"
mkdir -p "$G/build/opt14" "$G/build/oet14"; : > "$G/build/ehrtslib-export-log.txt"
for T in t_genomics_cancer_report t_genomics_request; do for F in opt oet; do
  (cd "$EHRTSLIB" && deno task -q export:${F}14 --lib "$TMP/archetypes/ckm-adl2" --lib "$TMP/archetypes/drafts" \
    --template "$G/templates/adl2/openEHR-EHR-COMPOSITION.$T.v1.0.0.adls" --lang en,sv --out "$G/build/${F}14/openEHR-EHR-COMPOSITION.$T.$F") 2>&1 | sed 's/^/  /' | tee -a "$G/build/ehrtslib-export-log.txt" >/dev/null
done; done
echo "== Ehrtslib ADL 1.4 down-conversion (drafts + sv-translated CKM copies)"
mkdir -p "$G/build/ehrtslib-adl14" "$G/build/archie-adl14"
(cd "$EHRTSLIB" && EHRTSLIB="$EHRTSLIB" deno run -q --allow-read --allow-write --allow-env=EHRTSLIB "$G/tools/ehrtslib-down14.ts" "$G/build/ehrtslib-adl14" "$TMP"/archetypes/drafts/*.adls)
echo "== Archie fork ADL 1.4 down-conversion"
for f in "$G"/archetypes/drafts/*.adls; do
  o="$G/build/archie-adl14/$(basename "$f" | sed -E 's/\.v([0-9]+)\.[0-9]+\.[0-9]+.*\.adls$/.v\1.adl/')"
  java -cp "$CP" com.nedap.archie.adl14.down.ADL2ToADL14Cli "$f" "$o" 2>/dev/null && echo "  OK $(basename "$o")" || echo "  FAIL $(basename "$f")"
done
echo "== XSD validation"
python3 - "$XSD" "$G" "$OET_XSD" <<'PY' | tee "$G/build/xsd-validation.txt"
import sys,glob; from lxml import etree
xsd,g,oet=sys.argv[1],sys.argv[2],sys.argv[3]
for kind,schema in (("opt14",f"{xsd}/Template.xsd"),("oet14",oet)):
    for f in sorted(glob.glob(f"{g}/build/{kind}/*")):
        s=etree.XMLSchema(etree.parse(schema)); d=etree.parse(f)
        print(f"  {f.split('/')[-1]}: {'VALID' if s.validate(d) else 'INVALID '+str(s.error_log.last_error)}")
PY
rm -rf "$TMP"
