# proteomics-pipelines

Shared analysis code of the **Xinyue Liu Lab** for mass spectrometry-based proteomics, primarily data acquired on the Bruker nanoElute 2 + timsTOF Pro and searched with DIA-NN.

This repository contains reusable code, analysis settings and documentation only. Raw files, search results and sample metadata remain on lab storage (see [Data policy](#data-policy)).

## Repository layout

```
proteomics-pipelines/
├── R/
│   ├── functions/   # reusable R functions, one file per topic (e.g., import_diann.R)
│   └── scripts/     # step-by-step R workflows (01_import.R, 02_qc.R, …)
├── python/          # Python tools; currently the DIA-NN peptide and protein export
├── configs/         # analysis settings shared by R and Python; DIA-NN search records in configs/diann/
├── docs/            # conventions, SOP notes, how-to guides
├── example_data/    # small test files only (< 5 MB each)
├── results/         # your local outputs; ignored by Git
├── CONTRIBUTING.md  # how to propose changes
└── proteomics-pipelines.Rproj
```

## Available tools

| Tool | Language | What it does | Guide |
| --- | --- | --- | --- |
| DIA-NN export | Python | Converts a DIA-NN `report.parquet` into per-run peptide and protein tables with a run summary (counts, filters, mass error). Written as a starting point for new lab members. | [python/README.md](python/README.md) |

## Getting started

1. Accept the invitation to the `Xinyue-Liu-Lab` organization on GitHub.
2. Install [Git](https://git-scm.com/downloads) or, if you prefer not to use the command line, [GitHub Desktop](https://desktop.github.com/).
3. Clone (download) the repository: `https://github.com/Xinyue-Liu-Lab/proteomics-pipelines.git`. In GitHub Desktop: **File → Clone repository**; in RStudio: **File → New Project → Version Control → Git**.
4. Copy `configs/paths.example.yml` to `configs/paths.yml` and edit the paths for your computer. `paths.yml` is not tracked by Git.
5. Set up the language you will use:
   - **R:** open `proteomics-pipelines.Rproj` (see [R/README.md](R/README.md)).
   - **Python:** create the environment in `python/` (see [python/README.md](python/README.md)).

Pull the latest version before you start working, so that you use the current code.

## Using this code in a project

Start each new project or manuscript from the [`project-template`](https://github.com/Xinyue-Liu-Lab/project-template) repository (**Use this template → Create a new repository**). Record in the project README which version of this toolkit (release tag or commit) the analysis used.

## Data policy

- **No raw or derived MS data in Git.** This includes `.d` folders, converted files (`.mzML`, `.dia`), spectral libraries, DIA-NN reports and FASTA files. The `.gitignore` blocks the common formats, but always check `git status` before committing.
- **No identifiable sample information.** Patient or donor identifiers, clinical metadata and sample keys must never be committed, even though the repository is private. Keep them in the approved secure storage.
- **No exported tables in Git.** Write outputs to `results/` (ignored by Git) or to lab storage.
- **No hard-coded paths.** Scripts read file locations from `configs/paths.yml`.
- GitHub rejects files larger than 100 MB; anything approaching that size does not belong in this repository.

## Versioning

When code is used for a manuscript, report or shared dataset, create a release tag (e.g., `v1.0-<project-shortname>`) so that the exact version can be cited and recovered.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintainer

All members in the Liu Lab
