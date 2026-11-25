# DIA-NN export (Python)

This tool turns a DIA-NN main report (`report.parquet`) from a label-free experiment into three plain-text tables that are easy to open in Excel, R or Python:

- `peptides.tsv`: one row per identified peptide ion (precursor) in each run
- `proteins.tsv`: one row per identified protein group in each run
- `run_summary.tsv`: one row per run, with identification counts, the filters used and mass accuracy

It removes decoys and contaminants, keeps only confident identifications, and reports intensities on DIA-NN's original scale. The code is split into short, commented modules so each step can be read on its own.

## Key terms

| Term | Meaning |
| --- | --- |
| Precursor | A peptide with a given set of modifications and a given charge, i.e. the ion selected for fragmentation. The same peptide at charge 2+ and 3+ is two precursors. |
| Modified sequence | The peptide sequence including modifications, written as UniMod codes, e.g. `AC(UniMod:4)DEFM(UniMod:35)K` (UniMod:4 = carbamidomethylated cysteine, UniMod:35 = oxidized methionine). |
| Stripped sequence | The amino-acid sequence without modifications, e.g. `ACDEFMK`. |
| Protein group | Proteins that cannot be told apart from the identified peptides are reported together as one group, e.g. `P62805;Q99878`. |
| Proteotypic peptide | A peptide that occurs in only one protein (or gene, depending on DIA-NN settings) of the sequence database, so its signal can be assigned unambiguously. |
| Decoy | An artificial peptide sequence that DIA-NN uses to estimate how many identifications are false. Decoys are never real identifications. |
| Contaminant | A protein that is commonly introduced during sample handling (e.g. keratins, trypsin), marked `contaminant_` or `cRAP-` in the sequence database. |
| Q-value | The estimated false discovery rate (FDR) at which an identification is accepted. `Q.Value ≤ 0.01` keeps identifications at an estimated 1% FDR. *Run-specific* q-values refer to one run; *global* q-values express confidence that the peptide or protein was correctly identified in at least one run of the experiment. |
| PEP | Posterior error probability: the estimated probability that this single identification is wrong. |
| Unnormalized intensity | The signal as measured, without correction for differences in sample loading or instrument response between runs. Normalize before comparing runs quantitatively. |
| ppm | Parts per million; mass error = 10⁶ × (observed m/z − theoretical m/z) / theoretical m/z. |

## Folder layout

```
python/
├── DIA-NN_Export.ipynb          # interactive use: settings, preview, export, inspect
├── export_diann.py              # command-line use
├── requirements.txt
└── diann_tools/                 # the code, one step per module
    ├── settings.py              # default cutoffs, contaminant pattern, column lists
    ├── reader.py                # read and check the .parquet report
    ├── filters.py               # decoys, contaminants, q-value cutoffs
    ├── mass_error.py            # MS1/MS2 ppm and observed precursor m/z
    ├── tables.py                # peptide and protein tables for one run
    ├── summary.py               # one run_summary.tsv row per run
    └── export.py                # runs the steps in order and writes the files
```

To change a default (for example a q-value cutoff), edit `diann_tools/settings.py`. To change it for a single export, set it in the notebook or on the command line.

## Setup

Create a Python environment in the `python` folder of your copy of the repository once (Python 3.10 or later). The `.venv` folder is not tracked by Git.

```powershell
Set-Location '<your copy of the repository>\proteomics-pipelines\python'
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
& .\.venv\Scripts\python.exe -m pip install 'jupyterlab>=4,<5'   # only for the notebook
```

## Usage

**Notebook (recommended for beginners).** Open `DIA-NN_Export.ipynb`, set `input_file` in cell 1, and run the cells from top to bottom with **Shift+Enter**. By default the tables are written to `results/<report name>_tables` in the repository folder.

```powershell
& .\.venv\Scripts\python.exe -m jupyterlab .\DIA-NN_Export.ipynb
```

**Command line.**

