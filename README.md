# openehr-genomik-templates

**SV:** openEHR-templates för RCC i samverkans *Konfigurationsunderlag – Harmoniserad datamängd cancergenomik* (remissversion, NAG CancerGenomik). Målet är att hela konfigurationsunderlaget ska kunna representeras som openEHR-templates byggda på internationella CKM-arketyper. FHIR-resurs/element/profil per variabel spåras så att en senare EHR-Slice med FHIR-profil och dubbelriktad FHIRconnect-mappning blir möjlig.

**EN:** openEHR templates for the Swedish RCC *harmonised cancer genomics dataset* (consultation draft). Built from international CKM archetypes, with per-variable FHIR traceability to support a later EHR-Slice + FHIR profile + bidirectional FHIRconnect mappings.

## Status
Phase 1 (analysis) — no templates authored yet. See `docs/decisions.md`.

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
