# Draft issue
- Target: https://github.com/openFHIR/openfhir/issues
- Title: `manual` mapping directly on a repeating element applies the last matching code to every repetition
- Related/possible duplicate: https://github.com/openFHIR/openfhir/issues/88 (toFHIR ignores openehrCondition in manual coded mappings — always emits the last branch). Consider commenting there instead of filing.

## Repro
```yaml
  - name: reasonCode
    with:
      fhir: $resource.reasonCode
      openehr: $archetype/activities[at0001]/description[at0009]/items[at0062]
    manual:
      - name: q1
        fhir: [{ path: coding.code, value: "1" }]
        openehr: [{ path: defining_code/code_string, value: at0.1 }]
        ...
      - name: q2 ...
```
Input: ServiceRequest with two `reasonCode`s (codes 1 and 2).

## Expected
Two openEHR elements with at0.1 and at0.2 (and back).

## Actual
The manual block is evaluated against the whole collection; every repetition gets the last matching code.

## Version
openFHIR 3.0.2 (docker image openfhir/openfhir).

## Workaround
Put the table in a `followedBy` child using `$fhirRoot`/`$openehrRoot`.
