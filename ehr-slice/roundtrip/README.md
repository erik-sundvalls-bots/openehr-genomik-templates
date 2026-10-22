# roundtrip

FHIR → openEHR → FHIR → openEHR round-trip through a running openFHIR engine (`../engine/`).

- `run.sh`: posts `../examples/fhir/*.json` to the engine, writes compositions to `../examples/openehr/` and raw responses to `out/`, then runs `compare.py`.
- `compare.py`: compares input and output field by field and writes `RESULTS.md`.
- `out/`: raw engine responses (Parameters/Bundle JSON) from the last run.
