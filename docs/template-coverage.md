# T1/T2 coverage vs variable inventory

*Updated 2026-10-21 (Europe/Stockholm). Inventory: `analysis/variable-inventory.json` (73 variables).*

## Templates

| ID | File | Root | Overlays / fills |
|----|------|------|------------------|
| T1 | `templates/adl2/openEHR-EHR-COMPOSITION.t_genomics_cancer_report.v1.0.0.adls` | `report-result` | lab_result → specimen (+anatomical_location, specimen_processing), TMB/MSI/HRD/cellularity analytes, GVR-cancer (+CNV-cancer, substitution/del/ins/indel, clinical implication, presence, translocation), organisation, sequencing_assay-genomic_study (+device, reference_sequence; study id, study type, coded method), device. Value sets bound: specimen type (provtyp + extraherat material), collection method, fixation method |
| T2 | `templates/adl2/openEHR-EHR-COMPOSITION.t_genomics_request.v1.0.0.adls` | `request` | service_request (mandate remiss_id / Requester order identifier; Receiver organisation), problem_diagnosis (mandate diagnosis name). Frågeställning: Reason for request specialised to `id63.1` *Clinical question / Frågeställning*, 1..* required, closed coded list (8 local codes) |

Archie full validation (parse + flatten + validate, 31 artefacts incl. all overlays): **0 failures** (`build/archie-validation.txt`).

## Coverage by inventory block

| Block | Vars | In T1/T2? | Notes |
|-------|------|-----------|-------|
| PATIENT | 2 | Out of scope | EHR subject / demographics |
| ORGANISATION | 3 | T1 + T2 | `organisation` Receiving laboratory / Receiver; HSA via Identifier |
| REMISS | 3 | T2 (+ T1 mirror) | remiss_id = service_request protocol id11; diagnos = problem_diagnosis; frågeställning = Reason for request → *Clinical question* (1..*, closed list; one ACTIVITY ≈ one FHIR ServiceRequest, recommended one ACTIVITY per question; see decisions §10.1) |
| PROVMATERIAL N1 | 10 | T1 | specimen + anatomical_location + specimen_processing; cellularity as analyte |
| PROVMATERIAL N2 | 2 | T1 | Child specimen + sequencing_assay nucleic acid |
| DIAGNOSTISK RAPPORT | 11 | T1 | lab_result fields + GVR fills; remiss_ref = Test request details / Requester order identifier |
| STUDIEMETADATA | 6 | T1 | sequencing_assay-genomic_study draft: Study identifier (studie_id), Study type (analystyp, HL7 genomic-study-type), coded Sequencing type (analysmetod, HL7 method type); status via overall test status |
| DEVICE / PANEL | 1 | T1 | device under assay / Testing details |
| VARIANT gemensamma | 9 | T1 | GVR-cancer (incl. genetiskt ursprung ASCO/ESCAT); presence draft |
| SNV/INDEL | 5 | T1 | GVR + substitution/del/ins/indel overlays |
| CNV | 4 | T1 | genomic_copy_number_variant-cancer |
| FUSION | 3 | T1 partial | Gene Part-of-fusion on parent GVR + translocation in Additional details |
| DIAGNOSTISK IMPLIKATION | 5 | T1 | variant_clinical_implication under GVR |
| TERAPEUTISK IMPLIKATION | 3 | T1 | same implication cluster (type = therapeutic) |
| TMB / MSI / HRD | 6 | T1 | dedicated analyte overlays with name constraints |

## Counts (inventory gap_flag, updated)

| gap_flag | Before (2026-10-15) | Now |
|----------|-----------|-----|
| covered | 34 | 40 |
| partial | 26 | 22 |
| covered_by_local_draft | – | 7 (genetic origin, ASCO, ESCAT, copy number type, implication id/status) |
| gap | 9 | 0 |
| out_of_scope_demographics | 4 | 4 |

## Value-set bindings (source → where bound)