```powershell
& .\.venv\Scripts\python.exe .\export_diann.py 'D:\UNT\Data\DIA_20min.parquet' --out ..\results\DIA_20min_tables

# Switch off the experiment-wide filters, e.g. for an LC-MS method comparison
& .\.venv\Scripts\python.exe .\export_diann.py 'D:\UNT\Data\DIA_20min.parquet' --out ..\results\DIA_20min_runfilter `
    --q-cutoff Global.Q.Value=off --q-cutoff Global.PG.Q.Value=off
```

The output folder must not exist yet, so earlier exports are never overwritten. Exported tables are never uploaded to GitHub: everything in `results/` and every `peptides.tsv`, `proteins.tsv` and `run_summary.tsv` is ignored by Git. Copy results you want to keep to lab storage.

## Processing steps

Each run in the report is processed separately:

1. **Decoys** are removed (`Decoy = 1`).
2. **Contaminants** are removed: rows whose `Protein.Group` contains `contaminant_` or `cRAP-` (case-insensitive). A protein group that contains any contaminant entry is removed in full.
3. **Q-value cutoffs** are applied. A row is kept when its q-value is at or below the cutoff.

   | DIA-NN column | Default | Applies to |
   | --- | --- | --- |
   | `Q.Value` | 0.01 | all tables |
   | `Global.Q.Value` | 0.01 | all tables |
   | `Global.PG.Q.Value` | 0.01 | all tables |
   | `PG.Q.Value` | 0.05 | protein table only |
   | `Lib.Q.Value` | off | all tables |
   | `Lib.PG.Q.Value` | off | all tables |

4. **Mass errors** are calculated for the remaining precursors (see `run_summary.tsv` below).
5. **Tables** are built and written.

No log transformation, normalization or imputation is applied. Negative or non-finite intensities are treated as missing (blank); a measured zero is kept.

## Output

```
<output folder>/
├── run_summary.tsv            # written last; if it is missing, the export did not finish
└── 01_<run name>/
    ├── peptides.tsv
    └── proteins.tsv
