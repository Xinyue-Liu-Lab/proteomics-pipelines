"""Command-line entry point for the DIA-NN exporter.

Examples (PowerShell, from the python folder of the repository):

    python export_diann.py D:\\UNT\\Data\\DIA_20min.parquet --out ..\\results\\DIA_20min_tables

    # Switch the experiment-wide filters off for an LC-MS method comparison
    python export_diann.py report.parquet --out ..\\results\\report_tables `
        --q-cutoff Global.Q.Value=off --q-cutoff Global.PG.Q.Value=off

Default cutoffs are listed in diann_tools/settings.py.
"""

import argparse
import sys

from diann_tools import export_report


def parse_cutoff(text):
    """Turn 'Q.Value=0.01' or 'Q.Value=off' into ('Q.Value', 0.01 or None)."""
    column, separator, value = text.partition("=")
    if not separator:
        raise argparse.ArgumentTypeError("use COLUMN=VALUE, for example Q.Value=0.01 or Lib.Q.Value=off")
    if value.lower() == "off":
        return column, None
    try:
        cutoff = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not a number or 'off'") from None
    if not 0 <= cutoff <= 1:
        raise argparse.ArgumentTypeError("q-value cutoffs must be between 0 and 1")
    return column, cutoff


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export unnormalized peptide and protein tables from a DIA-NN report.")
    parser.add_argument("report", help="DIA-NN main report (.parquet)")
    parser.add_argument("--out", required=True, help="new output folder")
    parser.add_argument("--protein-quantity", choices=["auto", "reported", "sum-proteotypic"],
                        help="protein intensity method (default from settings.py: auto)")
    parser.add_argument("--q-cutoff", type=parse_cutoff, action="append", default=[], metavar="COLUMN=VALUE",
                        help="override one q-value cutoff; repeat for several; VALUE may be 'off'")
    args = parser.parse_args(argv)

    try:
        export_report(args.report, args.out, dict(args.q_cutoff), args.protein_quantity)
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
