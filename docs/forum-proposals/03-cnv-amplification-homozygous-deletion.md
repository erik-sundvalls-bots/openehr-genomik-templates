# Proposal: Extend CNV Copy number change type beyond Gain/Loss

**Status:** Draft for Erik to post — **not posted**.  
**Date:** 2026-10-15 (Europe/Stockholm)  
**Related local draft:** `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_copy_number_variant-cancer.v1.0.0.adls`

## Problem
`CLUSTER.genomic_copy_number_variant.v1` value set for Copy number change type (`ac9001`) members are only:

- **Gain** (`at7`)
- **Loss** (`at8`)

Swedish underlag `kopietaltyp` and Sequence Ontology practice also need:

| Category | SO | Clinical examples |
|----------|-----|-------------------|
| Gain | SO:0001742 | Polysomy, low-level gain |
| Loss | SO:0001743 | Heterozygous deletion |
| **Amplification** | SO:0001742 (high-level) | ERBB2, MYC amp |
| **Homozygous deletion** | SO:0002210 | CDKN2A hom del |

Parent archetype comment explicitly says finer impact (e.g. low-level amplification, whole-gene deletion) should go to **Functional impact** on `genomic_variant_result`. That works for narrative but fails coded national reporting and clean FHIR `copy-number-change-type` mapping.

## Proposed change
Extend `ac9001` (or specialised `ac9001.1`) with:

```
at0.1 Amplification
at0.2 Homozygous deletion
```

Members: `at7, at8, at0.1, at0.2`.

## Alternatives
1. Keep parent Gain/Loss; encode amp/hom-del only in Functional impact / Additional details.
2. Specialisation (our local draft) for cancer CNV.
3. Upstream extension of the published CNV archetype (preferred for interoperability).

## FHIR alignment
`Observation.component:copy-number-change-type` with SO codes.

## Ask
Should Amplification and Homozygous deletion become first-class members of Copy number change type in CKM?
