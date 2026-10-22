# EHR Slice demo – Swedish cancer genomics

**SV:** En liten men körbar *EHR Slice* för den harmoniserade datamängden för cancergenomik:
openEHR-templates (ADL2 + OPT 1.4), FHIR R4-profiler med kodverk och värdemängder, och
dubbelriktade FHIRconnect-mappningar, paketerad som en FHIR IG. Mappningarna har körts med den
öppna motorn openFHIR (FHIR → openEHR → FHIR → openEHR); resultatet finns i
[`roundtrip/RESULTS.md`](roundtrip/RESULTS.md).

**EN:** A small, working EHR Slice for the Swedish harmonised cancer genomics data set: openEHR
templates, FHIR profiles + terminology, and bidirectional FHIRconnect mappings, packaged as one
FHIR IG. Demo/draft: canonical URLs (`https://example.org/fhir/ehr-slice-se-genomics`) are
placeholders.

## What is in it

| Path | Content |
|---|---|
| `ig/` | FHIR IG source (FSH/SUSHI): `input/fsh/` profiles, terminology, examples; `input/resources/` the openEHR and FHIRconnect artefacts as `Binary` + a `Library` manifest; `input/pagecontent/` SV/EN pages |
| `fhirconnect/` | FHIRconnect mappings (grammar `FHIRConnect/v1.0.0`), **generated** from `tools/fhirconnect-src/` |
| `fhirconnect/model/openehr-lib/` | 8 model mappings reused unchanged from the open FHIRconnect mapping library (Apache-2.0, see `NOTICE.md`) |
| `fhirconnect/model/local/` | new model mapping: `CLUSTER.genomic_variant_result-cancer.v1` ↔ variant Observation |
| `fhirconnect/projects/se-genomics/{request,report}/` | context + extension mappings for T2 and T1 |
| `templates/opt14/` | OPT 1.4 used by the engine (copy of `../build/opt14`, refreshed by `engine/bootstrap.sh`) |
| `examples/fhir/` | input Bundles built from the IG examples |
| `examples/openehr/` | compositions produced by the engine (flat and canonical JSON) |
| `engine/` | `docker-compose.yml` (openFHIR 3.0.2 + MongoDB, pinned) and `bootstrap.sh` |
| `roundtrip/` | `run.sh`, `compare.py`, raw engine responses in `out/`, `RESULTS.md` |
| `tools/` | generators and checks (below) |

Profiles: `SEGenomicsServiceRequest` (T2), `SEGenomicReport` and `SEVariant` (T1, on Genomics
Reporting IG v3.0.0), `SEGenomicsSpecimen`, `SEGenomicsLaboratory` (on `hl7se.fhir.base`
SEBaseOrganization, HSA-id), `SEGenomicsReferringDiagnosis`. Terminology: CodeSystems
frågeställning, ASCO/AMP tier, ESCAT tier; ValueSets for these plus molecular consequence (SO,
`http://www.sequenceontology.org`), genetic origin (LOINC LL378-1) and specimen type (SNOMED CT).

## One table, both directions

`tools/code_tables.py` is the single source for every local openEHR at-code ↔ FHIR code pair.
It generates the FHIR CodeSystems/ValueSets (`gen_terminology_fsh.py`) and the per-code
FHIRconnect `manual` blocks in both directions (`gen_fhirconnect.py`). openFHIR has no
terminology server, so `conceptmap:` is not used.

## Reproduce

```bash
cd ehr-slice
python3 tools/gen_terminology_fsh.py && (cd ig && sushi build .)   # FHIR profiles + examples
python3 tools/gen_fhirconnect.py && python3 tools/validate_fhirconnect.py   # needs pyyaml, jsonschema
python3 tools/make_bundles.py                                        # examples/fhir/*.json
(cd engine && docker compose up -d && ./bootstrap.sh)
roundtrip/run.sh                                                     # writes roundtrip/RESULTS.md
python3 tools/gen_ig_artefacts.py && (cd ig && sushi build .)        # Binary/Library + pages
(cd ig && java -jar publisher.jar -ig ig.ini)                        # optional: full IG site (needs Jekyll)
```

