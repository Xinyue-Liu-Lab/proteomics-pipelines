"""Default settings for the DIA-NN exporter.

Every value the exporter uses lives in this module, so filtering can be
changed in one place. The notebook and the command line can override the
q-value cutoffs and the protein quantity method for a single export without
editing this file.
"""

# ---------------------------------------------------------------------------
# Q-value cutoffs
# ---------------------------------------------------------------------------
# Keys are DIA-NN column names. A row passes when 0 <= value <= cutoff.
# Set a cutoff to None to switch that filter off (for example, when an older
# report lacks the column, or to compare LC-MS methods with run-specific
# filters only).
Q_CUTOFFS = {
    "Q.Value": 0.01,            # run-specific precursor q-value
    "Global.Q.Value": 0.01,     # experiment-wide precursor q-value
    "Global.PG.Q.Value": 0.01,  # experiment-wide protein-group q-value
    "PG.Q.Value": 0.05,         # run-specific protein-group q-value (protein table only)
    "Lib.Q.Value": None,        # library precursor q-value
    "Lib.PG.Q.Value": None,     # library protein-group q-value
}

# Cutoffs listed here are applied to the protein table only. All other
# cutoffs are applied to every precursor before any table is built.
PROTEIN_ONLY_FILTERS = ("PG.Q.Value",)

# ---------------------------------------------------------------------------
# Contaminants
# ---------------------------------------------------------------------------
# Rows whose Protein.Group matches this pattern (case-insensitive) are removed.
# A mixed protein group that contains a contaminant entry is removed in full.
CONTAMINANT_PATTERN = r"contaminant_|cRAP-"

# ---------------------------------------------------------------------------
# Protein intensity
# ---------------------------------------------------------------------------
# "auto"            use PG.Quantity when the report has it, otherwise sum
# "reported"        use DIA-NN's PG.Quantity (error if the column is missing)
# "sum-proteotypic" sum Precursor.Quantity of precursors with Proteotypic = 1
PROTEIN_QUANTITY = "auto"

# ---------------------------------------------------------------------------
# Columns read from the report
# ---------------------------------------------------------------------------
# The export stops with an error if any of these is missing.
REQUIRED_COLUMNS = (
    "Run",
    "Precursor.Id",
    "Modified.Sequence",
    "Stripped.Sequence",
    "Precursor.Charge",
    "Protein.Group",
    "Precursor.Quantity",
)

# Read when present; the related output columns are left out otherwise.
OPTIONAL_COLUMNS = (
    "Decoy",
    "Proteotypic",
    "Protein.Ids",
    "Genes",
    "Protein.Names",
    "Precursor.Mz",
    "Ms1.Apex.Area",
    "Ms1.Apex.Mz.Delta",
    "Best.Fr.Mz",
    "Best.Fr.Mz.Delta",
    "Quantity.Quality",
    "PEP",
    "PG.Quantity",
    *Q_CUTOFFS,
)
