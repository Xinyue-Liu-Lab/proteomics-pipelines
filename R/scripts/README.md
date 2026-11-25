# R/scripts/

Step-by-step R workflows, numbered in the order they run:

```
01_import.R
02_qc.R
03_normalize.R
04_statistics.R
05_figures.R
```

Scripts should read paths from `configs/paths.yml`, call functions from `R/functions/`, and write outputs to the `results` directory defined there.
