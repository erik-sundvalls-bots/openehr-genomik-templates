# T1/T2 coverage vs variable inventory

*Updated 2026-10-15 (Europe/Stockholm). Inventory: `analysis/variable-inventory.json` (73 variables).*

## Templates

| ID | File | Root | Overlays / fills |
|----|------|------|------------------|
| T1 | `templates/adl2/openEHR-EHR-COMPOSITION.t_genomics_cancer_report.v1.0.0.adls` | `report-result` | lab_result → specimen (+anatomical_location, specimen_processing), TMB/MSI/HRD/cellularity analytes, GVR-cancer (+CNV-cancer, substitution/del/ins/indel, clinical implication, presence, translocation), organisation, sequencing_assay (+device, reference_sequence), device |
| T2 | `templates/adl2/openEHR-EHR-COMPOSITION.t_genomics_request.v1.0.0.adls` | `request` | service_request (mandate remiss_id / Requester order identifier; Receiver organisation), problem_diagnosis (mandate diagnosis name) |

Archie `parse2`: **OK** for both.

## Coverage by inventory block

| Block | Vars | In T1/T2? | Notes |
|-------|------|-----------|-------|
| PATIENT | 2 | Out of scope | EHR subject / demographics |
| ORGANISATION | 3 | T1 + T2 | `organisation` Receiving laboratory / Receiver; HSA via Identifier |
| REMISS | 3 | T2 (+ T1 mirror) | remiss_id = service_request protocol id11; diagnos = problem_diagnosis; frågeställning = Reason for request / Clinical indication (rename in OPT) |
| PROVMATERIAL N1 | 10 | T1 | specimen + anatomical_location + specimen_processing; cellularity as analyte |
| PROVMATERIAL N2 | 2 | T1 | Child specimen + sequencing_assay nucleic acid |
| DIAGNOSTISK RAPPORT | 11 | T1 | lab_result fields + GVR fills; remiss_ref = Test request details / Requester order identifier |
| STUDIEMETADATA | 6 | T1 partial | sequencing_assay + overall status; **studie_id**, **analystyp** still gap/extension |
| DEVICE / PANEL | 1 | T1 | device under assay / Testing details |
| VARIANT gemensamma | 9 | T1 | GVR-cancer (incl. genetiskt ursprung ASCO/ESCAT); presence draft |
| SNV/INDEL | 5 | T1 | GVR + substitution/del/ins/indel overlays |
| CNV | 4 | T1 | genomic_copy_number_variant-cancer |
| FUSION | 3 | T1 partial | Gene Part-of-fusion on parent GVR + translocation in Additional details |
| DIAGNOSTISK IMPLIKATION | 5 | T1 | variant_clinical_implication under GVR |
| TERAPEUTISK IMPLIKATION | 3 | T1 | same implication cluster (type = therapeutic) |
| TMB / MSI / HRD | 6 | T1 | dedicated analyte overlays with name constraints |

## Counts (approximate against inventory gap_flag)

| gap_flag | Inventory | Template status |
|----------|-----------|-----------------|
| covered | 34 | Represented in T1/T2 structure |
| partial | 26 | Structure present; value-set / path polish in OPT |
| gap | 9 | Mostly studie_id, analystyp, implication entry ids; ASCO/ESCAT/origin addressed by **draft specialisations** now included |
| out_of_scope_demographics | 4 | Unchanged |

## Still missing / deferred

1. **OET/OPT for Better** — see `docs/template-oet-gaps.md`.
2. **studie_id** — no dedicated element on sequencing_assay; use Extension or lab internal id until archetype evolves.
3. **analystyp** (snp/cnv/…) — may stay template annotation / Extension.
4. **ICD-10 / frågeställning / ASCO / ESCAT / SO bindings** — local value sets in `valuesets/`; bind in Better OPT.
5. **Per-finding fynd_id / status** — feeder_audit or Additional details; not separate ENTRY.
6. **Widen lab_result slots** (optional local specialisation) if Better slot-checks reject GVR / sequencing_assay placement.
7. **specimen_preparation** — not in repo; using specimen_processing in Additional details instead.

## Validation performed

- Archie `parse2` on T1 and T2 ADL2 templates: OK.
- Archie `parse14` on down-converted drafts in `build/archie-adl14/`: OK (3 cancer drafts + organisation sample).
- Ehrtslib ADL14 on same drafts: OK (`build/ehrtslib-adl14/*.v1.0.0.adl`).
- Ehrtslib ADL14 on T1/T2 templates: **not** valid ADL1.4 archetypes (expected; not OET).
