# Draft issue (own fork)
- Target: https://github.com/erik-sundvalls-bots/archie/issues
- Title: adl14 down-converter does not compile on master (Archie 4.0.0)

## Problem
master is on upstream Archie 4.0.0; the `adl14.down` converter was written against 3.21. Five compile errors:
- `getConstraint()` now returns `String` (was a list/constraint object).
- `getRmRelease()` removed.

## Fix
Adapt the converter to the 4.0.0 API (use the String constraint directly; take RM release from the archetype/`ArchetypeHRID`/metadata or a converter option), run the converter tests, open a PR against master. Until then build from the feature branch.
