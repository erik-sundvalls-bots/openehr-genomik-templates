# Proposal: specify id-coded ADL2 → at-coded / ADL 1.4 code conversion

*Draft for SEC / openEHR Discourse. Not posted.*

## Problem
ADL 2.4 allows two node-identifier coding systems: at-coded (the same as ADL 1.4, mandatory for openEHR RM) and id-coded (ADL 2.0–2.3). The spec says that ADL 1.4 → id-coded converters exist (ADL2 `master07.04-adl_basics.adoc` l.39). It does not define the reverse direction, id-coded → at-coded or ADL 1.4, which tools need for CDRs that only accept 1.4/at-coded artefacts.

In id-coded archetypes, `idN` and `atN` are separate code spaces. In at-coded archetypes and ADL 1.4 they share one: AOM 1.4 has one `term_definitions` list per language, and `term_definition(a_lang, a_code)` returns a single term. The mechanical shift `idN`/`atN` → `at(N-1)` (the inverse of the ADL 1.4 → 2 rule `[at0000]` (`[id1]`)) can therefore map a node id and a value code with different meanings onto the same at-code.

The spec's own parallel examples hit this case. `ADL2/master09.09-spec_terminology.adoc` has `DV_CODED_TEXT[id4]` and value code `at4` (l.103, l.124). The at-coded version gives the node `at9000` (l.31) and the value `at0003` (l.52).

## Proposed text (ADL2, new subsection "Conversion from id-coded to at-coded form")
1. The top-level code segment shifts down by one: `id1` → `at0000`, `id1.1` → `at0000.1`, `atN` → `at(N-1)` zero-padded to 4 digits. `id0.N` → `at0.N`.
2. Value codes (`at`) keep the shifted code, because they are persisted in data (`DV_CODED_TEXT.defining_code`).
3. A node id whose shifted code clashes with a value code of different meaning is assigned an unused code. Use the `at9000+` range when the node has no term definition and is not a LOCATABLE. The node id can be omitted where ADL 1.4 does not require one (children of single-valued attributes).
4. If a node id and a value code came from the same ADL 1.4 code (same term definition), they map back to that code. This keeps ADL 1.4 → 2 → 1.4 conversion lossless.
5. Synthetic codes created by 1.4 → 2 converters (`id9000+`, not defined in the terminology) are removed or mapped back to "no node id" on reverse conversion.

## Why
Without a rule, tools disagree. One leaves a duplicate at-code with two meanings, which is invalid AOM 1.4. Another renumbers the value code, which changes coded values stored in data. A shared rule makes down-conversion deterministic and keeps it compatible with data.
