# tools

Build and helper scripts for the templates (the EHR Slice has its own `../ehr-slice/tools/`).

- `build.sh`: rebuilds everything in `../build/` (Archie validation, Ehrtslib OPT/OET 1.4 export, ADL 1.4 down-conversion with Ehrtslib and the Archie fork, XSD checks). Needs JDK 17, Deno and checkouts of Ehrtslib and the Archie fork (paths via `EHRTSLIB`, `ARCHIE`, `XSD`, `OET_XSD`).
- `ArchieValidateAll.java`: Archie parse + flatten + validate of all ADL2 files; `ArchieConvert.java` + `archie-pom.xml`: Archie helper (ADL 1.4 → ADL2 conversion, parse checks).
- `ehrtslib-down14.ts`: ADL2 → ADL 1.4 with Ehrtslib.
- `add_sv_translation.py`: adds the Swedish translations in `../translations/sv/` to `../archetypes/ckm-adl2/`.
- `bind_valuesets.py`: one-off helper that generated the value-set bindings in `../templates/adl2/` from `../valuesets/`.
