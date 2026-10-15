# Proposal: Modelling diagnostic & therapeutic implications for genomic variants

**Status:** Draft for Erik to post — **not posted**.  
**Date:** 2026-10-15 (Europe/Stockholm)  
**Related local draft:** `archetypes/drafts/openEHR-EHR-CLUSTER.variant_clinical_implication.v1.0.0.adls`

## Problem
FHIR Genomics IG uses **separate Observations** for DiagnosticImplication and TherapeuticImplication (with their own identifier and status). RCC underlaget has blocks `DIAGNOSTISK IMPLIKATION` and `TERAPEUTISK IMPLIKATION` with `impl_*_id`, status, and links to variants.

openEHR has no published implication archetype. Options:

| Option | Pros | Cons |
|--------|------|------|
| A. CLUSTER under each variant (slot) | Simple nesting; travels with the variant | Weaker 1:n FHIR Observation identity |
| B. Separate EVALUATION entries | Clear clinical assessment semantics | Heavier; needs linking to variant |
| C. Free text in Functional impact / Additional details | Zero new artefacts | No structure, poor FHIR mapping |

## Local recommendation (Phase 2)
**Option A** for v1 templates: new `CLUSTER.variant_clinical_implication` slotted under `genomic_variant_result-cancer`, with:

| Element | Type | FHIR |
|---------|------|------|
| Implication identifier | DV_IDENTIFIER | Observation.identifier |
| Implication type | DV_CODED_TEXT (diagnostic \| therapeutic) | profile / category |
| Status | DV_CODED_TEXT | Observation.status |
| Summary | DV_TEXT | Observation.value / note |
| Related therapy or finding | DV_TEXT / DV_CODED_TEXT | component / derivedFrom target |
| Linked variant reference | DV_URI / DV_IDENTIFIER | derivedFrom |

ASCO/ESCAT stay on the **variant** specialisation (not inside implication), because they classify the variant itself; implications then reference therapies/findings.

## Ask
1. Prefer CLUSTER-under-variant vs EVALUATION for CKM Genomics?
2. Interest in co-authoring a shared `variant_clinical_implication` CLUSTER?
