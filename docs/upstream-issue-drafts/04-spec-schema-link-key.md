# Draft issue
- Target: https://github.com/SevKohler/FHIRconnect-spec/issues
- Title: JSON Schema does not allow the `link` key used by the mapping library
- Related: https://github.com/SevKohler/FHIRconnect-spec/issues/85 (what should a LINK mapping output).

## Context
`laboratory_test_result.v1.yml` in FHIRconnect-mapping-lib uses:
```yaml
              - name: basedOnLink
                with:
                  fhir: $fhirRoot
                  openehr: $archetype/protocol[at0004]/items[at0094]/items[at0063]/links
                link:
                  meaning: the identifier which it derived from
                  type: based on
```
Validating against the JSON Schemas in `modules/ROOT/attachments` (commit e5871641) reports `link` as an unknown property.

## Expected
Either the schema defines `link` (with `meaning`, `type`), or the library stops using it.

## Actual
Schema validation fails/warns for valid-in-practice library files.
