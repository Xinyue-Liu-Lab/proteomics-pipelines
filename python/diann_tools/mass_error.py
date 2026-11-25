"""Mass error (ppm) and observed precursor m/z.

    MS1.PPM                = 1e6 * Ms1.Apex.Mz.Delta / Precursor.Mz
    MS2.Best.Fragment.PPM  = 1e6 * Best.Fr.Mz.Delta  / Best.Fr.Mz
    Observed.Precursor.Mz  = Precursor.Mz + Ms1.Apex.Mz.Delta

MS1 values are kept only where DIA-NN found an MS1 apex (Ms1.Apex.Area > 0).
"""

import numpy as np
import pandas as pd


def column_or_nan(frame, column):
    """Return a column as float64, or an all-missing column if the report lacks it."""
    if column in frame.columns:
        return frame[column].astype("float64")
    return pd.Series(np.nan, index=frame.index)


def ppm(delta, reference_mz):
    """Signed mass error in ppm; missing where the reference m/z is not positive or a value is not finite."""
    error = 1e6 * delta / reference_mz.where(reference_mz > 0)
    return error.where(np.isfinite(error))


def add_mass_columns(precursors):
    """Add MS1.PPM, MS2.Best.Fragment.PPM and Observed.Precursor.Mz to the passing precursors."""
    precursor_mz = column_or_nan(precursors, "Precursor.Mz")
    ms1_delta = column_or_nan(precursors, "Ms1.Apex.Mz.Delta")
    has_ms1_apex = column_or_nan(precursors, "Ms1.Apex.Area") > 0

    ms1_ppm = ppm(ms1_delta, precursor_mz).where(has_ms1_apex)
    precursors["MS1.PPM"] = ms1_ppm
    precursors["MS2.Best.Fragment.PPM"] = ppm(
        column_or_nan(precursors, "Best.Fr.Mz.Delta"), column_or_nan(precursors, "Best.Fr.Mz")
    )
    # Observed m/z is reported only when the MS1 error itself is valid.
    precursors["Observed.Precursor.Mz"] = (precursor_mz + ms1_delta).where(ms1_ppm.notna())
    return precursors
