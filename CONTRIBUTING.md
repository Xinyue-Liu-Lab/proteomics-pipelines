# Contributing

These conventions keep the lab's code reproducible and easy to review. New to Git? The RStudio **Git** pane or GitHub Desktop covers every step below without the command line.

## Workflow

1. **Pull** the latest version of `main` before you start.
2. **Create a branch** for your change, named after what it does, e.g., `add-diann-import` or `fix-qc-plot-labels`.
3. **Commit** small, logical changes with a short message in the imperative mood, e.g., `Add function to read DIA-NN pg_matrix`.
4. **Push** the branch and open a **pull request** on GitHub. Briefly describe what changed and how you tested it.
5. A maintainer reviews the pull request and merges it into `main`.

Please do not commit directly to `main`.

## Code conventions

- Put reusable functions in `R/`, one file per topic (e.g., `R/import_diann.R`, `R/normalization.R`).
- Start each function with a short comment block stating its purpose, inputs and output.
- Put step-by-step workflows in `scripts/`, numbered in the order they run (`01_import.R`, `02_qc.R`, …).
- Read file locations from `configs/paths.yml`; never hard-code paths such as `C:/Users/...`.
- Store analysis settings (filtering thresholds, normalization choices) in `configs/` rather than inside scripts.
- Set a random seed (`set.seed()`) before any step that involves randomness, such as imputation.
- Manage package versions with `renv`; after installing a new package, run `renv::snapshot()` and commit `renv.lock`.

## Before every commit

- [ ] `git status` lists only code, configs or documentation — no data files.
- [ ] No patient or donor identifiers, clinical metadata or sample keys.
- [ ] The script runs from a fresh R session (**Session → Restart R**).
- [ ] New functions work on the files in `example_data/`.

## Questions

Open an issue in this repository or contact the maintainer listed in the README.
