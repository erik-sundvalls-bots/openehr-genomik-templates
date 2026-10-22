// Profiles for the EHR Slice demo. Each profile is paired with an openEHR template
// (T1 = Genomics cancer report, T2 = Genomics request) through FHIRconnect context mappings.

Profile: SEGenomicsServiceRequest
Parent: ServiceRequest
Id: se-genomics-servicerequest
Title: "SE Genomics ServiceRequest (genomikremiss)"
Description: "Request for genomic analysis (T2). One ServiceRequest corresponds to one openEHR ACTIVITY of INSTRUCTION.service_request.v1 in template 'Genomics request'. The Genomics Reporting IG v3 has no ServiceRequest profile, so this derives from core R4."
* ^status = #draft
* ^experimental = true
* identifier 1..1 MS
* identifier ^short = "remiss_id (openEHR: protocol/Requester order identifier)"
* status MS
* intent = #order
* code 1..1 MS
* code ^short = "Requested genomic service (openEHR: Service name)"
* subject 1..1 MS
* subject only Reference(Patient)
* authoredOn MS
* reasonCode 1..* MS
* reasonCode from FragestallningVS (required)
* reasonCode ^short = "frågeställning – closed coded list, multiple selection (openEHR: Clinical question)"
* reasonReference MS
* reasonReference only Reference(SEGenomicsReferringDiagnosis)
* reasonReference ^short = "Referring diagnosis (openEHR: EVALUATION.problem_diagnosis.v1)"
* performer 0..1 MS
* performer only Reference(SEGenomicsLaboratory)
* performer ^short = "Receiving laboratory (openEHR: CLUSTER.organisation.v1 in protocol)"

Profile: SEGenomicsReferringDiagnosis
Parent: Condition
Id: se-genomics-referring-diagnosis
Title: "SE Genomics referring diagnosis"
Description: "Diagnosis motivating the genomic request (T2: EVALUATION.problem_diagnosis.v1). ICD-10 (Swedish edition in practice; generic ICD-10 system used in the demo)."
* ^status = #draft
* ^experimental = true
* code 1..1 MS
* subject 1..1

Profile: SEGenomicsLaboratory
Parent: http://hl7.se/fhir/ig/base/StructureDefinition/SEBaseOrganization
Id: se-genomics-laboratory
Title: "SE Genomics laboratory"
Description: "Performing or receiving genomics laboratory, based on the Swedish base Organization profile (HSA-id)."
* ^status = #draft
* ^experimental = true
* identifier 1..* MS
* identifier[hsaid] 1..1 MS
* name 1..1 MS

Profile: SEGenomicsSpecimen
Parent: Specimen
Id: se-genomics-specimen
Title: "SE Genomics specimen (provmaterial nivå 1)"
Description: "Original specimen (T1: CLUSTER.specimen.v1)."
* ^status = #draft
* ^experimental = true
* identifier 1..* MS
* type 1..1 MS
* type from SpecimenTypeSEVS (extensible)
* collection.collected[x] only dateTime
* collection.collectedDateTime 1..1 MS

Profile: SEGenomicReport
Parent: http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/genomic-report
Id: se-genomic-report
Title: "SE Genomic report"
Description: "Genomic report (T1 'Genomics cancer report': OBSERVATION.laboratory_test_result.v1). Subset used by the demo: identifier, status, code, issued, performer, specimen, basedOn and variant results."
* ^status = #draft
* ^experimental = true
* identifier 1..1 MS
* identifier ^short = "rapport_id (openEHR: protocol/Laboratory internal identifier)"
* status MS
* code MS
* code.text MS
* subject 1..1
* subject only Reference(Patient)
* issued 1..1 MS
* performer 1..* MS
* performer only Reference(SEGenomicsLaboratory)
* specimen 1..* MS
* specimen only Reference(SEGenomicsSpecimen)
* basedOn 1..* MS
* basedOn only Reference(SEGenomicsServiceRequest)
* basedOn ^short = "remiss_ref (openEHR: Test request details/Requester order identifier)"
* result[variant] MS
* result[variant] only Reference(SEVariant)
* conclusion MS

Profile: SEVariant
Parent: http://hl7.org/fhir/uv/genomics-reporting/StructureDefinition/variant
Id: se-variant
Title: "SE Variant"
Description: "Variant finding (T1: CLUSTER.genomic_variant_result-cancer.v1). Demo simplification: molecular consequence, AMP/ASCO/CAP tier and ESCAT tier are carried as components on the variant (mirroring the openEHR cluster) instead of separate molecular-consequence / diagnostic-implication / therapeutic-implication Observations as in Genomics Reporting v3. See the round-trip page."
* ^status = #draft
* ^experimental = true
* subject 1..1
* subject only Reference(Patient)
* specimen MS
* component[gene-studied] 1..* MS
* component[gene-studied] ^short = "studerad_gen (openEHR: Transcript/Gene/Gene symbol)"
* component[representative-coding-hgvs] 1..1 MS
* component[representative-coding-hgvs] ^short = "dna_förändring (openEHR: Transcript/DNA change)"
* component[representative-protein-hgvs] MS
* component[representative-protein-hgvs] ^short = "protein_förändring (openEHR: Transcript/Amino acid change)"
* component[genomic-source-class] MS
* component[genomic-source-class].value[x] from GeneticOriginSEVS (required)
* component[genomic-source-class] ^short = "genetiskt_ursprung (openEHR: Genetic origin)"
* component[sample-allelic-frequency] MS
* component contains
    molecular-consequence 0..1 MS and
    asco-amp-tier 0..1 MS and
    escat-tier 0..1 MS
* component[molecular-consequence].code = $TBD#feature-consequence
* component[molecular-consequence].value[x] only CodeableConcept
* component[molecular-consequence].value[x] from MolecularConsequenceSEVS (extensible)
* component[molecular-consequence] ^short = "molecular_consequence, Sequence Ontology (openEHR: Molecular consequence)"
* component[asco-amp-tier].code = $LNC#53037-8
* component[asco-amp-tier].value[x] only CodeableConcept
* component[asco-amp-tier].value[x] from AscoAmpTierVS (required)
* component[asco-amp-tier] ^short = "klinisk_signifikans_asco (openEHR: ASCO/AMP clinical significance tier)"
* component[escat-tier].code = $LNC#93044-6
* component[escat-tier].value[x] only CodeableConcept
* component[escat-tier].value[x] from EscatTierVS (required)
* component[escat-tier] ^short = "behandlingsrelevans_escat (openEHR: ESCAT therapeutic relevance)"
