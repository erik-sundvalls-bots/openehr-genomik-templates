# analysis

Analysis of the source dataset (`../source/`), first committed 2026-10-15.

- `variable-inventory.{csv,md,json}`: the 73 dataset variables, each with its openEHR target and a gap flag. Updated by hand as templates evolved; `../docs/template-coverage.md` builds on it.
- `variables-raw.json`: the variables as read from the *Alla variabler* sheet, including the dataset's FHIR resource/element/profile columns.
- `sheet-summary.json`: size and merged cells of each Excel sheet.
- `gms-prior-art/`: earlier Swedish (GMS) archetypes kept for comparison (see its README).
- `gms-solid-tumours-readme.md`: note on a GMS solid-tumour report template based on a HiGHmed template; source of this file not recorded.

The extraction script used to produce the JSON/CSV files was not committed.
