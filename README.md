# proteomics-pipelines

Shared analysis code of the **Xinyue Liu Lab** (UNT Health Fort Worth) for mass spectrometry-based proteomics, primarily data acquired on the Bruker nanoElute 2 + timsTOF Pro and searched with DIA-NN.

This repository contains reusable code, analysis settings and documentation only. Raw files, search results and sample metadata remain on lab storage (see [Data policy](#data-policy)).

## Repository layout

```
proteomics-pipelines/
├── R/               # reusable functions, one file per topic (e.g., import_diann.R)
├── scripts/         # step-by-step workflows (01_import.R, 02_qc.R, …)
├── configs/         # analysis settings; DIA-NN search records in configs/diann/
├── docs/            # conventions, SOP notes, how-to guides
├── example_data/    # small test files only (< 5 MB each)
├── CONTRIBUTING.md  # how to propose changes
└── proteomics-pipelines.Rproj
```

## Getting started

1. Accept the invitation to the `Xinyue-Liu-Lab` organization on GitHub.
2. Install [Git](https://git-scm.com/downloads), R and RStudio. If you prefer not to use the command line, [GitHub Desktop](https://desktop.github.com/) works as well.
3. Clone the repository. In RStudio: **File → New Project → Version Control → Git**, then paste
   `https://github.com/Xinyue-Liu-Lab/proteomics-pipelines.git`
4. Open `proteomics-pipelines.Rproj`.
5. Copy `configs/paths.example.yml` to `configs/paths.yml` and edit the paths for your computer. `paths.yml` is not tracked by Git.
6. Once an `renv.lock` file is present, run `renv::restore()` to install the exact package versions used by the lab.

## Using this code in a project

Start each new project or manuscript from the [`project-template`](https://github.com/Xinyue-Liu-Lab/project-template) repository (**Use this template → Create a new repository**). Record in the project README which version of this toolkit (release tag or commit) the analysis used.

## Data policy

- **No raw or derived MS data in Git.** This includes `.d` folders, converted files (`.mzML`, `.dia`), spectral libraries, DIA-NN reports and FASTA files. The `.gitignore` blocks the common formats, but always check `git status` before committing.
- **No identifiable sample information.** Patient or donor identifiers, clinical metadata and sample keys must never be committed, even though the repository is private. Keep them in the approved secure storage.
- **No hard-coded paths.** Scripts read file locations from `configs/paths.yml`.
- GitHub rejects files larger than 100 MB; anything approaching that size does not belong in this repository.

## Versioning

When code is used for a manuscript, report or shared dataset, create a release tag (e.g., `v1.0-<project-shortname>`) so that the exact version can be cited and recovered.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintainer

Le Sun, Xinyue Liu Lab
