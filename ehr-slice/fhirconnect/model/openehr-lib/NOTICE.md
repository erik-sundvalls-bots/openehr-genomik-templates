# Upstream model mappings (unchanged)

These FHIRconnect **model mappings** are copied unchanged from the official FHIRconnect
mapping library, <https://github.com/SevKohler/FHIRconnect-mapping-lib> (commit `6d5e66c82197654a40089d56dc39546e84ea9904`),
licensed under Apache-2.0 (see `LICENSE`). They map international CKM archetypes to base
FHIR R4 resources and are reused as-is; everything genomics- or Sweden-specific is in
`../local/` and `../../projects/se-genomics/` as *extension* and *context* mappings.
This reuse of the archetype-level layer is the main point of the FHIRconnect design.
