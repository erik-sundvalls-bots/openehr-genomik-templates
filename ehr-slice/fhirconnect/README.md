# fhirconnect

FHIRconnect mappings (grammar `FHIRConnect/v1.0.0`) loaded into the engine by `../engine/bootstrap.sh`.

- `model/openehr-lib/`: 8 model mappings copied unchanged from the FHIRconnect mapping library (Apache-2.0; commit and licence in `NOTICE.md`, `LICENSE`).
- `model/local/`, `projects/se-genomics/{request,report}/`: our own mappings for the genomics variant archetype and the context and extension mappings of the genomics request and genomics cancer report templates. **Generated** from `../tools/fhirconnect-src/` by `../tools/gen_fhirconnect.py`; edit the source, not these files.
- Checked by `../tools/validate_fhirconnect.py` against the FHIRconnect JSON Schemas.
