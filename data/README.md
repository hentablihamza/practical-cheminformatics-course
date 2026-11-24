# Datasets

All datasets in this folder are small, public, and committed so the notebooks run offline.
No measurements were invented, averaged, or altered. Each file keeps its original identifiers.

## `esol_delaney.csv` — aqueous solubility (1,128 compounds)

Used in notebooks 01–05 and 10–11.

- `compound_id` — source compound name
- `smiles` — structure (values unchanged)
- `logS` — measured aqueous solubility, log10(mol/L)

**Source:** the DeepChem / MoleculeNet distribution of the Delaney ESOL set
(https://raw.githubusercontent.com/deepchem/deepchem/master/datasets/delaney-processed.csv),
re-used here via the author's [qsar-split-bench](https://github.com/hentablihamza/qsar-split-bench) repository.

**Cite:** Delaney, J. S. ESOL: Estimating Aqueous Solubility Directly from Molecular Structure.
*J. Chem. Inf. Comput. Sci.* **2004**, *44*, 1000–1005. https://doi.org/10.1021/ci034243x

## `egfr_chembl37_ic50.csv` — EGFR inhibitors (6,871 compounds)

Used in notebooks 03–05 and 08–12. One row per compound.

- `compound_id` — ChEMBL molecule ID
- `smiles` — curated structure
- `p_activity` — aggregated pIC50 (−log10 of IC50 in mol/L; 6 = 1 µM, 9 = 1 nM)
- `active` — 1 if pIC50 ≥ 7, else 0

**Source:** ChEMBL release 37 (target CHEMBL203, human EGFR, binding IC50), curated with the author's
[chembl-easy](https://github.com/hentablihamza/chembl-easy) pipeline (target resolution, unit
harmonization, mutant/flagged-assay removal, confidence ≥ 9, replicate aggregation).

## `chembl_cache/` — offline cache for notebook 07

A small snapshot of a live ChEMBL REST API query (human acetylcholinesterase, CHEMBL220, binding
IC50, 1,000 records), so notebook 07 runs without internet. Notebook 07 queries the live API first
and only falls back to these files when the API is unreachable. Refresh with
`python scripts/refresh_chembl_cache.py`.

- `target_search_acetylcholinesterase.csv` — target search results
- `activities_CHEMBL220_IC50.csv` — raw activity records
- `metadata.json` — ChEMBL release, query, and retrieval date

## ChEMBL data licence

ChEMBL data are provided by EMBL-EBI under the Creative Commons Attribution-ShareAlike 3.0 licence
(CC BY-SA 3.0). The ChEMBL-derived files above keep their ChEMBL IDs. If you use them, please cite:

> Zdrazil, B. *et al.* The ChEMBL Database in 2023: a drug discovery platform spanning multiple
> bioactivity data types and time periods. *Nucleic Acids Res.* **2024**, *52*, D1180–D1192.
> https://doi.org/10.1093/nar/gkad1004
