# Draft issue
- Target: https://github.com/openFHIR/openfhir/issues
- Title: Profile URL in `fhirConfig.structureDefinition` silently disables the model mapping
- Duplicates: none found.

## Repro
```yaml
spec:
  fhirConfig:
    structureDefinition: https://example.org/fhir/StructureDefinition/my-servicerequest
```
## Expected
Mapping applies to resources claiming that profile (or to the base type), or the engine reports an error.

## Actual
No mapping is applied and no error/warning is logged. Only the base URL (`http://hl7.org/fhir/StructureDefinition/ServiceRequest`) works.

## Version
openFHIR 3.0.2. Workaround: use the base resource URL.
