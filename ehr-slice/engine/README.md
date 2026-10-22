# engine

Local openFHIR set-up for the round-trip demo (openFHIR is an open-source FHIRconnect engine).

- `docker-compose.yml`: openFHIR 3.0.2 and MongoDB 7, both pinned by image digest.
- `bootstrap.sh`: copies the FHIRconnect mappings (`../fhirconnect/`) and OPT 1.4 files (`../../build/opt14/` via `../templates/opt14/`) into `bootstrap/` (git-ignored) and asks the running engine to load them.
