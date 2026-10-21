# Draft issue
- Target: https://github.com/SevKohler/FHIRconnect-mapping-lib/issues
- Title: service_request.v1: requester mapped to non-existent `$composition/provider`
- Duplicates/related: none found (searched "provider").

## Context
Model mapping `service_request.v1.yml` (commit 6d5e66c8) maps `ServiceRequest.requester`:
```yaml
  - name: provider
    with:
      fhir: $resource.requester
      openehr: $composition/provider
```
`COMPOSITION` has no `provider` attribute in the openEHR RM (`provider` exists on `ENTRY`/CARE_ENTRY instead).

## Expected
Map to an existing RM path, e.g. `$archetype/provider` (ENTRY.provider) or `$composition/composer`, per the mapping's intent.

## Actual
The path cannot be resolved; with openFHIR 3.0.2 the requester is not mapped, so `ServiceRequest.requester` is lost on round-trip.

## Versions
FHIRconnect v1.0.0 files, openFHIR 3.0.2.

## Workaround
Override the entry with an empty/neutral mapping in an extension mapping.
