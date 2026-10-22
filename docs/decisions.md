# Beslut och öppna frågor – fas 2

*Uppdaterad 2026-10-21 (Europe/Stockholm). Fas 1-bakgrund behålls; Eriks svar 1–5 inarbetade; beslut om frågeställning och studie-/analystyp (§10).*

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
| 4 | Format / verktyg | Modellera i **ADL2**, konvertera till **ADL 1.4** efteråt. Java/Archie OK. **Kör inte EHRbase** — validering sker i målmiljöns CDR/mallverktyg |
| 5 | Språk | **Engelska** som original/tekniskt språk + **svensk översättning** för export. Preferera ADL2-funktioner som stödjer detta |

Övriga fas 1-frågor (implikationer-design, SO-URI, lokala URI:er, patient/organisation) hanteras i utkast/forumförslag tills vidare; implikationer i fas 2 modelleras som **CLUSTER under variant** (se beslut 2.1 nedan).

### 2.1 Implikationer (arbetshypotes fas 2)
Kluster inuti varianten (`CLUSTER.variant_clinical_implication`) — enklast för T1 v1 och tillräckligt för FHIR-spårbarhet via Implication identifier. Utvärdera EVALUATION senare om CDR-/FHIRconnect-behov kräver egna poster.

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
- Box: Archie parse2 för ADL2; senare målmiljöns CDR för OPT/data.
- **Ingen EHRbase** på boxen (beslut 4).

## 5. Luckor och lokala specialiseringar

### 5.1 ASCO/ESCAT-gap bekräftat
CKM-sökning 2026-10-15: **0 träffar** för ASCO/AMP/ESCAT. GMS `mtbp_classification.v0` har endast grov relevansskala. Svenskt material: `analysis/gms-prior-art/` (= GMS Information-specifications / modellbibliotek-lokala arketyper).

### 5.2 Drafts (ADL2, EN+SV, parse2 OK)

| Fil | Förälder / typ | Fyller |
|-----|----------------|--------|
| `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adls` | specialiserar `genomic_variant_result.v1` | Genetiskt ursprung, ASCO/AMP, ESCAT, exon, ISCN, SO molecular consequence, slot för implikation |
| `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_copy_number_variant-cancer.v1.0.0.adls` | specialiserar `genomic_copy_number_variant.v1` | Amplifiering + homozygot deletion i kopietaltyp |
| `archetypes/drafts/openEHR-EHR-CLUSTER.variant_clinical_implication.v1.0.0.adls` | ny CLUSTER | Diagnostisk/terapeutisk implikation (id, typ, status, …) |

### 5.3 Forumförslag (ej publicerade)
`docs/forum-proposals/01`–`05` — ASCO+ESCAT vs ACMG; genetiskt ursprung; CNV Gain/Loss; implikationer; övrigt (exon/ISCN/SO).

## 6. Kvarvarande öppna frågor (med rekommendation)

