# Draft archetypes (ADL2)

Our own drafts made for this project (author organisation in the files: Regionala cancercentrum i samverkan); English original with Swedish translation. Not in CKM; CKM parents © openEHR Foundation.

- `CLUSTER.genomic_variant_result-cancer`: specialisation of CKM `genomic_variant_result.v1` (genetic origin, ASCO/AMP, ESCAT, exon, ISCN, SO consequence, implication slot).
- `CLUSTER.genomic_copy_number_variant-cancer`: specialisation adding Amplification and Homozygous deletion.
- `CLUSTER.sequencing_assay-genomic_study`: specialisation of CKM `sequencing_assay.v0` for study id, analysis type and method.
- `CLUSTER.variant_clinical_implication`: new CLUSTER.

Validated and down-converted to ADL 1.4 by `../../tools/build.sh` (output in `../../build/`). Forum proposals for upstream changes: `../../docs/forum-proposals/`.
