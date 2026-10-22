# tools

Generators and checks for the EHR Slice (run from anywhere; see `../README.md` for the order).

- `code_tables.py`: single table of local openEHR at-code ↔ FHIR code pairs.
- `gen_terminology_fsh.py`: writes `../ig/input/fsh/terminology.fsh` from the code tables.
- `gen_fhirconnect.py`: expands the code-mapping markers in `fhirconnect-src/` into `../fhirconnect/`. `fhirconnect-src/` is the hand-written source; no README is kept there because every file in it is copied to `../fhirconnect/`.
- `validate_fhirconnect.py`: checks `../fhirconnect/` against the JSON Schemas in `schema/` (copied from the FHIRconnect specification, see `schema/SOURCE.md`) plus cross-references. Needs `pyyaml`, `jsonschema`.
- `make_bundles.py`: builds `../examples/fhir/` from SUSHI output.
- `gen_ig_artefacts.py`: packages OPT, ADL2 and FHIRconnect files as IG `Binary` resources and a `Library` manifest.
