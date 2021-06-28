from glob import glob
import pandas as pd
from analysis.Preprocessing import Preprocessor
from IPython.display import display

# Get list of faulty strings
faultsFiles = glob("../../PVDaten/Real/LimesysAnalyzeOutput/faultsCompact_*finish.csv")
dataframes = []
for f in faultsFiles:
    df = pd.read_csv(f)
    df = df[ (df['plantId'] == 425987) |  (df['plantId'] == 622592) ][['plantId', 'start', 'end', 'stringid']]
    dataframes.append(df)
df_faults = pd.concat(dataframes)
df_faults.reset_index()
faultyStrings = df_faults['stringid'].unique()

# free memory
del dataframes
del df_faults

# List of datasets
datasets = [
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_97a5f5a925c86b5b442f874d0760f6cb.csv", "425987", "97a5f5a925c86b5b442f874d0760f6cb"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_5523c761d21ce723767657c8615d6d23.csv", "425987", "5523c761d21ce723767657c8615d6d23"],
    ["../../PVDaten/Real/LimesysDataCleanedTmp/425987/*_f0e9ebe626b540b7fe71850b2d26acb4.csv", "425987", "f0e9ebe626b540b7fe71850b2d26acb4"],

    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_3f0162177a632253103ac85db40b4f23.csv", "622592", "3f0162177a632253103ac85db40b4f23"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_26a797f92bb1b509d8592dbded8caabc.csv", "622592", "26a797f92bb1b509d8592dbded8caabc"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_48a28befcb11c72435d8f44f435d5ad0.csv", "622592", "48a28befcb11c72435d8f44f435d5ad0"], 
    ["../../PVDaten/Real/LimesysDataCleanedTmp/622592/*_ee382cc56a3fb03a01b19cbdd49d456f.csv", "622592", "ee382cc56a3fb03a01b19cbdd49d456f"]  
]

for ds in datasets:
    path, ID, setID = ds
    print("Processing dataset: " + setID)

    # Init preprocessor
    pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")

    # Load files
    pre.loadFilesByPattern(path, ID)

    # Execute preprocessing
    columns = ['Dci','Dcu','temperature','humidity','cloudCover','uvIndex','fracMinuteOfDay','fracDayOfYear','orientation','string_id']
    pre.preprocessData(columns)
    pre.normalize(['temperature','humidity','cloudCover','uvIndex'])

    # Remove bad data
    pre.df.dropna(inplace=True)

    # Add defect category
    pre.df['defect'] = pre.df['string_id'].isin(faultyStrings)

    # Save dataframe
    pre.df.to_csv("./data/dataframes/" + ID + "_" + setID +".csv")