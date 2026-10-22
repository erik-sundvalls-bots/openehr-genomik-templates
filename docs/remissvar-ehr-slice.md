# Remissvar – underlag: EHR Slice för den harmoniserade datamängden cancergenomik

*Utkast till avsnitt i remissvar på RCC i samverkans "Konfigurationsunderlag – Harmoniserad
datamängd cancergenomik". Svarsdatum 24 oktober 2026.*

## Vad är ett EHR Slice?

Ett EHR Slice är en avgränsad, teknikneutral specifikation av en informationsmängd, paketerad som
en FHIR Implementation Guide. Utöver FHIR-profiler, kodverk och värdemängder innehåller guiden
också openEHR-templates (med de internationella arketyper de bygger på) och de mappningar som
översätter mellan template och FHIR-profil, i båda riktningarna. Mappningarna uttrycks i
FHIRconnect, ett öppet och maskinläsbart format som kan köras av en mappningsmotor. Allt
versioneras och publiceras tillsammans. En leverantör kan då både ta emot och skicka FHIR och
lagra samma information beständigt och frågbart, utan att tolka specifikationen på egen hand.

## Varför det är relevant för RCC, INCA och EHDS

- **FHIR förblir utbytesformatet.** Underlagets FHIR-design (bl.a. Genomics Reporting IG och
  `ServiceRequest.reasonCode` för frågeställning) behålls oförändrad; EHR Slice lägger till,
  det ersätter inget.
- **openEHR ger en beständig och frågbar modell.** Samma variabler finns som openEHR-templates
  byggda på internationella CKM-arketyper, så data kan lagras och frågas (AQL) leverantörsoberoende
  och återanvändas för uppföljning, kvalitetsregister och forskning.
- **Mappningarna blir versionerade artefakter.** I stället för att varje system gör sin egen
  översättning publiceras mappningen tillsammans med profilerna och kan granskas, testas och
  versioneras. Det ligger i linje med EHDS, där EHR Slice har föreslagits som ett sätt att
  beskriva delmängder av journalinformation teknikneutralt och dubbelriktat mot FHIR.
- **Lokala kodlistor får en källa.** Frågeställning, ASCO/AMP- och ESCAT-nivåer har en enda tabell
  som både FHIR-kodverken och mappningen i båda riktningarna genereras från.

## Demonstration

Som underlag har vi byggt ett litet, körbart EHR Slice för T2 (remiss) och en del av T1
(genomiskt svar), i repot `openehr-genomik-templates`, katalogen `ehr-slice/`:

- FHIR-profiler för remiss (ServiceRequest), genomiskt svar (DiagnosticReport) och variant
  (Observation) på HL7 Genomics Reporting IG v3.0.0, med kodverk för frågeställning, ASCO/AMP och
  ESCAT samt värdemängder för Sequence Ontology, LOINC (genetiskt ursprung) och SNOMED CT (provtyp).
- openEHR-templates i ADL2 och OPT 1.4, inkluderade i guiden.
- Dubbelriktade FHIRconnect-mappningar: T2 helt; för T1 bl.a. gen, HGVS (c./p.), genetiskt
  ursprung, allelfrekvens, molekylär konsekvens (SO), ASCO/AMP och ESCAT.
- En faktisk körning med den öppna mappningsmotorn openFHIR 3.0.2: exemplen översattes
  FHIR → openEHR → FHIR → openEHR. 45 av 46 kontrollerade FHIR-element var identiska efter
  rundturen (undantaget är remittenten, som saknar element i T2); de kliniska openEHR-fälten var
  identiska. Se `ehr-slice/roundtrip/RESULTS.md`.

Demonstrationen är ett utkast. Kanoniska URL:er är platshållare, och några förenklingar är gjorda
(t.ex. ASCO/ESCAT som komponenter i variant-Observation i stället för separata
implication-Observationer). De står i `ehr-slice/README.md`.

## Förslag

Vi föreslår att RCC överväger att förvalta den harmoniserade datamängden som ett EHR Slice:
FHIR-profiler, openEHR-templates och FHIRconnect-mappningar i samma versionerade guide, med
gemensamma, maskinläsbara kodtabeller för de lokala kodlistorna.
