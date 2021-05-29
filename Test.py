from analysis.Preprocessing import Preprocessor
from IPython.display import display

pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")
pre.loadFilesByPattern("../../PVDaten/Real/LimesysDataParsedTmp/1/1_Biercamp1_West_1_2019-07-01-2019-07-31_0.csv", "1")
df = pre.preprocessData()

print(pre.files)
display(pre.df)