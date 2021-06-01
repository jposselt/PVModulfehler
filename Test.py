from analysis.Preprocessing import Preprocessor
from IPython.display import display

pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")
pre.loadFilesByPattern("../../PVDaten/Real/LimesysDataParsedTmp/1/1_Biercamp1_West_1_*.csv", "1")
df = pre.preprocessData()

columns = ['Edaily','AcPower','Dcp','Dci','Dcu','temperature','pressure','dewPoint','humidity','cloudCover','visibility','uvIndex','windBearing','windSpeed','precipIntensity']
pre.generatePlots(columns, "./data/plots/")

display(pre.df)