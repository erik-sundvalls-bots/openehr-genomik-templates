# Variable inventory — Konfigurationsunderlag genomik → openEHR

Total clinical/data variables: **73** (block headers excluded).

## Gap flags

*Updated 2026-10-16: studie_id/analystyp/analysmetod via `sequencing_assay-genomic_study` draft; value sets bound in T1/T2 overlays.*

- `covered`: 40
- `partial`: 22
- `covered_by_local_draft`: 7 (draft specialisations in `archetypes/drafts/`)
- `gap`: 0
- `out_of_scope_demographics`: 4

## Variables per proposed archetype (primary)

- 18  `openEHR-EHR-CLUSTER.genomic_variant_result.v1`
-  8  `openEHR-EHR-CLUSTER.specimen.v1`
-  7  `openEHR-EHR-CLUSTER.laboratory_test_analyte.v1`
-  7  `openEHR-EHR-OBSERVATION.laboratory_test_result.v1`
-  5  `openEHR-EHR-CLUSTER.organisation.v1`
-  4  `openEHR-EHR-CLUSTER.sequencing_assay.v0`
-  2  `openEHR-EHR-INSTRUCTION.service_request.v1`
-  2  `openEHR-EHR-EVALUATION.problem_diagnosis.v1`
-  2  `openEHR-EHR-CLUSTER.anatomical_location.v1`
-  2  `COMPOSITION.subject`
-  2  `openEHR-EHR-CLUSTER.genomic_copy_number_variant.v1`
-  1  `EHR subject / demographics`
-  1  `EHR subject identifier`
-  1  `openEHR-EHR-CLUSTER.specimen_processing.v1`
-  1  `openEHR-EHR-CLUSTER.sequencing_assay.v0 / lab_result`
-  1  `openEHR-EHR-CLUSTER.device.v1 via openEHR-EHR-CLUSTER.sequencing_assay.v0`
-  1  `openEHR-EHR-OBSERVATION.laboratory_test_result.v1 / analyte`
-  1  `openEHR-EHR-CLUSTER.genetic_variant_presence.v0`
-  1  `openEHR-EHR-CLUSTER.genomic_variant_result.v1 Structured variant choice`
-  1  `Separate EVALUATION or linked OBSERVATION`
-  1  `Same entry status`
-  1  `LINK to variant CLUSTER/entry`
-  1  `Therapeutic implication entry`
-  1  `LINK to variant`
-  1  `LINKs to contributing variants`

## Full table

