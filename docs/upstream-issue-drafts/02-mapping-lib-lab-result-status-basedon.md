# Draft issue
- Target: https://github.com/SevKohler/FHIRconnect-mapping-lib/issues
- Title: laboratory_test_result.v1: status always comes back as `unknown`; `basedOn` emits an empty CarePlan
- Related: https://github.com/openFHIR/openfhir/issues/88 (toFHIR ignores openehrCondition in manual coded mappings, emits the last branch) – may be the engine-side cause; https://github.com/SevKohler/FHIRconnect-mapping-lib/issues/13.

## Context
In `laboratory_test_result.v1.yml` (commit 6d5e66c8) the `unknown` status entry uses a non-path `targetRoot`:
```yaml
            - name: unknown
              openehrCondition:
                targetRoot: null_flavour/defining_code/code_string
                targetAttribute: value
                operator: one of
                criteria: "253"
```
Other entries use a path root plus `targetAttribute`. Together with the manual entries not being matched per element, every report status came out as `unknown`.

`basedOn`:
```yaml
        - name: basedOn
          with:
            fhir: basedOn.as(Reference)
            openehr: $archetype
          followedBy: ...identifier / link
```
produces a contained/empty CarePlan reference when only an identifier is present.

## Repro
DiagnosticReport with `status: final` and `basedOn.identifier` → openEHR → FHIR.

## Expected
`status: final`, `basedOn: { identifier: ... }` (logical reference).

## Actual
`status: unknown`; `basedOn` references an empty CarePlan.

## Versions
FHIRconnect v1.0.0 files, openFHIR 3.0.2.

## Workaround
Override `status` and `basedOn` in an extension mapping (explicit `targetRoot` path + per-code entries; identifier-only reference).
