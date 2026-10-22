# openehr-genomik-templates

**SV:** openEHR-templates för RCC i samverkans *Konfigurationsunderlag – Harmoniserad datamängd cancergenomik* (remissversion, NAG CancerGenomik), byggda på internationella CKM-arketyper, samt en körbar demo av en EHR Slice: FHIR-profiler, kodverk och dubbelriktade FHIRconnect-mappningar för samma data.

**EN:** openEHR templates for the Swedish RCC *harmonised cancer genomics dataset* (consultation version), built from international CKM archetypes, plus a working EHR Slice demo: FHIR profiles, terminology and bidirectional FHIRconnect mappings for the same data.

## What is here

- Two templates: **Genomics cancer report** (`t_genomics_cancer_report`, on CKM `COMPOSITION.report-result`) and **Genomics request** (`t_genomics_request`, on CKM `COMPOSITION.request`), authored in ADL2 with English original and Swedish translation, and exported as OPT 1.4 and OET 1.4.
- Coverage of the dataset's 73 variables: 40 covered, 22 partly covered, 7 covered by local draft archetypes, 4 (demographics) out of scope, 0 gaps (`docs/template-coverage.md`).
- Four local draft archetypes for what CKM lacks (ASCO/AMP and ESCAT tiers, genetic origin, CNV amplification/homozygous deletion, clinical implication, study id/analysis type).
- An EHR Slice demo in `ehr-slice/`: FHIR R4 IG (SUSHI) on HL7 Genomics Reporting IG 3.0.0 with profiles for the genomics request and part of the genomics cancer report, local CodeSystems/ValueSets, the templates as IG artefacts, and FHIRconnect mappings run FHIR → openEHR → FHIR → openEHR in the open-source openFHIR engine.

**T1/T2:** some file names, docs and example ids use *T1* for the genomics cancer report and *T2* for the genomics request.

## Layout

Each folder has a short README describing its content and source.

| Path | Content |
|---|---|
| [`source/`](source/README.md) | The dataset: original Excel and a CSV per sheet |
| [`analysis/`](analysis/README.md) | Variable inventory (73 variables → openEHR targets), sheet summary, Swedish prior-art archetypes |
| [`valuesets/`](valuesets/README.md) | The dataset's value lists as CSV and structured JSON, with code-system URIs |
| [`archetypes/`](archetypes/README.md) | CKM archetypes in ADL 1.4 ([`ckm/`](archetypes/ckm/README.md)) and ADL2 ([`ckm-adl2/`](archetypes/ckm-adl2/README.md)), local drafts ([`drafts/`](archetypes/drafts/README.md)), `CKM-CATALOG.md` |
| [`translations/sv/`](translations/sv/README.md) | Local Swedish translations of 10 CKM archetypes |
| [`templates/`](templates/README.md) | The two templates in ADL2; HiGHmed *Molecular Pathology Report* OET as prior art |
| [`build/`](build/README.md) | Generated OPT/OET 1.4, ADL 1.4 down-conversions, validation reports |
| [`tools/`](tools/README.md) | `build.sh` and helper scripts |
| [`docs/`](docs/README.md) | Decisions (Swedish), coverage, tool notes, forum proposals and upstream issue drafts (not posted) |
| [`ehr-slice/`](ehr-slice/README.md) | EHR Slice demo: [`ig/`](ehr-slice/ig/README.md), [`fhirconnect/`](ehr-slice/fhirconnect/README.md), [`engine/`](ehr-slice/engine/README.md), [`examples/`](ehr-slice/examples/README.md), [`roundtrip/`](ehr-slice/roundtrip/README.md), [`tools/`](ehr-slice/tools/README.md) |

## Build and test

Templates and archetypes (writes `build/`):

```bash
EHRTSLIB=/path/to/ehrtslib ARCHIE=/path/to/archie-fork \
XSD=/path/to/openEHR-XSD/AM/Release-1.4 OET_XSD=/path/to/CompositionTemplate.xsd \
  tools/build.sh
```

Needs JDK 17, Deno, Python 3 with `lxml`, a checkout of [Ehrtslib](https://github.com/ErikSundvall/ehrtslib) (`main`), and the Archie fork with the ADL2 → ADL 1.4 down-converter ([erik-sundvalls-bots/archie](https://github.com/erik-sundvalls-bots/archie), branch `feature/adl2-to-adl14-downconverter`). The script runs Archie parse/flatten/validate on all ADL2 files, exports OPT 1.4 and OET 1.4 with Ehrtslib, down-converts the drafts to ADL 1.4 with both tools, and checks OPT/OET against the openEHR XSDs.

EHR Slice (SUSHI, FHIRconnect validation, openFHIR round-trip, optional IG Publisher): see [`ehr-slice/README.md`](ehr-slice/README.md#reproduce).

## Current status

- Archie: 31 of 31 ADL2 archetypes and templates parse, flatten and validate (`build/archie-validation.txt`).
- OPT 1.4 and OET 1.4 of both templates: XSD-valid (`build/xsd-validation.txt`), exported with Ehrtslib `main` without local workarounds.
- SUSHI: 0 errors, 0 warnings. IG Publisher: 0 errors, 0 broken links (warnings and details: `ehr-slice/ig/QA-SUMMARY.md`).
- Round-trip in openFHIR 3.0.2: FHIR → openEHR → FHIR 45 of 46 checked FHIR elements identical; openEHR → FHIR → openEHR 78 of 89 flat paths identical (`ehr-slice/roundtrip/RESULTS.md`).

## Known limitations

- Draft archetypes and the Swedish translations are local and not reviewed in CKM; proposals for CKM are in `docs/forum-proposals/`.
- Sequence Ontology URIs follow a recommendation not yet finally decided: OBO term PURLs (`http://purl.obolibrary.org/obo/SO_nnnnnnn`) in ADL, system `http://www.sequenceontology.org` in FHIR (`docs/decisions.md` §10.3).
- *Frågeställning* (clinical question) in the genomics request is a closed coded list (1..*, `ServiceRequest.reasonCode`) as in the dataset; a coded-plus-free-text alternative is discussed in `docs/decisions.md` §10.1.
- Canonical URLs of the IG and the local CodeSystems are `example.org` placeholders.
- The EHR Slice simplifies the Genomics Reporting IG (tiers and molecular consequence as Observation components, variation type not mapped, only the first transcript mapped); the round-trip differences are party references (composer, health care facility), a context start-time null flavour in the request, and `ServiceRequest.requester`, which the request template has no element for. Details and engine/mapping-library findings: `ehr-slice/README.md`.
- Structural nodes without a term in the ADL2 source get generic names from the RM type ("History", "Tree") in the exported OPTs.
- The Archie fork's down-converter builds only on its feature branch, not on the fork's `master` (Archie 4.0.0); see `docs/upstream-issue-drafts/09-archie-fork-master-build.md`.

## Sources and licences

- Dataset (`source/`, `valuesets/` CSV): © RCC i samverkan.
- CKM archetypes (`archetypes/ckm/`, `archetypes/ckm-adl2/`): © openEHR Foundation, CC-BY-SA 4.0.
- `templates/reference/Molecular_Pathology_Report.oet`: © HiGHmed.
- `ehr-slice/fhirconnect/model/openehr-lib/` and `ehr-slice/tools/schema/`: copied unchanged from the FHIRconnect mapping library and specification, Apache-2.0 (see `NOTICE.md` / `SOURCE.md` there).
- The FHIR IG declares CC-BY-4.0 (`ehr-slice/ig/sushi-config.yaml`). No licence file has been chosen for the rest of the repository's own content.