| # | Fråga | Alternativ | Rekommendation |
|---|-------|-----------|----------------|
| 6 | **SO-URI** i term_bindings | (a) OBO-term-PURL `http://purl.obolibrary.org/obo/SO_0001583`; (b) FHIR-system `http://www.sequenceontology.org` (utan avslutande snedstreck, enligt HL7 THO NamingSystem SO) + kod `SO:0001583`; (c) `http://identifiers.org/so/SO:0001583` | **Rekommenderat, inväntar Eriks slutliga besked:** (a) i ADL (en resolverbar URI per term; används i `genomic_variant_result-cancer`) och (b) på FHIR-sidan. Mappningen a↔b är mekanisk (`SO_nnnnnnn` ↔ `SO:nnnnnnn`). Obs: bara per-term-adresser resolverar; själva katalogen `/obo/` ger 404. |
| 7 | **Namnrymd för lokala värdemängder** (ASCO, ESCAT, frågeställning, cellblock …) | (a) organisationsägd HTTPS-namnrymd, t.ex. `https://<ägare>/fhir/CodeSystem/<namn>`; (b) `urn:oid:` under ägarens OID; (c) inga externa bindningar, endast lokala at-koder | **(a)** när ägaren (den nationella genomik-/cancerorganisationen) har bekräftat basadressen. Tills dess **(c)**: värdemängderna finns redan som lokala at-koder, och inga platshållar-URI:er läggs in i ADL. |
| 8 | Patient via EHR-subject; HSA-id i `organisation` | – | Behåll. Bekräftas med mottagande system. |
| 9 | När ska forumförslagen 01–07 postas? | – | Gärna 07 (översättningar) först. Det är minst kontroversiellt och ger granskare för resten. |
| 10 | Grafiskt mallverktyg vs genererad OET | (a) importera genererad OPT direkt; (b) importera OET och efterbearbeta i mallverktyg | **(a)** för test. OPT:n är komplett och XSD-giltig, medan OET:n saknar lokala kodade värdemängder (Ehrtslib-gap C). |
| 11 | **Studie-/analystyp-luckan**: lokal specialisering vs CKM-ändring | (a) behåll `sequencing_assay-genomic_study` lokalt; (b) föreslå ändring i CKM (förslag 07 §2) | **BESLUTAT 2026-10-21: (a)+(b).** Lokala utkastet används nu; CKM-ändringsförslaget finns färdigt i `forum-proposals/07` §2 (ej postat, Erik postar). |
| 12 | Frågeställning: stängd kodad lista vs kodat + fritext | (a) stängd lista; (b) kodat + öppen fritext | **BESLUTAT 2026-10-21: (a)**, som underlagets FHIR-design (`ServiceRequest.reasonCode`, 1..*, obligatorisk, flerval). Se §10. Alternativ (b) dokumenteras som möjligt designval. |

## 7. Repo
Privat: `https://github.com/erik-sundvalls-bots/openehr-genomik-templates` (gh som `erik-sundvalls-bots`).

## 8. T1/T2 filled (2026-10-15 kväll)
ADL2 templates filled with nested `template_overlay` slot fills (not skeletons). See `docs/template-coverage.md` and `docs/template-oet-gaps.md`. Archie parse2 OK. Specialised drafts down-converted under `build/archie-adl14/` / `build/ehrtslib-adl14/`. Template→OET for target-CDR still open.

## 9. Luckor stängda 2026-10-16
- `studie_id`, `analystyp` (+ `analysmetod`) är modellerade i en ny lokal specialisering, `archetypes/drafts/openEHR-EHR-CLUSTER.sequencing_assay-genomic_study.v0.0.1.adls`. Den är bunden till HL7 genomic-study-type / method-type. T1-overlayn `t_sequencing_assay` specialiserar nu denna.
- `ac0.4` (Molecular consequence) har fått 8 SO-termer med bindning till SO, och till SNOMED CT där sådan finns.
- CNV-cancer: Amplification och Homozygous deletion är nu specialiseringar av Gain/Loss (`at7.1`, `at8.1`). Den tidigare lösningen, som lade till nya koder i en omdefinierad värdemängd, var ogiltig ADL2 (VALUESET_REDEFINITION_ERROR).
- Värdemängder från `valuesets/` är bundna i T1/T2-overlays. Se tabellen i `template-coverage.md`.
- Svenska översättningar har lagts in lokalt i 10 CKM ADL2-kopior (`translations/sv/`, `tools/add_sv_translation.py`). CKM-förslag i `forum-proposals/07`.
- `tools/build.sh` bygger om allt och validerar (Archie full validering, Ehrtslib OPT/OET, ADL 1.4 via båda verktygen, XSD).

## 10. Beslut 2026-10-21: frågeställning, studie-/analystyp, SO-URI

### 10.1 Frågeställning (T2) — beslutat: följ underlagets FHIR-design
Underlaget (`source/csv/Alla_variabler.csv`, REMISS/frågeställning; `Listvärden - Frågeställning`): 1..*, Code, obligatorisk, kodat värde, flerval tillåtet, FHIR `ServiceRequest.reasonCode` (R4), "Separata ServiceRequest per frågeställning rekommenderas".