| valuesets/ file | Bound in | Codes | External binding |
|---|---|---|---|
| provtyp + extraherat_material | T1 overlay `t_specimen_genomics` Specimen type `ac0.1` | 18 | SNOMED CT (15) |
| provtagningsteknik | T1 overlay `t_specimen_genomics` Collection method `ac0.2` | 15 | SNOMED CT (14; cell block has none) |
| fixeringsmetod | T1 overlay `t_specimen_processing_genomics` Method `ac0.1` | 3 | none in source |
| analystyp | draft `sequencing_assay-genomic_study` Study type `ac0.1` | 12 | HL7 genomic-study-type |
| analysmetod | draft `sequencing_assay-genomic_study` Sequencing type `ac0.2` | 9 | HL7 genomic-study-method-type |
| molecular_consequence | draft `genomic_variant_result-cancer` `ac0.4` (was empty) | 8 | SO (8) + SNOMED CT (4) |
| genetiskt_ursprung | draft `genomic_variant_result-cancer` `ac0.1` | 5 | SNOMED CT (2) |
| asco_tier / escat_tier | draft `genomic_variant_result-cancer` `ac0.2`/`ac0.3` | 7 / 11 | local only (namespace open, see decisions) |
| kopietaltyp | draft `genomic_copy_number_variant-cancer` (Amplification = `at7.1` under Gain, Homozygous deletion = `at8.1` under Loss) | 4 | SO in descriptions |
| fragestallning | T2 overlay `t_genomics_service_request` Clinical question (`id63.1`, 1..*) `ac0.1`, closed | 8 | local only |
| variationstyp | not bound: expressed by choice of structured-variant archetype | – | – |
| produktnamn | not bound: free text (Kit name / device name); list changes often | – | – |

## Still missing / deferred

1. ~~T2 frågeställning constraint missing from OPT (Ehrtslib gap B)~~: fixed by ehrtslib#134. The OPT now has the DV_CODED_TEXT with the 8 codes and occurrences 1..*.
2. **HL7 study type/method and SO term bindings missing from OPT (Ehrtslib gap D)**: the `#` parse error is fixed (ehrtslib#133) and the build workaround is removed, but the OPT exporter only converts `[terminology::code]` and `http://<host>/id/<code>` binding URIs. HL7 `CodeSystem#code` and OBO `SO_nnnnnnn` URIs are silently dropped. Codes and texts are present.
3. **OET lacks local coded-text value sets (gap C)**: the OPT is complete.
4. **ICD-10 binding** for diagnosis (T2 problem_diagnosis): external terminology, left to the target CDR.
5. **Per-finding fynd_id / status**: feeder_audit or Additional details; not a separate ENTRY.
6. **Widen lab_result slots** (optional local specialisation) if the target CDR's slot checks reject GVR / sequencing_assay placement.
7. **specimen_preparation**: not in repo; specimen_processing is used instead.
8. **Swedish translation** of 3 unused CKM archetypes (duplication, inversion, knowledge_base_reference).

## Design alternative: frågeställning as coded + free text

T2 follows the dataset's FHIR design (closed coded list, `ServiceRequest.reasonCode`, 1..*). Another option is coded plus open free text: allow `DV_TEXT` alongside `DV_CODED_TEXT`, or an open (extensible) value set.
- Pros: captures clinical nuance without "Other"; survives list changes without a new template version.
- Cons: weaker comparability and statistics; free text must be interpreted by the lab; the FHIR side gets `reasonCode.text` without a code, which breaks the dataset's coded-value requirement.

See `docs/decisions.md` §10.1.

## Validation performed (2026-10-21, `tools/build.sh`)

- Archie fork (`feature/adl2-to-adl14-downconverter` @ 6b4e39a, the content merged into the fork's `master` by PR #1) full validation of `archetypes/ckm-adl2`, `archetypes/drafts`, `templates/adl2`: **31/31 OK**.
- Ehrtslib main @ ebc2434 (includes #133, #134, #135) `export:opt14` / `export:oet14` for T1 and T2, with no `#`-stripping workaround.
- OPT 1.4 vs `AM/Release-1.4/Template.xsd`: both VALID. OET vs `OET/latest/CompositionTemplate.xsd`: both VALID.
- ADL 1.4 down-conversion of the 4 drafts with both Ehrtslib and Archie: OK.
- T2 OPT check: `at0062` (Clinical question) has occurrences 1..*, DV_CODED_TEXT, local code_list at0.1–at0.8.

## Earlier validation (2026-10-16)

- Archie (fork, `feature/adl2-to-adl14-downconverter` incl. PR #3) full validation of `archetypes/ckm-adl2`, `archetypes/drafts`, `templates/adl2`: 31/31 OK. Three earlier errors that `parse2` had missed were fixed: the T1 root/slot node ids had the wrong specialisation depth, the CNV-cancer value set added codes outside its parent, and the reference_sequence root was `id19`.
- Ehrtslib (main @ fc1b5b0) `export:opt14` / `export:oet14` for T1 and T2.
- OPT 1.4 vs `AM/Release-1.4/Template.xsd`: both VALID.
- OET vs `OET/latest/CompositionTemplate.xsd`: both VALID. They are not valid against Release-1.0.1, which has no `annotations` element (needed for the L10n workaround).
- ADL 1.4 down-conversion of the 4 drafts with both Ehrtslib and Archie: OK (`build/ehrtslib-adl14`, `build/archie-adl14`).
