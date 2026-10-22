# templates

- `adl2/`: our ADL2 templates *Genomics cancer report* (`t_genomics_cancer_report`, on CKM `COMPOSITION.report-result`) and *Genomics request* (`t_genomics_request`, on CKM `COMPOSITION.request`), English original with Swedish translation. Value-set bindings were first generated with `../tools/bind_valuesets.py`; the ADL2 files are now the source of truth. Built and validated by `../tools/build.sh`.
- `reference/Molecular_Pathology_Report.oet`: HiGHmed *Molecular Pathology Report* OET (2019, © HiGHmed), kept as prior art only. Described in the top-level README as a CKM template (HiGHmed draft); exact URL and revision not recorded.
