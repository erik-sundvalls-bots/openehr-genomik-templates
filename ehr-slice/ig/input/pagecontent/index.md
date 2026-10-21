> **Demo / utkast.** Inte för produktion. Kanoniska URL:er (`https://example.org/...`) är platshållare.
> **Demo / draft.** Not for production use. Canonical URLs (`https://example.org/...`) are placeholders.

### Svenska

Den här guiden är ett **EHR Slice**: en FHIR Implementation Guide som utöver FHIR-profiler,
CodeSystems och ValueSets också bär de teknikneutrala openEHR-artefakterna för samma
informationsmängd – openEHR-templates (ADL2 och OPT 1.4) – och de **dubbelriktade
FHIRconnect-mappningarna** mellan templates och profiler. Allt versioneras och publiceras
tillsammans, så att ett system kan ta emot och skicka FHIR och samtidigt lagra informationen
beständigt och frågbart i openEHR.

Innehållet bygger på den harmoniserade datamängden för cancergenomik (konfigurationsunderlaget
på remiss) och på HL7 Genomics Reporting IG v3.0.0:

| Del | FHIR | openEHR |
|---|---|---|
| Remiss (T2) | [SE Genomics ServiceRequest](StructureDefinition-se-genomics-servicerequest.html) | template *Genomics request* |
| Svar (T1) | [SE Genomic Report](StructureDefinition-se-genomic-report.html), [SE Variant](StructureDefinition-se-variant.html) | template *Genomics cancer report* |
| Kodverk | frågeställning, ASCO/AMP, ESCAT, SO, LOINC LL378-1, SNOMED CT provtyp | lokala at-koder bundna till samma kodverk |

Se [Artefakter](artefacts.html) för templates och mappningar och [Rundtur](roundtrip.html)
för resultatet av en faktisk körning FHIR → openEHR → FHIR → openEHR med den öppna
FHIRconnect-motorn openFHIR.

### English

This guide is an **EHR Slice**: a FHIR Implementation Guide that, besides FHIR profiles,
CodeSystems and ValueSets, also carries the technology-neutral openEHR artefacts for the same
data set – openEHR templates (ADL2 and OPT 1.4) – and the **bidirectional FHIRconnect
mappings** between the templates and the profiles. Everything is versioned and published
together, so a system can exchange FHIR and at the same time persist the data in a queryable
openEHR form.

It is based on the Swedish harmonised cancer genomics data set (consultation draft) and on
HL7 Genomics Reporting IG v3.0.0. See [Artefacts](artefacts.html) and the
[round-trip evidence](roundtrip.html).

### Deviations from Genomics Reporting v3 (demo simplifications)

- ASCO/AMP tier, ESCAT tier and molecular consequence are components of the variant
  Observation instead of separate *implication* / *molecular-consequence* Observations.
- No variation type (coding-change-type): the T1 template has no element for it.
- There is no Swedish base profile for ServiceRequest; the request profile derives from core R4.
