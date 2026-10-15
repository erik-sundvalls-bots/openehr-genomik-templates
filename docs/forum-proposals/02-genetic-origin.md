# Proposal: Explicit Genetic origin element on `CLUSTER.genomic_variant_result`

**Status:** Draft for Erik to post — **not posted**.  
**Date:** 2026-10-15 (Europe/Stockholm)  
**Related local draft:** `archetypes/drafts/openEHR-EHR-CLUSTER.genomic_variant_result-cancer.v1.0.0.adls` (`id0.1`)

## Problem
RCC variable `genetiskt_ursprung` (somatic / germline / likely_somatic / likely_germline / unknown) has **no dedicated element** in `genomic_variant_result.v1`.

Workarounds today:
- **Allelic state** (`id41`) — zygosity concepts, not origin.
- **Additional details** slot (`id99`) — unconstrained; poor interoperability.

## Proposed element

```
ELEMENT Genetic origin  (occurrences 0..1)
  value: DV_CODED_TEXT | DV_TEXT
  local value set: somatic | germline | likely_somatic | likely_germline | unknown
```

Bindings (preferred):
- SNOMED CT `719428005` (somatic), `261101003` (germline) where available
- HL7 Genomics allele-origin codes for likely_* / unknown

## FHIR alignment
`Observation.component:genomic-allele-origin` in FHIR Genomics Reporting IG.

## Ask
Add optional Genetic origin to the published parent archetype (or confirm specialisation is the intended path).
