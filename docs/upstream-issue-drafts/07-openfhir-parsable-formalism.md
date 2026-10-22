# Draft issue
- Target: https://github.com/openFHIR/openfhir/issues
- Title: DV_PARSABLE `formalism` always written as `text/html`; mapped formalism ignored
- Related: https://github.com/openFHIR/openfhir/pull/74 (parsable support).

## Repro
Map an HGVS string (`valueCodeableConcept.coding` with system http://varnomen.hgvs.org) to a DV_PARSABLE element and set a manual/fixed `formalism` (e.g. `HGVS`).

## Expected
`formalism` = mapped value.

## Actual
`formalism` = `text/html`, the manual value is dropped.

## Version
openFHIR 3.0.2.
