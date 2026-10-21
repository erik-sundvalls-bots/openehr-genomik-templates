// Example instances (fictitious data). Used both as IG examples and as input to the
// openFHIR round-trip (see ehr-slice/roundtrip).

Instance: patient-demo-1
InstanceOf: http://hl7.se/fhir/ig/base/StructureDefinition/SEBasePatient
Title: "Demo patient"
Usage: #example
* identifier[personnummer].system = $PNR
* identifier[personnummer].value = "191212121212"
* name.family = "Testsson"
* name.given = "Tolvan"

Instance: lab-genomics-demo
InstanceOf: SEGenomicsLaboratory
Title: "Demo genomics laboratory"
Usage: #example
* identifier[hsaid].system = $HSA
* identifier[hsaid].value = "SE0000000000-GEN1"
* name = "Genomiklaboratoriet (demo)"

Instance: diagnosis-demo-1
InstanceOf: SEGenomicsReferringDiagnosis
Title: "Referring diagnosis – lung adenocarcinoma"
Usage: #example
* code = $ICD10#C34.1 "Malignant neoplasm: Upper lobe, bronchus or lung"
* code.text = "Malign tumör i övre loben, bronk eller lunga"
* subject = Reference(patient-demo-1)

Instance: servicerequest-demo-1
InstanceOf: SEGenomicsServiceRequest
Title: "Genomikremiss – NSCLC panel"
Usage: #example
* identifier.system = "https://example.org/fhir/ehr-slice-se-genomics/identifier/remiss"
* identifier.value = "REM-2026-000123"
* status = #active
* intent = #order
* code.text = "Solid tumour NGS panel (DNA)"
* subject = Reference(patient-demo-1)
* authoredOn = "2026-10-01T09:30:00+02:00"
* requester = Reference(practitioner-demo-1) "Remitterande läkare (demo)"
* reasonCode[0] = FragestallningCS#"1" "Primärdiagnostik"
* reasonCode[1] = FragestallningCS#"2" "Behandlingssvarsprediktion"
* reasonReference = Reference(diagnosis-demo-1)
* performer = Reference(lab-genomics-demo)

Instance: specimen-demo-1
InstanceOf: SEGenomicsSpecimen
Title: "Tumour tissue specimen (FFPE)"
Usage: #example
* identifier.system = "https://example.org/fhir/ehr-slice-se-genomics/identifier/pad"
* identifier.value = "PAD-2026-04567"
* type = $SCT#258435002 "Tumor"
* subject = Reference(patient-demo-1)
* collection.collectedDateTime = "2026-09-28T13:15:00+02:00"

Instance: variant-demo-egfr
InstanceOf: SEVariant
Title: "EGFR L858R (somatic)"
Usage: #example
* status = #final
* category[labCategory] = $OBSCAT#laboratory
* category[geCategory] = $V2-0074#GE
* code = $LNC#69548-6
* subject = Reference(patient-demo-1)
* specimen = Reference(specimen-demo-1)
* valueCodeableConcept = $LNC#LA9633-4 "Present"
* component[gene-studied].code = $LNC#48018-6
* component[gene-studied].valueCodeableConcept.text = "EGFR"
* component[representative-coding-hgvs].code = $LNC#48004-6
* component[representative-coding-hgvs].valueCodeableConcept = $HGVS#"NM_005228.5:c.2573T>G"
* component[representative-protein-hgvs].code = $LNC#48005-3
* component[representative-protein-hgvs].valueCodeableConcept = $HGVS#"NP_005219.2:p.(Leu858Arg)"
* component[genomic-source-class].code = $LNC#48002-0
* component[genomic-source-class].valueCodeableConcept = $LNC#LA6684-0 "Somatic"
* component[sample-allelic-frequency].code = $LNC#81258-6
* component[sample-allelic-frequency].valueQuantity = 0.32 '1' "1"
* component[molecular-consequence].valueCodeableConcept = $SO#"SO:0001583" "missense_variant"
* component[asco-amp-tier].valueCodeableConcept = AscoAmpTierCS#"Tier I-A"
* component[escat-tier].valueCodeableConcept = EscatTierCS#"Tier I-A"

Instance: variant-demo-tp53
InstanceOf: SEVariant
Title: "TP53 R273H (somatic)"
Usage: #example
* status = #final
* category[labCategory] = $OBSCAT#laboratory
* category[geCategory] = $V2-0074#GE
* code = $LNC#69548-6
* subject = Reference(patient-demo-1)
* specimen = Reference(specimen-demo-1)
* valueCodeableConcept = $LNC#LA9633-4 "Present"
* component[gene-studied].code = $LNC#48018-6
* component[gene-studied].valueCodeableConcept.text = "TP53"
* component[representative-coding-hgvs].code = $LNC#48004-6
* component[representative-coding-hgvs].valueCodeableConcept = $HGVS#"NM_000546.6:c.818G>A"
* component[representative-protein-hgvs].code = $LNC#48005-3
* component[representative-protein-hgvs].valueCodeableConcept = $HGVS#"NP_000537.3:p.(Arg273His)"
* component[genomic-source-class].code = $LNC#48002-0
* component[genomic-source-class].valueCodeableConcept = $LNC#LA6684-0 "Somatic"
* component[sample-allelic-frequency].code = $LNC#81258-6
* component[sample-allelic-frequency].valueQuantity = 0.18 '1' "1"
* component[molecular-consequence].valueCodeableConcept = $SO#"SO:0001583" "missense_variant"
* component[asco-amp-tier].valueCodeableConcept = AscoAmpTierCS#"Tier III"
* component[escat-tier].valueCodeableConcept = EscatTierCS#"Tier X"

Instance: genomic-report-demo-1
InstanceOf: SEGenomicReport
Title: "Genomic report – NSCLC panel"
Usage: #example
* identifier.system = "https://example.org/fhir/ehr-slice-se-genomics/identifier/labreport"
* identifier.value = "GEN-2026-000777"
* status = #final
* category[Genetics] = $V2-0074#GE
* code = $LNC#51969-4 "Genetic analysis report"
* code.text = "Solid tumour NGS panel (DNA)"
* subject = Reference(patient-demo-1)
* effectiveDateTime = "2026-10-05T10:00:00+02:00"
* issued = "2026-10-06T14:00:00+02:00"
* performer = Reference(lab-genomics-demo)
* specimen = Reference(specimen-demo-1)
* basedOn = Reference(servicerequest-demo-1)
* basedOn.identifier.system = "https://example.org/fhir/ehr-slice-se-genomics/identifier/remiss"
* basedOn.identifier.value = "REM-2026-000123"
* result[variant][0] = Reference(variant-demo-egfr)
* result[variant][1] = Reference(variant-demo-tp53)
* conclusion = "EGFR L858R påvisad (Tier I-A / ESCAT I-A). TP53 R273H påvisad."

Instance: practitioner-demo-1
InstanceOf: Practitioner
Title: "Requesting physician (demo)"
Usage: #example
* name.text = "Remitterande läkare (demo)"
