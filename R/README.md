# R/

R code of the lab.

```
R/
├── functions/   # reusable functions, one file per topic (e.g., import_diann.R)
└── scripts/     # step-by-step workflows that use the functions (01_import.R, 02_qc.R, …)
```

## Setup

1. Open `proteomics-pipelines.Rproj` in the repository root, so that all paths start from the repository folder.
2. Copy `configs/paths.example.yml` to `configs/paths.yml` and edit the paths for your computer.
3. Once an `renv.lock` file is present, run `renv::restore()` to install the package versions used by the lab.

Load a function file in a script with:

```r
source("R/functions/import_diann.R")
```

Write outputs to `results/` (not tracked by Git) or to lab storage.
