"""Remove decoys and contaminants and apply q-value cutoffs.

The order matters for the run summary: decoys are removed first, then
contaminants are counted and removed, then q-value cutoffs are applied.
"""

from . import settings


def within_cutoff(values, cutoff):
    """True where 0 <= value <= cutoff. Missing values do not pass."""
    return values.between(0, cutoff).fillna(False)


def filter_precursors(run_rows, q_cutoffs):
    """Return the passing precursors of one run and the number of contaminant rows removed.

    Parameters
    ----------
    run_rows : DataFrame
        All report rows of a single run.
    q_cutoffs : dict
        DIA-NN column -> cutoff (None = off). Cutoffs listed in
        settings.PROTEIN_ONLY_FILTERS are skipped here; see protein_filter().
    """
    rows = run_rows

    # 1. Decoys (Decoy = 1). Rows with an unknown decoy flag are also dropped.
    if "Decoy" in rows.columns:
        rows = rows[rows["Decoy"] == 0]

    # 2. Contaminants, matched on the protein group name.
    is_contaminant = rows["Protein.Group"].str.contains(
        settings.CONTAMINANT_PATTERN, case=False, na=False
    )
    contaminants_removed = int(is_contaminant.sum())
    rows = rows[~is_contaminant]

    # 3. Precursor-level q-value cutoffs.
    for column, cutoff in q_cutoffs.items():
        if cutoff is None or column in settings.PROTEIN_ONLY_FILTERS:
            continue
        rows = rows[within_cutoff(rows[column], cutoff)]

    # DIA-NN reports one row per precursor and run; a duplicate means the
    # report has more than one channel or was merged incorrectly.
    duplicated = rows["Precursor.Id"].duplicated()
    if duplicated.any():
        example = rows.loc[duplicated, "Precursor.Id"].iloc[0]
        raise ValueError(f"precursor {example!r} appears more than once in the same run")

    return rows.copy(), contaminants_removed


def protein_filter(precursors, q_cutoffs):
    """Apply the protein-only cutoffs (PG.Q.Value by default) to passing precursors."""
    rows = precursors
    for column in settings.PROTEIN_ONLY_FILTERS:
        cutoff = q_cutoffs.get(column)
        if cutoff is not None:
            rows = rows[within_cutoff(rows[column], cutoff)]
    return rows
