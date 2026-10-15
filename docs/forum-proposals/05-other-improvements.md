# Proposal: Other genomic_variant_result improvements (exon, ISCN, SO molecular consequence)

**Status:** Draft for Erik to post — **not posted**.  
**Date:** 2026-10-15 (Europe/Stockholm)  
**Related local draft:** `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adls`

## Gaps / partial mappings from Swedish inventory

| Variable | Today in CKM | Proposal |
|----------|--------------|----------|
| `exonnummer` | Only **Fusion exon** (`id60`); DNA region name is free text | Add general **Exon number** (`DV_COUNT` \| `DV_TEXT`) |
| `karyotyp_iscn` | No dedicated element | Add **Karyotype (ISCN)** (`DV_TEXT`) |
| `molecular_consequence` | Amino acid change type is local/coded but not SO molecular consequence | Add **Molecular consequence** bound to Sequence Ontology |

## FHIR alignment
- Molecular consequence → `Observation.component:molecular-consequence` (SO)
- ISCN → often carried as variant text / component; explicit ELEMENT improves AQL
- Exon → common annotation in VCF/HGVS pipelines; Fusion exon remains for fusion context

## Sequencing study metadata (related)
`studie_id` / `analystyp` map poorly onto draft `CLUSTER.sequencing_assay.v0`. Separate forum thread may be needed once that archetype advances past TEAMREVIEW.

## Ask
Accept these three optional ELEMENTs into parent `genomic_variant_result` or endorse cancer specialisation for them.
