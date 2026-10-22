# openehr-genomik-templates

**SV:** openEHR-templates för RCC i samverkans *Konfigurationsunderlag – Harmoniserad datamängd cancergenomik* (remissversion, NAG CancerGenomik). Målet är att hela konfigurationsunderlaget ska kunna representeras som openEHR-templates byggda på internationella CKM-arketyper. FHIR-resurs/element/profil per variabel spåras så att en senare EHR-Slice med FHIR-profil och dubbelriktad FHIRconnect-mappning blir möjlig.

**EN:** openEHR templates for the Swedish RCC *harmonised cancer genomics dataset* (consultation draft). Built from international CKM archetypes, with per-variable FHIR traceability to support a later EHR-Slice + FHIR profile + bidirectional FHIRconnect mappings.

## Status (2026-10-21)
- T1 Genomics cancer report and T2 Genomics request are authored in ADL2 (`templates/adl2/`), EN original + SV translation. Of the 73 variables, 69 are covered, partly covered or covered by local drafts and 4 (demographics) are out of scope; no gaps remain (`docs/template-coverage.md`).
- `tools/build.sh` rebuilds and validates everything: Archie full validation (31/31 OK), OPT 1.4 + OET 1.4 via Ehrtslib (XSD-valid), ADL 1.4 down-conversion via Ehrtslib and the Archie fork.
- **Frågeställning (T2)** follows the dataset's FHIR design: required closed coded list, 1..*, multiple selection (`ServiceRequest.reasonCode`); one ACTIVITY ≈ one ServiceRequest. *Alternative design:* coded plus open free text (DV_TEXT alongside DV_CODED_TEXT, or an extensible value set). It keeps clinical nuance and tolerates list changes, but weakens comparability and breaks the dataset's coded-value requirement. See `docs/decisions.md` §10.
- **SO URIs:** OBO term PURLs (`http://purl.obolibrary.org/obo/SO_nnnnnnn`) in ADL; FHIR system `http://www.sequenceontology.org` (no trailing slash). Recommended, pending final decision.
- Next phases: EHR-Slice, FHIR profile, FHIRconnect mappings.

The phase 2 notes below are kept for history.

## Layout
| Path | Content |
|---|---|
| `source/xlsx/` | Original Excel (18 sheets) |
| `source/csv/` | UTF-8 CSV export of every sheet |
| `analysis/` | `variable-inventory.{csv,md,json}` (73 variables → openEHR target + gap flag), sheet summary |
| `valuesets/` | Each Listvärden sheet as CSV + structured JSON; `valuesets.json` with code-system URIs |
| `archetypes/ckm/` | ADL 1.4 of all chosen CKM archetypes (unchanged) + `../CKM-CATALOG.md` |
| `archetypes/drafts/` | Future local specialisations / new archetypes |
| `templates/reference/` | CKM *Molecular Pathology Report* OET (HiGHmed draft) as prior art |
| `docs/decisions.md` | Template set, format recommendation, open questions (Swedish) |

Source data © RCC i samverkan; CKM archetypes © openEHR Foundation, CC-BY-SA 4.0.


## Phase 2 status (2026-10-15)
- `archetypes/ckm-adl2/`: all 25 CKM archetypes converted to ADL2 with Archie 3.21 (`batch`). All pass `parse2`.
- `archetypes/drafts/` (ADL2, original language EN + SV translation, all pass Archie `parse2`):
  - `genomic_variant_result-cancer`: genetic origin, ASCO/AMP, ESCAT, exon, ISCN, SO consequence, implication slot
  - `genomic_copy_number_variant-cancer`: adds Amplification and Homozygous deletion
  - `variant_clinical_implication` (new CLUSTER)
- `templates/adl2/`: T1 `t_genomics_cancer_report` (report-result) and T2 `t_genomics_request` (request). EN+SV scaffolds that pass `parse2`; detailed constraints not yet done.
- `docs/forum-proposals/01–05`: forum drafts. **Not posted**; Erik posts them himself.
- `docs/decisions.md`: answers 1–5 included.
- `docs/ehrtslib-gaps.md`: ADL2→1.4 with Ehrtslib currently fails (0/5 usable).
- `tools/`: ArchieConvert.java, the pom, and the Ehrtslib script.
- **Not done:** ADL 1.4 / OET / OPT export (no working 2→1.4 converter), validation in the target CDR, full T1 constraints (specimen, assay, analytes, variant slots).