Modellering i T2 (`t_genomics_service_request`-overlayn på `INSTRUCTION.service_request.v1`):
- `Reason for request` (id63) specialiseras till `id63.1` med namnet **Clinical question / Frågeställning**, `occurrences 1..*` (obligatorisk, flerval).
- Värdet är `DV_CODED_TEXT` med **stängd** lokal värdemängd `ac0.1` (8 koder, `valuesets/fragestallning.json`; beskrivningar från underlaget). Ingen fritext i elementet.
- Mappning: openEHR `ACTIVITY` ↔ FHIR `ServiceRequest` (en aktivitet är den enhet som beställs och följs upp med ACTIONs), `Reason for request` ↔ `ServiceRequest.reasonCode`, remiss-id (protocol `Requester order identifier`, delat av alla aktiviteter i INSTRUCTION). Underlaget mappar `remiss_id` till `ServiceRequest.id`; med en ServiceRequest per frågeställning bör det delade remiss-id:t i stället bli `ServiceRequest.requisition` (gruppidentifierare) och varje ServiceRequest få eget id. Detta tas upp i FHIRconnect-fasen.
- `ACTIVITY` behåller arketypens `1..*`. **Rekommenderat mönster**: en ACTIVITY per frågeställning (ger separata ServiceRequest per frågeställning, som underlaget rekommenderar). Flera frågeställningar i en ACTIVITY är också giltigt (motsvarar flera `reasonCode` i en ServiceRequest). Vi tvingar inte 1 frågeställning per aktivitet, eftersom underlaget bara *rekommenderar* separata ServiceRequests men kräver 1..* flerval.
- Arketypens fritextelement `Reason description` (id65) är fortfarande tillgängligt (ej begränsat i T2), som i CKM. Det kan tas bort (occurrences 0) om man vill ha en helt stängd remiss.

**Alternativ design (ej vald): kodat + öppen fritext.** Tillåt `DV_TEXT` bredvid `DV_CODED_TEXT` i elementet (eller en öppen värdemängd, ADL2 `constraint_status = extensible`), så att remittenten kan skriva fritext när listan inte räcker.
- *Fördelar:* fångar kliniska nyanser utan "Övrigt"; tål listförändringar utan ny mallversion.
- *Nackdelar:* sämre jämförbarhet och statistik; fritext måste tolkas av labbet; FHIR-sidan får `reasonCode.text` utan kod, och det bryter underlagets krav på kodat värde.

### 10.2 Studie-/analystyp — beslutat
Behåll lokala utkastet `sequencing_assay-genomic_study` **och** förbered CKM-ändringsförslaget. Verifierat: förslaget finns i `docs/forum-proposals/07-ckm-swedish-translations-and-sequencing-assay.md` §2 (Study identifier, Study type, kodad Sequencing type). Ej postat.

### 10.3 SO-URI — rekommenderat (inväntar Eriks slutliga besked)
ADL: OBO-term-PURL `http://purl.obolibrary.org/obo/SO_nnnnnnn`. FHIR: system `http://www.sequenceontology.org` (utan avslutande snedstreck, HL7 THO NamingSystem SO), kod `SO:nnnnnnn`. Förekomster med snedstreck i docs/valuesets är rättade.

## 11. EHR Slice-demo 2026-10-21 (förenklingar att känna till)

Demo i `ehr-slice/` (se `ehr-slice/README.md` och `docs/remissvar-ehr-slice.md`). Förenklingar jämfört med Genomics Reporting IG v3 och underlaget:

- ASCO/AMP-nivå, ESCAT-nivå och molekylär konsekvens är komponenter i variant-Observation, inte separata *implication*-/*molecular-consequence*-Observationer (en-till-många-mappning med `derivedFrom` är för stor för demon).
- Variationstyp (coding-change-type) mappas inte: T1 saknar element för den.
- `Observation.value` ("Present") är en konstant vid export och lagras inte.
- Ingen svensk basprofil för ServiceRequest finns; remissprofilen bygger på R4 core.
- Kanoniska URL:er (`https://example.org/fhir/ehr-slice-se-genomics`) och lokala CodeSystem-URL:er är platshållare. **Öppen fråga:** vilken namnrymd (RCC/INCA, Inera, HL7 Sverige) ska äga dem?
