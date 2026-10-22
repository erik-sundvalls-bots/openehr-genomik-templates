# examples

- `fhir/`: FHIR input Bundles for the genomics cancer report (`T1-report-bundle.json`) and the genomics request (`T2-request-bundle.json`), assembled by `../tools/make_bundles.py` from the SUSHI-built IG examples (`../ig/fsh-generated/resources/`). Demo data.
- `openehr/`: the compositions openFHIR produced from those Bundles, in flat and canonical JSON, written by `../roundtrip/run.sh`.
