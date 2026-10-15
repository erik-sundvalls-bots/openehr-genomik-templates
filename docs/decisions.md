# Beslut och öppna frågor – fas 2

*Uppdaterad 2026-10-15 (Europe/Stockholm). Fas 1-bakgrund behålls; Eriks svar 1–5 inarbetade.*

## 1. Underlaget i siffror (oförändrat från fas 1)
- 73 variabler: 34 covered, 26 partial, 9 gap, 4 demografi.
- 14 värdemängder i `valuesets/`.
- Se `analysis/variable-inventory.md`.

## 2. Eriks beslut (svar på fas 1-frågor)

| # | Fråga | Beslut |
|---|-------|--------|
| 1 | Templateantal | **Både T1 Genomikrapport och T2 Genomikremiss** |
| 2 | Luckor | **Lokala specialiseringar** i `archetypes/drafts/` **och** forumfärdiga förslag i `docs/forum-proposals/` (Erik publicerar själv — botten postar **inte**) |
| 3 | Utkastarketyper | **OK** att använda `sequencing_assay.v0`, `translocation_variant.v0`, `service_request.v1`, `genetic_variant_presence.v0` |
| 4 | Format / verktyg | Modellera i **ADL2**, konvertera till **ADL 1.4** efteråt. Java/Archie OK. **Kör inte EHRbase** — validering sker i Better-produkter på Karolinska |
| 5 | Språk | **Engelska** som original/tekniskt språk + **svensk översättning** för export. Preferera ADL2-funktioner som stödjer detta |

Övriga fas 1-frågor (implikationer-design, SO-URI, lokala URI:er, patient/organisation) hanteras i utkast/forumförslag tills vidare; implikationer i fas 2 modelleras som **CLUSTER under variant** (se beslut 2.1 nedan).

### 2.1 Implikationer (arbetshypotes fas 2)
Kluster inuti varianten (`CLUSTER.variant_clinical_implication`) — enklast för T1 v1 och tillräckligt för FHIR-spårbarhet via Implication identifier. Utvärdera EVALUATION senare om Better-/FHIRconnect-behov kräver egna poster.

## 3. Templateuppsättning (beslutad)

| # | Template | Rot | CGEM |
|---|----------|-----|------|
| T1 | Genomikrapport – cancer | `COMPOSITION.report-result.v1` | Event Assessment |
| T2 | Genomikremiss | `COMPOSITION.request.v1` | Managed Response |

ADL2-utkast: `templates/adl2/`. OET 1.4-export kommer efter nedkonvertering.

## 4. Format och verktygskedja (uppdaterat)

### 4.1 ADL2 först
- CKM-arketyper (ADL 1.4) konverteras till ADL2 med **Archie 3.21** → `archetypes/ckm-adl2/` (25 filer, parse2 OK).
- Specialiseringar och templates författas som **ADL2** (`.adls`, `adl_version=2.0.6`) med `original_language=en` och `translations["sv"]`.

### 4.2 Archie: endast 1.4 → 2
Archie (`com.nedap.healthcare.archie`) har `ADL14Parser` + `ADL14Converter` (1.4→2) och `ADLParser` / `ADLArchetypeSerializer` för ADL2. **Ingen inbyggd 2→1.4-väg.**  
Verktyg: `/workspace/tools/archie` → `archie-convert-0.1.0.jar` (kommandon `parse14`, `to2`, `parse2`, `batch`, `roundtrip14to2`).

### 4.3 ADL2 → 1.4 via Ehrtslib (sidospår)
Erik är författare till [ehrtslib](https://github.com/ErikSundvall/ehrtslib) (TypeScript/Deno) som har `ADL14Serializer` (2→1.4) och OPT/OET-stöd. Efter Archie-vägen: prova samma nedkonvertering/validering och dokumentera luckor i `docs/ehrtslib-gaps.md`. **Blockera inte** huvudspåret på Ehrtslib.

### 4.4 Validering
- Box: Archie parse2 för ADL2; senare Better på Karolinska för OPT/data.
- **Ingen EHRbase** på boxen (beslut 4).

## 5. Luckor och lokala specialiseringar

### 5.1 ASCO/ESCAT-gap bekräftat
CKM-sökning 2026-10-15: **0 träffar** för ASCO/AMP/ESCAT. GMS `mtbp_classification.v0` har endast grov relevansskala. Svenskt material: `analysis/swedish-prior-art/` (= GMS Information-specifications / modellbibliotek-lokala arketyper).

### 5.2 Drafts (ADL2, EN+SV, parse2 OK)

| Fil | Förälder / typ | Fyller |
|-----|----------------|--------|
| `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adls` | specialiserar `genomic_variant_result.v1` | Genetiskt ursprung, ASCO/AMP, ESCAT, exon, ISCN, SO molecular consequence, slot för implikation |
| `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_copy_number_variant-cancer.v1.0.0.adls` | specialiserar `genomic_copy_number_variant.v1` | Amplifiering + homozygot deletion i kopietaltyp |
| `archetypes/drafts/openEHR-EHR-CLUSTER.variant_clinical_implication.v1.0.0.adls` | ny CLUSTER | Diagnostisk/terapeutisk implikation (id, typ, status, …) |

### 5.3 Forumförslag (ej publicerade)
`docs/forum-proposals/01`–`05` — ASCO+ESCAT vs ACMG; genetiskt ursprung; CNV Gain/Loss; implikationer; övrigt (exon/ISCN/SO).

## 6. Kvarvarande öppna frågor
6. Kodverk: SO som primär för variationstyp/konsekvens/kopietal — URI (`http://www.sequenceontology.org` vs IG-variant)?
7. Lokala värdemängder (ASCO, ESCAT, frågeställning, …): namnrymd `https://cancercentrum.se/terminology/...` som platshållare?
8. Patient via EHR-subject; HSA-id i `organisation` — bekräfta.
9. När ska Erik posta forumförslagen?
10. Preferens för Better Template Designer vs handskriven OET efter ADL2→1.4?

## 7. Repo
Privat: `https://github.com/erik-sundvalls-bots/openehr-genomik-templates` (gh som `erik-sundvalls-bots`).
