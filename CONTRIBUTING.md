# Contributing

These conventions keep the lab's code reproducible and easy to review. New to Git? GitHub Desktop (or the RStudio **Git** pane) covers every step below without the command line.

## Workflow

1. **Pull** the latest version of `main` before you start.
2. **Create a branch** for your change, named after what it does, e.g., `add-diann-import` or `fix-qc-plot-labels`.
3. **Commit** small, logical changes with a short message in the imperative mood, e.g., `Add function to read DIA-NN pg_matrix`.
4. **Push** the branch and open a **pull request** on GitHub. Briefly describe what changed and how you tested it.
5. A maintainer reviews the pull request and merges it into `main`.

Please do not commit directly to `main`.

## Code conventions

### All languages

- Start each function with a short description of its purpose, inputs and output.
- Read file locations from `configs/paths.yml` or from a settings cell; never hard-code personal paths such as `C:/Users/...` inside functions.
- Store analysis settings (filtering thresholds, normalization choices) in `configs/` or a settings module rather than deep inside the code.
- Write outputs to `results/` (ignored by Git) or to lab storage, never into the code folders.
- Set a random seed before any step that involves randomness, such as imputation.

### R (`R/`)

- Put reusable functions in `R/functions/`, one file per topic (e.g., `R/functions/import_diann.R`).
- Put step-by-step workflows in `R/scripts/`, numbered in the order they run (`01_import.R`, `02_qc.R`, …).
- Manage package versions with `renv`; after installing a new package, run `renv::snapshot()` and commit `renv.lock`.

### Python (`python/`)

- Put reusable code in a package folder (e.g., `python/diann_tools/`), one module per processing step, with a docstring for each module and function.
- Keep entry points thin: command-line scripts and notebooks should only set options and call functions from the package.
- Pin package versions in `python/requirements.txt`.
- **Clear notebook outputs before committing** (**Kernel → Restart Kernel and Clear Outputs of All Cells**). Saved outputs can contain run names, sample information and data previews.

## Before every commit

- [ ] `git status` lists only code, configs or documentation — no data files or exported tables.
- [ ] No patient or donor identifiers, clinical metadata or sample keys.
- [ ] Notebooks are saved without outputs.
- [ ] The code runs from a fresh session (R: **Session → Restart R**; Jupyter: **Kernel → Restart Kernel**).
- [ ] New functions work on the files in `example_data/`.

## Questions

Open an issue in this repository or contact the maintainer listed in the README.
