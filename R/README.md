# R/

Reusable functions shared across projects, one file per topic, for example:

- `import_diann.R` — reading DIA-NN reports and matrices
- `qc.R` — identification counts, missingness, CV and intensity distributions
- `normalization.R` — normalization and imputation helpers
- `plotting.R` — shared plot themes and figure helpers

Load them in a script with:

```r
source("R/import_diann.R")
```

Each function should begin with a comment block describing its purpose, inputs and output.
