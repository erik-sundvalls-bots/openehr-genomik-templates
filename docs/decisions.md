# Beslut och öppna frågor – fas 1

*Status: förslag från Grok Bot, 2026-10-15. Inget är beslutat förrän Erik godkänt.*

## 1. Underlaget i siffror
- 18 flikar: 3 informationsflikar (Information till granskare, Översikt, Vägval), *Alla variabler*, 14 listvärdesflikar.
- *Alla variabler*: 97 rader = 17 informationsblock + **73 variabler** (några namn återkommer i flera block: `patient_ref`, `laboratorium_ref`, `variant_ref`, `karyotyp_iscn`).
- Datatyper: Code 27, Reference 13, String 9, Identifier 8, UUID 3, Decimal 3, Quantity 3, Date 2, CodeableConcept 2, DateTime/Instant/Integer 1 vardera.
- FHIR-resurser: Observation 37, DiagnosticReport 11, Specimen 10, Procedure/GenomicStudy 6, Organization 3, Patient 2, ServiceRequest 2, Device 1.
- 14 värdemängder, 104 koder totalt (se `valuesets/valuesets.json`).

## 2. Mappningsresultat (se `analysis/variable-inventory.md`)
| Flagga | Antal | Betydelse |
|---|---|---|
| covered | 34 | Ren mappning till befintligt CKM-element |
| partial | 26 | Möjlig mappning men med kompromiss (fel granularitet, utkastarketyp, kodverk i Additional details) |
| gap | 9 | Inget lämpligt element – kräver specialisering/ny arketyp eller designbeslut |
| demografi (utanför template) | 4 | Patient-id/personnummer/subject-referenser = EHR-subject |

Huvudarketyper: `CLUSTER.genomic_variant_result.v1` (18 variabler), `CLUSTER.specimen.v1` (8), `OBSERVATION.laboratory_test_result.v1` (7), `CLUSTER.laboratory_test_analyte.v1` (7, TMB/MSI/HRD/tumörcellshalt), `CLUSTER.organisation.v1` (5), `CLUSTER.sequencing_assay.v0` (4).

### Identifierade luckor (gap)
1. **ASCO/AMP-tier** och **ESCAT** – finns inte i CKM; `genomic_variant_result` har bara ACMG (germline).
2. **Genetiskt ursprung** (somatisk/germline) – inget eget element i `genomic_variant_result.v1`.
3. **Kopietaltyp** – `genomic_copy_number_variant` har bara Gain/Loss; amplifiering och homozygot deletion saknas (underlaget använder SO-koder).
4. **Diagnostisk/terapeutisk implikation** som egna poster med id/status/variant_ref – FHIR har separata Observations; i openEHR behövs designbeslut.
5. **studie_id / analystyp** (GenomicStudy) – inget motsvarande i `sequencing_assay.v0`.

## 3. Föreslagen templateuppsättning
Enligt CGEM: rapporten är *Event Assessment*, remissen *Managed Response*.

| # | Template | Rot | Innehåll | Kategori |
|---|---|---|---|---|
| T1 | **Genomikrapport – cancer** (huvudtemplate) | `COMPOSITION.report-result.v1` | `OBSERVATION.laboratory_test_result.v1` med specimen (nivå 1 + härledd nivå 2 via Parent specimen identifier), anatomical_location, specimen_processing, sequencing_assay + device (panel), 0..* `genomic_variant_result` (+ strukturerade varianttyper: substitution/deletion/insertion/delins/duplication/inversion/CNV/translocation), 0..* `laboratory_test_analyte` för TMB/MSI/HRD/tumörcellshalt, organisation (laboratorium) | event |
| T2 | **Genomikremiss** (valfri) | `COMPOSITION.request.v1` | `INSTRUCTION.service_request.v1` (frågeställning, remiss_id), `EVALUATION.problem_diagnosis.v1` (ICD-10) | event |

Alternativ: lägga remissvariablerna (diagnos, frågeställning, remiss_id) direkt i T1 under *Test request details* / *Clinical information provided*, eftersom INCA tar emot färdiga svar och inte hanterar beställningsflödet. **Min rekommendation: börja med T1 som täcker allt (inkl. remissreferenser), och T2 bara om beställningsflödet ska modelleras.** Implikationer (diagnostisk/terapeutisk) läggs i T1 som klustrar per variant i första versionen.

`templates/reference/Molecular_Pathology_Report.oet` (HiGHmed, CKM-utkast) visar samma mönster och används som förlaga, men bygger på gamla v0-arketyper.

## 4. Format: ADL 1.4 OET → OPT 1.4 (rekommendation)
- **ADL 1.4 OET + OPT 1.4** är vad EHRbase, Better och de flesta CDR:er tar emot, och alla CKM-arketyperna ovan är ADL 1.4. FHIRconnect-mappningar (fas 3) refererar till OPT 1.4/webbtemplate-sökvägar.
- ADL2 är bättre långsiktigt (template = arketyp, AOM), men kräver konvertering av alla arketyper och ger sämre CDR-stöd idag.
- **Validering på boxen:** Java saknas idag (kan installeras). Förslag: installera JDK 17 + Archie (`com.nedap.healthcare.archie`) för att parsa/validera ADL och generera OPT, och köra EHRbase i Docker (finns redan) för slutlig validering genom att ladda upp OPT och posta exempelkompositioner. OET kan även öppnas i Archetype Designer/Template Designer för kontroll.
- Föreslagen arbetsgång: handskriven OET (enligt template-authoring-guiden) → OPT via Archie/EHRbase → webbtemplate + exempeldata → senare ADL2-export via Archie om ni vill.

## 5. Öppna frågor till Erik
1. **Templateantal:** räcker en rapporttemplate (T1), eller vill du ha separat remisstemplate (T2)?
2. **Luckor:** ska vi skapa lokala specialiseringar (t.ex. `genomic_variant_result-cancer` med ASCO-tier, ESCAT, genetiskt ursprung, exonnummer, ISCN) i `archetypes/drafts/`, eller föreslå ändringar upstream i CKM Genomics-projektet (som Norge/Tyskland driver)?
3. **Utkastarketyper:** OK att använda `sequencing_assay.v0` (TEAMREVIEW), `translocation_variant.v0` (REVIEWSUSPENDED), `service_request.v1` (REASSESS_DRAFT) och `genetic_variant_presence.v0` (DRAFT)?
4. **Implikationer:** klustrar inuti varianten (enklast) eller egna poster (EVALUATION) som FHIR:s separata Observations (bättre FHIR-spårbarhet)?
5. **Kodverk:** SO som primär för variationstyp/konsekvens/kopietal, SNOMED CT som alternativ – OK? Vilken SO-URI ska användas (`http://www.sequenceontology.org` vs. IG:s variant)?
6. **Lokala värdemängder** utan internationella koder (frågeställning, ASCO-tier, ESCAT, ctDNA/ctRNA/cfDNA, cellblock): vilken namnrymd/URI (förslag `https://cancercentrum.se/terminology/...` som platshållare)?
7. **Patient/organisation:** behandla patient via EHR-subject (ingen templatedata) och HSA-id i `organisation`-klustret – OK?
8. **Format:** OK med ADL 1.4 OET/OPT nu och ADL2 senare? Får jag installera Java/Archie och köra EHRbase i Docker på boxen för validering?
9. **Språk:** svenska etiketter i templaten (namnöversättningar) + engelska arketyper?
10. **Svenska arketyper:** jag har inte hittat någon svensk genomikarketyp; känner du till nationellt material (t.ex. Inera/Region) som borde kollas?
