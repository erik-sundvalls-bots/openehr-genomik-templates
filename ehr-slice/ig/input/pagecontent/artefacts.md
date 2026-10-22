### openEHR templates / openEHR-templates

The templates are included as [Binary](artifacts.html) resources and listed in the
[EHR Slice manifest](Library-ehr-slice-manifest.html) (a `Library` of type *asset-collection*).

| Template | ADL2 (source) | OPT 1.4 (operational, used by the mapping engine) |
|---|---|---|
| Genomics request (T2) | [adls](Binary-adl2-openEHR-EHR-COMPOSITION.t-genomics-request.v1.0.0.adls.html) | [opt](Binary-opt-openEHR-EHR-COMPOSITION.t-genomics-request.opt.html) |
| Genomics cancer report (T1) | [adls](Binary-adl2-openEHR-EHR-COMPOSITION.t-genomics-cancer-report.v-306ee6ab.html) | [opt](Binary-opt-openEHR-EHR-COMPOSITION.t-genomics-cancer-report.opt.html) |

### FHIRconnect mappings / FHIRconnect-mappningar

The mappings follow the published FHIRconnect specification (grammar `FHIRConnect/v1.0.0`) and its
layered structure:

- **model** mappings: one archetype ↔ one FHIR resource, reusable across projects. Eight are reused
  unchanged from the open FHIRconnect mapping library (Apache-2.0); one is new
  (`CLUSTER.genomic_variant_result-cancer.v1` ↔ variant Observation).
- **extension** mappings: project-specific additions and overrides (Swedish code lists, the
  performing/receiving laboratory, genomics report codes, fixes for three upstream issues).
- **context** mappings: bind one FHIR profile to one openEHR template and list the model and
  extension mappings to use.

Local openEHR codes (at-codes) are translated to FHIR codes with explicit per-code tables
generated from one source (`ehr-slice/tools/code_tables.py`), so the same table drives the
FHIR CodeSystems/ValueSets in this guide and both directions of the mapping.

| Direction | Context | Extensions | Models |
|---|---|---|---|
| T2 ↔ ServiceRequest (+ Condition, Organization) | [request context](Binary-fc-se-genomics-request.context.yaml.html) | [service request](Binary-fc-se-genomics-service-request.yml.html), [referring diagnosis](Binary-fc-se-genomics-referring-diagnosis.yml.html) | service_request, request composition, organisation, problem_diagnosis |
| T1 ↔ DiagnosticReport (+ variant Observations, Specimen, Organization) | [report context](Binary-fc-se-genomics-report.context.yaml.html) | [genomic report](Binary-fc-se-genomic-report.yml.html), [specimen](Binary-fc-se-genomics-specimen.yml.html) | laboratory_test_result, report composition, specimen, organisation, [genomic variant result (new)](Binary-fc-genomic-variant-result-cancer.v1.yml.html) |
