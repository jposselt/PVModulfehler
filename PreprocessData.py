# This script processes set of initial data files, prunes unnecessary columns and merges weather information.
# The results are stored in CSV files (one for each set of files)

from glob import glob
import pandas as pd
from analysis.Preprocessing import Preprocessor

# Get list of faulty strings
faultsFiles = glob("../../PVDaten/Real/LimesysAnalyzeOutput/faultsCompact_*finish.csv")
dataframes = []
for f in faultsFiles:
    df = pd.read_csv(f)
    df = df[ (df['plantId'] == 425987) |  (df['plantId'] == 622592) |  (df['plantId'] == 1081347) ][['plantId', 'start', 'end', 'stringid']]
    dataframes.append(df)
df_faults = pd.concat(dataframes)
df_faults.reset_index()
faultyStrings = df_faults['stringid'].unique()

# manually free memory
del dataframes
del df_faults

# List of datasets ([Path in directory, ID of string, setID id of set])
# NOTE: If you are processing cleaned data (from the LimesysDataCleanedTmp folder) the required weather reports must already be present in
# the folder given to the Preprocessor below since these data files do not contain location coordinates.
datasets = [
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_97a5f5a925c86b5b442f874d0760f6cb.csv", "425987", "97a5f5a925c86b5b442f874d0760f6cb"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_5523c761d21ce723767657c8615d6d23.csv", "425987", "5523c761d21ce723767657c8615d6d23"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_f0e9ebe626b540b7fe71850b2d26acb4.csv", "425987", "f0e9ebe626b540b7fe71850b2d26acb4"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_3f0162177a632253103ac85db40b4f23.csv", "622592", "3f0162177a632253103ac85db40b4f23"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_26a797f92bb1b509d8592dbded8caabc.csv", "622592", "26a797f92bb1b509d8592dbded8caabc"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_48a28befcb11c72435d8f44f435d5ad0.csv", "622592", "48a28befcb11c72435d8f44f435d5ad0"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_ee382cc56a3fb03a01b19cbdd49d456f.csv", "622592", "ee382cc56a3fb03a01b19cbdd49d456f"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/1081347/*_f55054c9be71ab6580aa39aea9b81e69.csv", "1081347", "f55054c9be71ab6580aa39aea9b81e69"]
]

for ds in datasets:
    path, ID, setID = ds
    print("Processing dataset: " + setID)

    # Init preprocessor
    pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")

    # Load files into preprocessor with preset path and string ID
    pre.loadFilesByPattern(path, ID)

    # Execute preprocessing
    columns = ['Dci','Dcu','temperature','humidity','cloudCover','uvIndex','minuteOfDay','fracMinuteOfDay','fracDayOfYear','orientation','string_id']

    pre.preprocessData(columns)
    pre.normalize(['temperature','humidity','cloudCover','uvIndex'])

    # Remove invalid data
    pre.df.dropna(inplace=True)

    # Add defect category for later classification
    pre.df['defect'] = pre.df['string_id'].isin(faultyStrings)

    # Save dataframe in csv file (static path)
    pre.df.to_csv("./data/paper/dataframes/" + ID + "_" + setID +".csv")

    # Counts
    print(ID + "_" + setID + ":\n")
    print(pre.df.count())

    print("\nDefect Counts:\n")
    print(pre.df['defect'].value_counts())