```

A blank cell means the value is missing or does not apply. Columns marked "if present" appear only when the DIA-NN report contains the source column.

### `peptides.tsv`

One row per precursor (modified sequence + charge) that passed all filters. To follow the same precursor across runs, match rows by `Modified.Sequence` and `Precursor.Charge`.

| Column | Meaning | DIA-NN source |
| --- | --- | --- |
| `Run` | Name of the LC-MS run (raw file). | `Run` |
| `Protein.Group` | Protein group DIA-NN inferred for this precursor; accessions are separated by `;`. | `Protein.Group` |
| `Mapped.Protein.Ids` | All proteins in the library or sequence database that contain this peptide (if present). | `Protein.Ids` |
| `Genes` | Gene names of the protein group (if present; blank when DIA-NN could not annotate them). | `Genes` |
| `Protein.Names` | UniProt entry names of the protein group, e.g. `RL4_HUMAN` (if present). | `Protein.Names` |
| `Modified.Sequence` | Peptide sequence with modifications. | `Modified.Sequence` |
| `Stripped.Sequence` | Peptide sequence without modifications. | `Stripped.Sequence` |
| `Precursor.Charge` | Charge state of the precursor ion. | `Precursor.Charge` |
| `Library.Precursor.Mz` | Theoretical (library) m/z of the precursor (if present). | `Precursor.Mz` |
| `Observed.Precursor.Mz` | Measured m/z at the MS1 apex, = library m/z + `Ms1.Apex.Mz.Delta`. Blank when DIA-NN found no MS1 apex. | calculated |
| `Peptide.Intensity.Unnormalized` | MS2-based intensity of this precursor, not normalized. This is the main quantitative value. | `Precursor.Quantity` |
| `Quantity.Quality` | Precision of the intensity, from 0 to 1; higher is better. Calculated by DIA-NN as 1 / (1 + SD), where SD is the estimated error of the relative quantity (if present). | `Quantity.Quality` |
| `Q.Value` | Run-specific precursor q-value. | `Q.Value` |
| `PEP` | Run-specific posterior error probability of the precursor (if present). | `PEP` |
| `Global.Q.Value` | Experiment-wide precursor q-value. | `Global.Q.Value` |
| `PG.Q.Value` | Run-specific protein-group q-value. | `PG.Q.Value` |
| `Global.PG.Q.Value` | Experiment-wide protein-group q-value. | `Global.PG.Q.Value` |

### `proteins.tsv`

One row per protein group, built from the precursors in `peptides.tsv` that also pass the protein cutoff (`PG.Q.Value ≤ 0.05` by default). Precursors without a protein group are left out.

| Column | Meaning |
| --- | --- |
| `Run` | Name of the LC-MS run. |
| `Protein.Group` | Protein group identifier; accessions are separated by `;`. |
| `Mapped.Protein.Ids` | All proteins matched by the group's precursors; distinct entries are separated by ` \| ` (if present). |
| `Genes` | Gene names of the group (if present). |
| `Protein.Names` | UniProt entry names of the group (if present). |
| `Precursor.Count` | Number of precursors assigned to the group. |
| `Peptide.Count` | Number of distinct peptide sequences (stripped sequences) assigned to the group. |
| `Protein.Intensity.Unnormalized` | Protein intensity, not normalized. By default, the sum of `Peptide.Intensity.Unnormalized` over the group's **proteotypic** precursors; blank when the group has no proteotypic signal. If the report contains DIA-NN's `PG.Quantity`, that value is used instead (setting `protein_quantity = "auto"`). |
| `PG.Q.Value.Max` | Highest run-specific protein-group q-value among the group's precursors (the least confident value). |
| `Global.PG.Q.Value.Max` | Highest experiment-wide protein-group q-value among the group's precursors. |

### `run_summary.tsv`

One row per run. Use it to compare runs at a glance and to find each run's tables.

| Column | Meaning |
| --- | --- |
| `Report` | File name of the DIA-NN report. |
| `Source.Path` | Full path of the DIA-NN report. |
| `Run` | Name of the LC-MS run. |
| `Input.Rows` | Rows for this run in the report before any filtering. |
| `Contaminant.Rows.Removed` | Rows removed as contaminants (after decoy removal, before q-value filtering). |
| `Peptide.Input.Precursors` | Number of precursors that passed all filters (= rows in `peptides.tsv`). |
| `Protein.Groups` | Number of protein groups (= rows in `proteins.tsv`). |
| `Peptides` | Number of distinct modified sequences. |
| `Unique.Stripped.Peptides` | Number of distinct stripped sequences; modified forms of the same sequence count once. |
| `Proteotypic.Stripped.Peptides` | Number of distinct stripped sequences that are proteotypic. |
| `Protein.Intensity.Method` | How `Protein.Intensity.Unnormalized` was calculated. |
| `Proteins.File`, `Peptides.File` | Location of this run's tables, relative to the output folder. |
| `Observed.Precursor.Mz.Count` | Number of precursors with a measured MS1 apex m/z. |
| `Filter.<column>` | The q-value cutoff used for each DIA-NN column, or `off`. |
| `MS1.PPM.Count` | Number of precursors with a valid MS1 mass error. |
| `MS1.PPM.Median` | Median signed MS1 mass error (ppm) = 10⁶ × `Ms1.Apex.Mz.Delta` / `Precursor.Mz`. A value far from 0 indicates a mass calibration offset. |
| `MS1.PPM.Abs.P95` | 95% of precursors have an MS1 error within ± this value (ppm); a measure of the spread. |
| `MS2.Best.Fragment.PPM.Count`, `.Median`, `.Abs.P95` | The same statistics for the fragment ion DIA-NN rated best for each precursor, = 10⁶ × `Best.Fr.Mz.Delta` / `Best.Fr.Mz`. |

## Scope

The exporter handles label-free (single-channel) DIA-NN reports without phosphosite analysis and processes one report per export. Phosphopeptide and phosphosite tables are not included yet.

## Validation

The exporter was checked against the lab's earlier, more extensive exporter on two K562 standard runs (November 2026), with default cutoffs. The peptide tables (61,725 and 51,398 precursors) and protein tables (6,717 and 6,409 protein groups) contained the same rows in the same order, with identical values in every column listed above, and the run summaries agreed on all counts and mass-error statistics. With the experiment-wide filters switched off, the run-summary counts and mass-error statistics also agreed.

Column definitions follow the [DIA-NN main output reference](https://github.com/vdemichev/DiaNN#main-output-reference).
