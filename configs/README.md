# configs/

Analysis settings and records of how data were processed.

- `paths.example.yml` — template for machine-specific file locations. Copy it to `paths.yml` (ignored by Git) and edit it for your computer.
- `diann/` — one record per DIA-NN search (see `diann/README.md`).
- Other settings, such as filtering thresholds or normalization choices, can be stored here as small YAML or text files so that scripts do not hard-code them.
