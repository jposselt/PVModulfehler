import glob
import os
import pandas as pd

def loadMultipleFilesByPattern(path):
    """
    Lädt mehrere CSV Dateien in einen Pandas Dataframe

    Parameters
    ----------
    path : String
        Dateipfad. Muster mit wildcard (*) möglich.

    Returns
    -------
    ([String], dataframe)
        Tuple aus Liste der eingelesenen Dateien und den Daten als Pandas Dataframe
    """
    files = glob.glob(os.path.join('', path))
    data = pd.concat(map(pd.read_csv, files))
    return (files, data)