# Template → OET / OPT gaps

*Updated 2026-10-15 (Europe/Stockholm).*

## Goal
The target environment uses a commercial CDR and template tooling. Runtime needs **OPT** (and usually **web template**), authored as **OET** or Archetype Designer `.t.json`, not raw ADL2 templates.

## What works today (box)

| Step | Status |
|------|--------|
| Author ADL2 templates + overlays (T1/T2) | Done — Archie `parse2` OK |
| Down-convert **specialised archetypes** ADL2→1.4 | Done — Archie fork + Ehrtslib; `parse14` OK on drafts in `build/archie-adl14/` and `build/ehrtslib-adl14/` |
| Down-convert **templates** ADL2→1.4 as archetypes | **Not usable** — Ehrtslib emits `undefined[undefined]` / missing `concept`; not OET |
| ADL2 template → **OET XML** | **Missing** — neither Archie fork nor Ehrtslib #117 path produces OET |
| OPT / web-template generation | **Missing** on box (no CDR on the box by decision) |

## Slot / modelling notes affecting OPT import

1. **Test result slot (`id98` / at0097)** in CKM `laboratory_test_result.v1.2.8` regex allows only `laboratory_test_analyte` / `laboratory_test_panel`. T1 still places `genomic_variant_result-cancer` there following **CKM Molecular Pathology Report** (genetic_variant at at0097) and the inventory. target-CDR often accepts this; strict slot validation may fail until CKM widens the slot or we add a local `laboratory_test_result-genomics` specialisation.
2. **Testing details (`id111` / at0110)** regex allows only `device`. T1 places `sequencing_assay` there (same CKM Molecular Pathology Report pattern) and nests `device` under the assay. Same caveat as (1).
3. **Specimen processing**: `specimen` Processing details (`id69`) allows `specimen_preparation` only. T1 puts `specimen_processing.v1` in **Additional details (`id84`)**.
4. **translocation_variant** / **genetic_variant_presence** are not in GVR Structured variant regex → T1 places them under GVR **Additional details (`id99`)**.
5. **Template overlays** are ADL2 constructs; OET uses nested `<Items>` — manual rebuild or a converter is required.

## Recommended path to the target CDR

1. Import ADL 1.4 **draft specialisations** from `build/archie-adl14/` (or Ehrtslib twins) into the project CKM / Archetype Designer.
2. Rebuild T1/T2 as **OET** (or Designer UI) referencing those archetypes + CKM parents — using this repo’s ADL2 templates as the **design blueprint** (slot fills, occurrences, analyte name constraints, bilingual labels).
3. Compile/import OPT in the target CDR; validate clinical data there.

## Open tooling work
- Ehrtslib: template → OET (or OPT2) serializer (tracked conceptually in Ehrtslib gaps / #117).
- Archie fork: archetype down-convert is usable; template/OET export not started.
