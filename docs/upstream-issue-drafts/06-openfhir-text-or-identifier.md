# Draft issue
- Target: https://github.com/openFHIR/openfhir/issues
- Title: toFHIR loses identifier when the openEHR element allows DV_TEXT or DV_IDENTIFIER and no `type` is given
- Related: https://github.com/openFHIR/openfhir/pull/109 (DV_IDENTIFIER handling in toOpenEHR).

## Repro
Element whose value is a choice of DV_TEXT | DV_IDENTIFIER (e.g. request identifier in service_request.v1), mapped to `identifier` without `type`. Composition holds a DV_IDENTIFIER.

## Expected
FHIR `identifier` with system/value, inferring the type from the data instance.

## Actual
Identifier is dropped on export unless the mapping states `type: IDENTIFIER`.

## Version
openFHIR 3.0.2. Workaround: add `type: IDENTIFIER`.
