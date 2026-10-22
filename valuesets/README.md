# valuesets

The dataset's value lists (*Listvärden* sheets of `../source/xlsx/`).

- `Listvärden_*.csv`: the sheets as exported (same as `../source/csv/`).
- `<name>.json`: each list as structured JSON: variable, FHIR target, code systems and codes with English/Swedish display. Generating script not committed; later edits (e.g. frågeställning, SO URIs) are recorded in `../docs/decisions.md`.
- `valuesets.json`: code-system URIs used across the lists (SNOMED CT, Sequence Ontology, HL7 genomics code systems, local systems).

Used by `../tools/bind_valuesets.py` (ADL2 template bindings) and read by `../ehr-slice/tools/code_tables.py` (`valuesets.json`).
