# Proposal: Add ASCO/AMP and ESCAT classification alongside ACMG in `CLUSTER.genomic_variant_result`

**Status:** Draft for Erik to post on openEHR Discourse / CKM Genomics project — **not posted**.  
**Date:** 2026-10-15 (Europe/Stockholm)  
**Related local draft:** `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adls`

## Problem
`CLUSTER.genomic_variant_result.v1` provides **ACMG classification** (`id59` / at0058) for germline pathogenicity. Swedish RCC *Konfigurationsunderlag genomik* and the [HL7 FHIR Genomics Reporting IG](http://hl7.org/fhir/uv/genomics-reporting/) also require:

| Need | FHIR Genomics IG | CKM today |
|------|------------------|-----------|
| Somatic clinical significance (ASCO/AMP/CAP Tier I–IV) | `Observation.component:somatic-clinical-significance` | **Missing** (CKM search 2026-10-15: 0 hits for ASCO/AMP/ESCAT) |
| Therapeutic actionability (ESCAT) | Often modelled via therapeutic implication / actionability | **Missing** |

GMS local prior art (`CLUSTER.mtbp_classification.v0`) only has a coarse three-level “variant relevance” scale — not ASCO or ESCAT.

ACMG and ASCO/AMP answer different clinical questions; they are **not interchangeable**.

## Proposed elements (ADL2 sketch)

```
ELEMENT[id0.2] ASCO/AMP clinical significance tier
  value: DV_CODED_TEXT  -- value set Tier I-A … Tier IV
ELEMENT[id0.3] ESCAT therapeutic relevance
  value: DV_CODED_TEXT  -- value set ESCAT Tier I-A … Tier X
```

Suggested placement: siblings of ACMG classification under the variant result cluster (same level as `id59`).

## Alternatives discussed
1. **Specialisation only** (what we draft locally) — fast for national use; delays international alignment.
2. **Extend parent CKM archetype** — preferred long-term; requires Genomics project consensus.
3. **Reuse Functional impact (`id53`/`id55`)** — currently `DV_TEXT`; too weak for coded national reporting and FHIR mapping.

## FHIR alignment
- ASCO/AMP → `Observation.component` code for somatic clinical significance (IG value set / local CS pending international URI).
- ESCAT → therapeutic actionability component or TherapeuticImplication Observation.

## Ask to the community
1. Is adding two optional coded ELEMENTs to `genomic_variant_result.v1` acceptable, or should they live in a cancer specialisation?
2. Preferred terminology URIs for ASCO/AMP and ESCAT once published?
