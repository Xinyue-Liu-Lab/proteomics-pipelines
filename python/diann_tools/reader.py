"""Read a DIA-NN main report (.parquet) into a pandas DataFrame."""

from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

from . import settings


def report_columns(path):
    """Return the set of column names in a Parquet report without loading the data."""
    return set(pq.read_schema(path).names)


def count_rows_per_run(path):
    """Return a small table with the number of report rows in each run.

    Useful as a quick check of what a report contains before exporting.
    """
    runs = pd.read_parquet(path, columns=["Run"])
    return runs.groupby("Run", sort=True).size().reset_index(name="Input.Rows")


def read_report(path, q_cutoffs):
    """Load the columns the exporter needs and check that the report is usable.

    Parameters
    ----------
    path : str or Path
        DIA-NN main report in Parquet format (report.parquet).
    q_cutoffs : dict
        Q-value cutoffs that will be applied. Every column with an active
        cutoff (not None) must exist in the report.
    """
    path = Path(path)
    if path.suffix.lower() != ".parquet":
        raise ValueError(f"{path.name}: expected a DIA-NN .parquet report")

    available = report_columns(path)

    # Required columns: without these no table can be built.
    missing = [column for column in settings.REQUIRED_COLUMNS if column not in available]
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {', '.join(missing)}")

    # An active filter on an absent column would silently pass nothing,
    # so stop and ask the user to switch it off instead.
    for column, cutoff in q_cutoffs.items():
        if cutoff is not None and column not in available:
            raise ValueError(
                f"{path.name} has no {column} column; set its cutoff to None to export without this filter"
            )

    # Read only the columns we use (dict.fromkeys removes duplicates, keeps order).
    wanted = dict.fromkeys((*settings.REQUIRED_COLUMNS, *settings.OPTIONAL_COLUMNS))
    columns = [column for column in wanted if column in available]
    report = pd.read_parquet(path, columns=columns)

    if report.empty:
        raise ValueError(f"{path.name} contains no rows")
    if report["Run"].isna().any():
        raise ValueError(f"{path.name} has rows without a Run name")
    return report
