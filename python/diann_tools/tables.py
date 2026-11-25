"""Build the per-run peptide and protein tables.

All intensities stay on DIA-NN's original (unnormalized) scale. No log
transformation, normalization or imputation is applied.
"""

import numpy as np
import pandas as pd

# Columns copied from the report into the peptide table, in output order,
# renamed where the exporter uses a clearer name. Absent columns are skipped.
PEPTIDE_COLUMNS = {
    "Protein.Group": "Protein.Group",
    "Protein.Ids": "Mapped.Protein.Ids",
    "Genes": "Genes",
    "Protein.Names": "Protein.Names",
    "Modified.Sequence": "Modified.Sequence",
    "Stripped.Sequence": "Stripped.Sequence",
    "Precursor.Charge": "Precursor.Charge",
    "Precursor.Mz": "Library.Precursor.Mz",
    "Observed.Precursor.Mz": "Observed.Precursor.Mz",
    "Precursor.Quantity": "Peptide.Intensity.Unnormalized",
    "Quantity.Quality": "Quantity.Quality",
    "Q.Value": "Q.Value",
    "PEP": "PEP",
    "Global.Q.Value": "Global.Q.Value",
    "PG.Q.Value": "PG.Q.Value",
    "Global.PG.Q.Value": "Global.PG.Q.Value",
}

# Protein-group annotations: distinct values are joined with " | ".
ANNOTATION_COLUMNS = {
    "Protein.Ids": "Mapped.Protein.Ids",
    "Genes": "Genes",
    "Protein.Names": "Protein.Names",
}


def usable_quantity(values):
    """Keep finite, non-negative intensities; anything else becomes missing.

    A zero is a real measurement and is kept.
    """
    values = values.astype("float64")
    return values.where(np.isfinite(values) & (values >= 0))


def join_unique(values):
    """Join the distinct, non-blank text values of a group, sorted, with ' | '."""
    names = {str(value).strip() for value in values.dropna()}
    return " | ".join(sorted(names - {""}))


def choose_protein_method(report, requested):
    """Resolve 'auto' and check that the chosen method has the column it needs."""
    method = requested
    if method == "auto":
        method = "reported" if "PG.Quantity" in report.columns else "sum-proteotypic"
    needed = {"reported": "PG.Quantity", "sum-proteotypic": "Proteotypic"}.get(method)
    if needed is None:
        raise ValueError(f"unknown protein quantity method {requested!r}")
    if needed not in report.columns:
        raise ValueError(f"protein quantity method {method!r} needs the {needed} column")
    return method


def peptide_table(precursors, run):
    """One row per precursor (modified sequence + charge) with its raw MS2 intensity.

    Match rows across runs by Modified.Sequence and Precursor.Charge.
    """
    precursors = precursors.sort_values(["Modified.Sequence", "Precursor.Charge", "Precursor.Id"])
    present = {source: name for source, name in PEPTIDE_COLUMNS.items() if source in precursors.columns}
    table = precursors[list(present)].rename(columns=present)
    table["Peptide.Intensity.Unnormalized"] = usable_quantity(table["Peptide.Intensity.Unnormalized"])
    table.insert(0, "Run", run)
    return table.reset_index(drop=True)


def protein_table(precursors, run, method):
    """One row per DIA-NN protein group with an unnormalized intensity.

    method = "sum-proteotypic": sum of Precursor.Quantity over precursors with
        Proteotypic = 1. A group with no usable proteotypic signal gets a
        blank intensity.
    method = "reported": DIA-NN's PG.Quantity for the group.
    """
    # Precursors without a protein group cannot be assigned and are left out.
    assigned = precursors[precursors["Protein.Group"].fillna("").str.strip() != ""]
    groups = assigned.groupby("Protein.Group", sort=True)

    table = pd.DataFrame(index=groups.size().index)
    for source, name in ANNOTATION_COLUMNS.items():
        if source in assigned.columns:
            table[name] = groups[source].agg(join_unique)
    table["Precursor.Count"] = groups.size()
    table["Peptide.Count"] = groups["Stripped.Sequence"].nunique()

    if method == "reported":
        quantity = usable_quantity(assigned["PG.Quantity"]).groupby(assigned["Protein.Group"])
        if (quantity.nunique() > 1).any():
            raise ValueError(f"run {run!r}: PG.Quantity differs within a protein group")
        table["Protein.Intensity.Unnormalized"] = quantity.first()
    else:
        proteotypic = assigned["Proteotypic"] == 1
        quantity = usable_quantity(assigned["Precursor.Quantity"]).where(proteotypic)
        # min_count=1 keeps the sum blank (not 0) when no proteotypic value exists.
        table["Protein.Intensity.Unnormalized"] = quantity.groupby(assigned["Protein.Group"]).sum(min_count=1)

    # Highest (least confident) protein q-values among the group's precursors.
    for score in ("PG.Q.Value", "Global.PG.Q.Value"):
        if score in assigned.columns:
            table[f"{score}.Max"] = groups[score].max()

    table = table.reset_index()
    table.insert(0, "Run", run)
    return table
