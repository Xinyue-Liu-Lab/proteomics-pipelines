"""One summary row per run: identification counts, filters and mass error."""

import pandas as pd

METHOD_LABELS = {
    "reported": "PG.Quantity",
    "sum-proteotypic": "sum of proteotypic Precursor.Quantity",
}


def ppm_statistics(values, label):
    """Count, median signed error and 95th percentile of the absolute error."""
    values = values.dropna()
    return {
        f"{label}.Count": len(values),
        f"{label}.Median": values.median(),
        f"{label}.Abs.P95": values.abs().quantile(0.95),
    }


def run_summary(report_path, run, input_rows, contaminants_removed, precursors, proteins,
                method, q_cutoffs, peptide_file, protein_file):
    """Collect the numbers reported in run_summary.tsv for one run.

    precursors : passing precursors used for the peptide table
    proteins   : the protein table written for this run
    """
    if "Proteotypic" in precursors.columns:
        proteotypic = precursors["Proteotypic"] == 1
        proteotypic_peptides = precursors.loc[proteotypic, "Stripped.Sequence"].nunique()
    else:
        proteotypic_peptides = pd.NA

    row = {
        "Report": report_path.name,
        "Source.Path": str(report_path),
        "Run": run,
        "Input.Rows": input_rows,
        "Contaminant.Rows.Removed": contaminants_removed,
        "Peptide.Input.Precursors": len(precursors),        # rows in peptides.tsv
        "Protein.Groups": len(proteins),                     # rows in proteins.tsv
        "Peptides": precursors["Modified.Sequence"].nunique(),
        "Unique.Stripped.Peptides": precursors["Stripped.Sequence"].nunique(),
        "Proteotypic.Stripped.Peptides": proteotypic_peptides,
        "Protein.Intensity.Method": METHOD_LABELS[method],
        "Proteins.File": protein_file,
        "Peptides.File": peptide_file,
        "Observed.Precursor.Mz.Count": precursors["Observed.Precursor.Mz"].count(),
    }
    # Record every cutoff so the export can be reproduced.
    row.update({f"Filter.{column}": "off" if cutoff is None else str(cutoff)
                for column, cutoff in q_cutoffs.items()})
    row.update(ppm_statistics(precursors["MS1.PPM"], "MS1.PPM"))
    row.update(ppm_statistics(precursors["MS2.Best.Fragment.PPM"], "MS2.Best.Fragment.PPM"))
    return row
