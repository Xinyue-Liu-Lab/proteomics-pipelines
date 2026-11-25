"""Export unnormalized peptide and protein tables from DIA-NN main reports.

Modules, in the order the export uses them:

    settings    default cutoffs, contaminant pattern and column lists
    reader      read and check the .parquet report
    filters     remove decoys and contaminants, apply q-value cutoffs
    mass_error  MS1/MS2 ppm errors and observed precursor m/z
    tables      peptide and protein tables for one run
    summary     one run_summary.tsv row per run
    export      ties the steps together and writes the files

Typical use:

    from diann_tools import export_report
    export_report("report.parquet", "report_tables")
"""

from .export import export_report

__all__ = ["export_report"]