| Block | Variable | Card. | Datatype | openEHR archetype | Path / element | RM type | Gap |
|---|---|---|---|---|---|---|---|
| PATIENT | `patient_id` | 1..1 | UUID | EHR subject / demographics | subject (COMPOSITION) | PARTY_PROXY | out_of_scope_demographics |
| PATIENT | `personnummer` | 1..1 | String | EHR subject identifier | subject.identifiers | DV_IDENTIFIER | out_of_scope_demographics |
| ORGANISATION | `organisation_id` | 1..1 | UUID | openEHR-EHR-CLUSTER.organisation.v1 | /items[at0001] Identifier (or COMPOSITION.composer | DV_IDENTIFIER | covered |
| ORGANISATION | `hsa_id` | 0..1 | String | openEHR-EHR-CLUSTER.organisation.v1 | /items[at0001] Identifier (type=HSA) | DV_IDENTIFIER | covered |
| ORGANISATION | `enhet_hsa_id` | 0..1 | String | openEHR-EHR-CLUSTER.organisation.v1 | partOf / nested organisation | DV_IDENTIFIER | partial |
| REMISS | `remiss_id` | 1..1 | UUID | openEHR-EHR-INSTRUCTION.service_request.v1 | INSTRUCTION.uid / protocol identifiers; also lab_r | DV_IDENTIFIER | covered |
| REMISS | `diagnos` | 1..1 | Code | openEHR-EHR-EVALUATION.problem_diagnosis.v1 | /data[at0001]/items[at0002] Problem/Diagnosis name | DV_CODED_TEXT | covered |
| REMISS | `frågeställning` | 1..* | Code | openEHR-EHR-INSTRUCTION.service_request.v1 | Service name / Reason for request (coded) | DV_CODED_TEXT | partial |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `prov_id` | 1..1 | Identifier | openEHR-EHR-CLUSTER.specimen.v1 | /items[at0001] Laboratory specimen identifier OR / | DV_IDENTIFIER | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `pad_nummer` | 1..1 | Identifier | openEHR-EHR-CLUSTER.specimen.v1 | /items[at0001] Laboratory specimen identifier (PAD | DV_IDENTIFIER | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `provtyp` | 1..1 | Code | openEHR-EHR-CLUSTER.specimen.v1 | /items[at0029] Specimen type | DV_CODED_TEXT | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `fixeringsmetod` | 0..1 | Code | openEHR-EHR-CLUSTER.specimen_processing.v1 | Processing details / processing procedure (in spec | DV_CODED_TEXT | partial |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `provtagningsteknik` | 0..1 | Code | openEHR-EHR-CLUSTER.specimen.v1 | /items[at0007] Collection method | DV_CODED_TEXT | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `provtagningsdatum` | 1..1 | Date | openEHR-EHR-CLUSTER.specimen.v1 | /items[at0015] Collection date/time | DV_DATE_TIME | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `kropplats` | 0..1 | Code | openEHR-EHR-CLUSTER.anatomical_location.v1 | specimen /items[at0013] Structured source site → a | DV_CODED_TEXT | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `lateralitet` | 0..1 | Code | openEHR-EHR-CLUSTER.anatomical_location.v1 | anatomical_location Laterality | DV_CODED_TEXT | covered |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `tumörcellshalt_patolog` | 0..1 | Decimal | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 OR specimen A | Analyte name=tumour cellularity (pathologist); res | DV_PROPORTION | partial |
| PROVMATERIAL - NIVÅ 1 (Ursprungsprov) | `tumörcellshalt_bioinformatisk` | 0..1 | Decimal | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Separate analyte result (bioinformatic tumour frac | DV_PROPORTION | partial |
| PROVMATERIAL - NIVÅ 2 (Extraherat materi | `extraherat_prov_id` | 1..1 | Identifier | openEHR-EHR-CLUSTER.specimen.v1 | Child specimen; /items[at0003] Parent specimen ide | DV_IDENTIFIER | covered |
| PROVMATERIAL - NIVÅ 2 (Extraherat materi | `extraherat_material` | 1..1 | Code | openEHR-EHR-CLUSTER.specimen.v1 + openEHR-EHR-CLUSTER.sequen | Child Specimen type OR sequencing_assay Nucleic ac | DV_CODED_TEXT | covered |
| DIAGNOSTISK RAPPORT | `rapport_id` | 1..1 | Identifier | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | /protocol[at0004]/items[at0068] Laboratory interna | DV_IDENTIFIER | covered |
| DIAGNOSTISK RAPPORT | `rapport_status` | 1..1 | Code | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | /data…/items[at0073] Overall test status | DV_CODED_TEXT | covered |
| DIAGNOSTISK RAPPORT | `rapport_typ` | 1..1 | CodeableConcept | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | /data…/items[at0005] Test name | DV_CODED_TEXT | covered |
| DIAGNOSTISK RAPPORT | `patient_ref` | 1..1 | Reference | COMPOSITION.subject | subject | PARTY_PROXY | out_of_scope_demographics |
| DIAGNOSTISK RAPPORT | `analysdatum` | 1..1 | DateTime | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | EVENT time / Analysis performed time on analyte | DV_DATE_TIME | covered |
| DIAGNOSTISK RAPPORT | `svarsdatum` | 1..1 | Instant | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | COMPOSITION.context.start_time / Overall test stat | DV_DATE_TIME | covered |
| DIAGNOSTISK RAPPORT | `laboratorium_ref` | 1..* | Reference | openEHR-EHR-CLUSTER.organisation.v1 | lab_result protocol Receiving laboratory at0017 OR | CLUSTER.organisation | covered |
| DIAGNOSTISK RAPPORT | `prover_ref` | 0..* | Reference | openEHR-EHR-CLUSTER.specimen.v1 | Nested specimen clusters (not FHIR refs) | CLUSTER | covered |
| DIAGNOSTISK RAPPORT | `fynd_ref` | 0..* | Reference | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Multiple genomic_variant_result in Test result slo | CLUSTER | covered |
| DIAGNOSTISK RAPPORT | `remiss_ref` | 1..* | Reference | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | protocol Test request details / Requester order id | DV_IDENTIFIER / LINK | covered |
| DIAGNOSTISK RAPPORT | `studiemetadata_ref` | 0..1 | Reference | openEHR-EHR-CLUSTER.sequencing_assay.v0 | protocol Testing details at0110 → sequencing_assay | CLUSTER | partial |
| STUDIEMETADATA (GenomicStudy) | `studie_id` | 1..1 | Identifier | openEHR-EHR-CLUSTER.sequencing_assay.v0 | Identifier via device/assay Extensions or lab inte | DV_IDENTIFIER | gap |
| STUDIEMETADATA (GenomicStudy) | `studie_status` | 1..1 | Code | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 | Overall test status (study-level) | DV_CODED_TEXT | partial |
| STUDIEMETADATA (GenomicStudy) | `sekvenseringsdatum` | 1..1 | Date | openEHR-EHR-CLUSTER.sequencing_assay.v0 / lab_result | EVENT time or Extension | DV_DATE_TIME | partial |
| STUDIEMETADATA (GenomicStudy) | `klinisk_kontext_ref` | 0..* | Reference | openEHR-EHR-EVALUATION.problem_diagnosis.v1 | LINK / reason; or Clinical information provided | LINK / DV_TEXT | partial |
| STUDIEMETADATA (GenomicStudy) | `analysmetod` | 1..1 | Code | openEHR-EHR-CLUSTER.sequencing_assay.v0 | /items[at0001] Sequencing type | DV_CODED_TEXT | partial |
| STUDIEMETADATA (GenomicStudy) | `analystyp` | 1..1 | Code | openEHR-EHR-CLUSTER.sequencing_assay.v0 | Sequencing type / Extensions (snp/cnv/struc-var/fu | DV_CODED_TEXT | gap |
| DEVICE / PANEL | `panel_produktnamn` | 1..1 | String | openEHR-EHR-CLUSTER.device.v1 via openEHR-EHR-CLUSTER.sequen | sequencing_assay Kit name at0002 OR device Name | DV_TEXT | covered |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `fynd_id` | 1..1 | Identifier | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | ENTRY/CLUSTER identifier via feeder_audit or Addit | DV_IDENTIFIER | partial |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `fynd_status` | 1..1 | Code | openEHR-EHR-OBSERVATION.laboratory_test_result.v1 / analyte | Result status at0005 on containing analyte or over | DV_CODED_TEXT | partial |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `patient_ref` | 1..1 | Reference | COMPOSITION.subject | subject | PARTY_PROXY | out_of_scope_demographics |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `prov_ref` | 1..1 | Reference | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0070] Specimen identifier | DV_TEXT/IDENTIFIER | covered |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `laboratorium_ref` | 1..1 | Reference | openEHR-EHR-CLUSTER.organisation.v1 | performer / protocol | CLUSTER.organisation | covered |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `förekomst` | 1..1 | Code | openEHR-EHR-CLUSTER.genetic_variant_presence.v0 OR gvr Funct | Finding at0002 (Detected/Not detected) OR genotype | DV_CODED_TEXT | partial |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `genetiskt_ursprung` | 0..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Additional details OR Allelic state (imperfect) —  | DV_CODED_TEXT | gap |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `studerad_gen` | 1..* | CodeableConcept | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0019]/items[at0020] Gene symbol (+ Gene n | DV_TEXT / DV_CODED_TEXT | covered |
| VARIANT - GEMENSAMMA ATTRIBUT (alla fynd | `variationstyp` | 1..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 Structured var | Choice of genomic_*_variant archetype OR Additiona | DV_CODED_TEXT / archetype choice | partial |
| VARIANTFYND - SNV OCH INDEL | `dna_förändring` | 1..1 | String | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0011] DNA change (HGVS) and/or /items[at0 | DV_TEXT | covered |
| VARIANTFYND - SNV OCH INDEL | `protein_förändring` | 0..1 | String | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0012] Amino acid change | DV_TEXT | covered |
| VARIANTFYND - SNV OCH INDEL | `molecular_consequence` | 0..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0013] Amino acid change type (local codes | DV_CODED_TEXT | partial |
| VARIANTFYND - SNV OCH INDEL | `allelisk_frekvens` | 0..1 | Quantity | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0047] Allele frequency | DV_PROPORTION / DV_QUANTITY | covered |
| VARIANTFYND - SNV OCH INDEL | `exonnummer` | 0..1 | Integer | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | DNA region name / Fusion exon at0059 / Additional  | DV_COUNT / DV_TEXT | partial |
| CNV-FYND (Kopietalförändring) | `målregion_gen` | 1..1 | String | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Gene symbol at0020 | DV_TEXT | covered |
| CNV-FYND (Kopietalförändring) | `antal_kopior` | 1..1 | Decimal | openEHR-EHR-CLUSTER.genomic_copy_number_variant.v1 | /items[at0003] Total copy number | DV_COUNT / DV_QUANTITY | covered |
| CNV-FYND (Kopietalförändring) | `kopietaltyp` | 1..1 | Code | openEHR-EHR-CLUSTER.genomic_copy_number_variant.v1 + gvr Fun | /items[at0005] Copy number change type (Gain/Loss  | DV_CODED_TEXT | gap |
| CNV-FYND (Kopietalförändring) | `karyotyp_iscn` | 0..1 | String | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Additional details / Variant text | DV_TEXT | partial |
| FUSIONSFYND (Rearrangemang) | `fusionspartner_1` | 1..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 + openEHR-EHR- | Gene cluster ×2 with Part of fusion=First/Second;  | DV_CODED_TEXT | partial |
| FUSIONSFYND (Rearrangemang) | `fusionspartner_2` | 1..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Second Gene cluster, Part of fusion=Second | DV_CODED_TEXT | partial |
| FUSIONSFYND (Rearrangemang) | `karyotyp_iscn` | 0..1 | String | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Additional details / Variant text (ISCN) | DV_TEXT | partial |
| DIAGNOSTISK IMPLIKATION | `impl_diag_id` | 1..1 | Identifier | Separate EVALUATION or linked OBSERVATION | feeder_audit / uid | DV_IDENTIFIER | gap |
| DIAGNOSTISK IMPLIKATION | `impl_diag_status` | 1..1 | Code | Same entry status | Result status | DV_CODED_TEXT | gap |
| DIAGNOSTISK IMPLIKATION | `variant_ref` | 1..1 | Reference | LINK to variant CLUSTER/entry | LINKs | LINK | partial |
| DIAGNOSTISK IMPLIKATION | `patogenicitet` | 0..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | /items[at0058] ACMG classification | DV_CODED_TEXT | partial |
| DIAGNOSTISK IMPLIKATION | `klinisk_signifikans_asco` | 0..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Functional impact Impact at0054 OR Additional deta | DV_CODED_TEXT | gap |
| TERAPEUTISK IMPLIKATION | `impl_ter_id` | 1..1 | Identifier | Therapeutic implication entry | uid | DV_IDENTIFIER | gap |
| TERAPEUTISK IMPLIKATION | `variant_ref` | 1..1 | Reference | LINK to variant | LINKs | LINK | partial |
| TERAPEUTISK IMPLIKATION | `behandlingsrelevans_escat` | 0..1 | Code | openEHR-EHR-CLUSTER.genomic_variant_result.v1 | Functional impact / Additional details — ESCAT | DV_CODED_TEXT | gap |
| KOMPLEX BIOMARKÖR - TMB (Tumor Mutationa | `tmb_värde` | 1..1 | Quantity | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Analyte name=TMB; result DV_QUANTITY (mut/Mb) | DV_QUANTITY | covered |
| KOMPLEX BIOMARKÖR - TMB (Tumor Mutationa | `tmb_tolkning` | 1..1 | Code | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Result interpretation / comment coded | DV_CODED_TEXT | partial |
| KOMPLEX BIOMARKÖR - TMB (Tumor Mutationa | `tmb_variant_ref` | 1..* | Reference | LINKs to contributing variants | LINKs | LINK | partial |
| KOMPLEX BIOMARKÖR - MSI (Microsatellite  | `msi_status` | 1..1 | Code | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Analyte name=MSI; coded result (MSI-H/MSS/…) | DV_CODED_TEXT | covered |
| KOMPLEX BIOMARKÖR - HRD (Homologous Reco | `hrd_score` | 1..1 | Quantity | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Analyte name=HRD score; DV_QUANTITY | DV_QUANTITY | covered |
| KOMPLEX BIOMARKÖR - HRD (Homologous Reco | `hrd_tolkning` | 1..1 | Code | openEHR-EHR-CLUSTER.laboratory_test_analyte.v1 | Coded interpretation | DV_CODED_TEXT | partial |
