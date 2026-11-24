# configs/diann/

Keep one record per DIA-NN search so that every result can be traced back to its exact settings. A convenient format is a short Markdown or text file named after the search, e.g., `2026-12-01_pilot-search.md`, together with the DIA-NN log file (e.g., `report.log.txt`, which is small and may be committed).

Each record should state:

- **DIA-NN version**
- **Input**: acquisition method (e.g., dia-PASEF window scheme) and the location of the raw files on lab storage
- **Spectral library**: library-free (predicted from FASTA) or empirical, and its location
- **Sequence database**: source and release (e.g., UniProt release, reviewed only or not, contaminant list)
- **Key settings**: enzyme and missed cleavages, modifications, precursor and fragment ranges, mass accuracy, match-between-runs, quantification strategy
- **Full command line** or the settings exported from the DIA-NN interface
