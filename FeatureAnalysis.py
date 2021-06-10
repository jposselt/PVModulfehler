### Generate plots for feature analysis

from analysis.Preprocessing import Preprocessor
from IPython.display import display

# Init preprocessor
pre = Preprocessor("799038c4e3522036d1ab6f8c64bb79b5", "./data/reports/")

# Load files
pre.loadFilesByPattern("../../PVDaten/Real/LimesysDataParsedTmp/1/*.csv", "1")

# Execute preprocessing
columns = ['Edaily','AcPower','Dcp','Dci','Dcu','temperature','pressure','dewPoint','humidity','cloudCover','visibility','uvIndex','windBearing','windSpeed','precipIntensity']
pre.preprocessData(columns)
pre.generatePlots(columns, "./data/plots/", pairplot=True)