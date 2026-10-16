# Draft (not posted): Swedish translations and study elements for CKM genomics archetypes

*Draft for Erik Sundvall to post on CKM (translation proposals / archetype change requests). Nothing has been submitted.*

## 1. Swedish translations (CKM translation proposals)

Local draft Swedish translations were added to the ADL2 copies in `archetypes/ckm-adl2/` for the ten CKM archetypes used by the genomics templates that lacked `sv`. Source texts (term text + description per code, plus purpose) are in `translations/sv/<concept>.json`; `tools/add_sv_translation.py` injects them. Translator recorded as Erik Sundvall with accreditation "Local draft translation, not CKM-reviewed".

| CKM archetype | Revision used | Terms translated (all, incl. synthesised value-set labels) |
|---|---|---|
| CLUSTER.genomic_variant_result.v1 | 1.1.1 | 78 |
| CLUSTER.sequencing_assay.v0 | 0.0.1-alpha | 46 (incl. 24 chromosome labels) |
| CLUSTER.specimen_processing.v1 | 1.0.1 | 13 |
| CLUSTER.genomic_copy_number_variant.v1 | 1.1.0 | 10 |
| CLUSTER.genetic_variant_presence.v0 | 0.0.1-alpha | 9 |
| CLUSTER.translocation_variant.v0 | 0.0.1-alpha | 8 |
| CLUSTER.genomic_deletion_insertion_variant.v1 | 1.0.3 | 6 |
| CLUSTER.genomic_deletion_variant.v1 | 1.0.3 | 5 |
| CLUSTER.genomic_insertion_variant.v1 | 1.0.3 | 5 |
| CLUSTER.genomic_substitution_variant.v1 | 1.0.4 | 5 |

Not translated (not used in T1/T2): `genomic_duplication_variant.v1`, `genomic_inversion_variant.v1`, `knowledge_base_reference.v1`.

Suggested post text (CKM translation discussion):

> I have prepared Swedish translations of the genomics CLUSTER archetypes listed above (term texts, descriptions and purpose). They are drafts from a cancer-genomics template project and need review by a Swedish clinical geneticist/molecular pathologist before upload. Points where reviewer input is especially welcome: "Allelic state" → "Allelstatus", "Predicted impact" → "Predicerad påverkan", "No call" → "Ingen bestämning", "Copy number change type" Gain/Loss → "Ökning"/"Förlust". Could a translation task be opened for each archetype so the texts can be entered in CKM?

Use/misuse/keywords were not translated; only purpose was. CKM reviewers should complete them.

## 2. Change request: CLUSTER.sequencing_assay — study identifier and study type

Gap found in the Swedish genomics configuration (variables `studie_id`, `analystyp`). FHIR Genomics Reporting IG v3 has `GenomicStudy.identifier`, `GenomicStudy.type` (genomic-study-type CS) and `GenomicStudy.analysis.methodType` (genomic-study-method-type CS). `sequencing_assay` has none of these as dedicated elements.

Local solution: `archetypes/drafts/openEHR-EHR-CLUSTER.sequencing_assay-genomic_study.v0.0.1.adls` adds
- `Study identifier` (DV_IDENTIFIER, 0..1)
- `Study type` (DV_CODED_TEXT, 0..*, 12 HL7 genomic-study-type codes)
- a coded alternative for `Sequencing type` (9 HL7 genomic-study-method-type codes).

Suggested post text:

> For mapping to FHIR GenomicStudy we need a study identifier and a coded study type (SNP/CNV/structural variant detection etc.) on CLUSTER.sequencing_assay. Would the editors consider adding "Study identifier" (DV_IDENTIFIER) and "Study type" (DV_TEXT with suggested binding to the HL7 genomic-study-type code system), and a suggested terminology binding for "Sequencing type" to genomic-study-method-type? A local specialisation implementing this is available for reference.

## 3. Observation: CLUSTER.reference_sequence.v1 root node code

The ADL 1.4 CKM file uses `at0018` as root node code. Converted to ADL2 this gives root `id19`, which ADL2 validators reject (VARCN: root must be `id1`). The local ADL2 copy renames the root to `id1`. Worth reporting so the CKM ADL2 export (or the archetype) uses `at0000` as root.
