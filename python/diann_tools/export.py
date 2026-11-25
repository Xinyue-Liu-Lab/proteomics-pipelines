"""Run the full export: read -> filter -> build tables -> write files.

Output layout (one folder per export):

    <out_dir>/
        run_summary.tsv          one row per run; written last
        01_<run name>/
            peptides.tsv
            proteins.tsv
        02_<run name>/
            ...

If run_summary.tsv is missing, the export did not finish.
"""

import re
from pathlib import Path

import pandas as pd

from . import filters, mass_error, reader, settings, summary, tables


def write_tsv(table, path):
    """Write a tab-separated file with Unix line endings; missing values are left blank."""
    table.to_csv(path, sep="\t", index=False, lineterminator="\n")


def run_folder_name(number, run):
    """Numbered, file-system-safe folder name for a run, e.g. '01_K562_Std_Slot2-2_1_289'."""
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", str(run))[:80].strip("._") or "unnamed"
    return f"{number:02d}_{safe}"


def export_report(report_path, out_dir, q_cutoffs=None, protein_quantity=None):
    """Export unnormalized peptide and protein tables for every run in a DIA-NN report.

    Parameters
    ----------
    report_path : str or Path
        DIA-NN main report (.parquet).
    out_dir : str or Path
        New folder for the results. It must not exist yet, so earlier exports
        are never overwritten.
    q_cutoffs : dict, optional
        Cutoffs that replace the defaults in settings.Q_CUTOFFS, e.g.
        {"Global.Q.Value": None} to switch the global precursor filter off.
    protein_quantity : str, optional
        "auto", "reported" or "sum-proteotypic"; defaults to settings.PROTEIN_QUANTITY.

    Returns
    -------
    DataFrame
        The run summary (also written to run_summary.tsv).
    """
    report_path = Path(report_path).resolve()
    out_dir = Path(out_dir)
    if out_dir.exists():
        raise FileExistsError(f"{out_dir} already exists; choose a new output folder")

    # Start from the defaults and apply any overrides for this export.
    cutoffs = {**settings.Q_CUTOFFS, **(q_cutoffs or {})}
    unknown = set(cutoffs) - set(settings.Q_CUTOFFS)
    if unknown:
        raise ValueError(f"unknown q-value columns: {', '.join(sorted(unknown))}")

    # 1. Read the report and decide how protein intensities are calculated.
    report = reader.read_report(report_path, cutoffs)
    method = tables.choose_protein_method(report, protein_quantity or settings.PROTEIN_QUANTITY)

    out_dir.mkdir(parents=True)
    summary_rows = []

    # 2. Process each run separately.
    for number, (run, run_rows) in enumerate(report.groupby("Run", sort=True), start=1):
        precursors, contaminants_removed = filters.filter_precursors(run_rows, cutoffs)
        precursors = mass_error.add_mass_columns(precursors)

        peptides = tables.peptide_table(precursors, run)
        proteins = tables.protein_table(filters.protein_filter(precursors, cutoffs), run, method)

        # 3. Write this run's tables to its own folder.
        folder = run_folder_name(number, run)
        (out_dir / folder).mkdir()
        write_tsv(peptides, out_dir / folder / "peptides.tsv")
        write_tsv(proteins, out_dir / folder / "proteins.tsv")

        summary_rows.append(summary.run_summary(
            report_path, run, len(run_rows), contaminants_removed, precursors, proteins,
            method, cutoffs, f"{folder}/peptides.tsv", f"{folder}/proteins.tsv",
        ))
        print(f"  {folder}: {len(peptides)} precursors, {len(proteins)} protein groups")

    # 4. The summary is written last and marks a complete export.
    run_summary = pd.DataFrame(summary_rows)
    write_tsv(run_summary, out_dir / "run_summary.tsv")
    print(f"Exported {len(run_summary)} run(s) to {out_dir}")
    return run_summary