IG Publisher result: 0 errors, 0 broken links (see `ig/QA-SUMMARY.md`).

`validate_fhirconnect.py` checks every file against the JSON Schemas of the FHIRconnect
specification (vendored in `tools/schema/`, see `SOURCE.md`) and cross-checks `extends` and
context references.

## Result (openFHIR 3.0.2)

See `roundtrip/RESULTS.md` for the full field-by-field table. In short:

- **T2** request: identifier, status, intent, service, date, both frågeställning codes, receiving
  laboratory (name + HSA-id) and referring diagnosis (ICD-10) survive FHIR → openEHR → FHIR.
- **T1** report: identifier, status, LOINC code + text, GE category, effective/issued,
  conclusion, remiss-id (basedOn), laboratory, specimen (id, SNOMED CT type, collection time)
  and, per variant, gene, c./p. HGVS, genetic origin, allele frequency, SO consequence, ASCO/AMP
  and ESCAT tiers survive.
- openEHR → FHIR → openEHR: all clinical flat paths identical; differences only in party
  references (`composer`, `health_care_facility`).
- Not regenerated: `ServiceRequest.requester` (T2 has no requester element; it only becomes the
  composition composer).

## Known limitations and findings

Demo simplifications (also stated in the IG):

- ASCO/AMP tier, ESCAT tier and molecular consequence are components of the variant Observation,
  not separate Genomics Reporting *implication* / *molecular-consequence* Observations.
- Variation type (coding-change-type) is not mapped: the T1 template has no element for it.
- `Observation.value` ("Present", LOINC LA9633-4) is a constant on export; it is not stored.
- Only the first Transcript cluster of a variant is mapped.
- No Swedish base profile for ServiceRequest exists; the request profile derives from core R4.

Findings while running the engine (worked around here; worth reporting upstream):

1. **OPT 1.4 export (Ehrtslib)**: fixed upstream, no workaround left. Earlier OPTs lacked
   `term_definitions` for structural nodes (ITEM_TREE, HISTORY), and the web-template parser used
   by openFHIR failed on that (ehrtslib#145); bound local value sets were exported as external
   code lists, so openFHIR wrote DV_CODED_TEXT without `value` (ehrtslib#147). Both are fixed on
   Ehrtslib main (37657ec, PR #154), and the engine now uses the plain export. Side effect: structural
   nodes without a term in the ADL2 source get a generic name synthesised from the RM type
   ("Tree", "History"), so compositions carry e.g. "History" where the CKM ADL 1.4 text was
   "Event Series". Flat paths and mappings are unaffected.
2. **Mapping library, `service_request.v1`**: maps the requester to `$composition/provider`, which
   does not exist in the RM; neutralised in `se_genomics_service_request.yml`.
3. **Mapping library, `laboratory_test_result.v1`**: the `unknown` status entry has a non-path
   `openehrCondition.targetRoot`, and the manual entries are not matched per element, so every
   status came back as `unknown`; overridden in `se_genomic_report.yml`. Its `basedOn` mapping
   emitted an empty CarePlan; also overridden.
4. **openFHIR 3.0.2**: a `manual` block directly on a repeating element (e.g. `reasonCode`) is
   evaluated against the whole collection, so every repetition gets the last matching code. Put
   the table in a `followedBy` child with `$fhirRoot`/`$openehrRoot` instead (done here).
5. **openFHIR 3.0.2**: when an element allows DV_TEXT or DV_IDENTIFIER, the identifier is lost on
   export unless the mapping says `type: IDENTIFIER`.
6. **openFHIR 3.0.2**: DV_PARSABLE `formalism` is always written as `text/html` (HGVS strings get
   the wrong formalism); a manual formalism is dropped.
7. **openFHIR 3.0.2**: `fhirConfig.structureDefinition` must be the base resource URL; a profile
   URL silently disables the model mapping.
8. **FHIRconnect spec schema** does not yet allow the `link` key that the mapping library uses
   (reported as WARN by `validate_fhirconnect.py`); the library README still says the engine
   supports only v0.9.0, while openFHIR 3.0.2 runs the v1.0.0 files.
