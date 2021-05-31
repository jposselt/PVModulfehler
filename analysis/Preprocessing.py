import pandas as pd
from analysis.Weather import DarkskyApiDownloader
from utils.fileUtils import loadMultipleFilesByPattern

class Preprocessor:
    """Class for loading and preprocessing of data.
    """
    def __init__(self, apiKey, reportsDir):
        """Constructor

        Arguments:
            apiKey (str): Your API Key for 
            reportsDir (str): Directory where weather report files are stored, ending with /
        """
        self.df = None
        self.files = []
        self.id = ""
        self.darksky = DarkskyApiDownloader(apiKey)
        self.reportsDir = reportsDir
        
    def loadFilesByPattern(self, path, ID):
        """ Load CSV files into a dataframe

        Args:
            path (str): Path to the CSV file(s). Wildcards (*) are allowed.
            ID (str): Identifier for this set of files. Used to name output files.
        """
        self.files, self.df = loadMultipleFilesByPattern(path)
        self.id = ID

    def preprocessData(self):
        """Preprocess and add weather data

        Returns:
            dataframe: Processed dataframe
        """
        # extract geographic coordinates
        lat = str(self.df['Latitude_plant'].iloc[0])
        lon = str(self.df['Longitude_plant'].iloc[0])

        # remove unused columns
        self.df = self.df[['Time','AcPower','Edaily','Dci','Dcp','Dcu','AnalysisGroup_string']]

        # setup category for east and west orientations
        self.df["AnalysisGroup_string"] = self.df["AnalysisGroup_string"].astype('category')
        self.df.rename(columns = {'AnalysisGroup_string':'Orientation'}, inplace = True)

        # convert time column to DatetimeIndex
        self.df['Time'] = pd.DatetimeIndex(self.df['Time'], dayfirst=True)

        # make time column the index
        self.df.set_index('Time', inplace=True)

        # list all days in dataframe as datetime.datetime objects
        days = self.df.index.normalize().unique().to_pydatetime()

        # download weather reports
        prefix = "weatherdata_" + self.id + "_"
        reports = self.darksky.downloadWeatherData(lat, lon, days, self.reportsDir, prefix)

        # combine weather reports
        dataPrefix="" # prefix for column names
        weather = self.darksky.combineAndPreprocessWeatherdata(reports, resampleTime='15T', prefix=dataPrefix)

        # remove unused column
        weather.drop(columns=[dataPrefix + 'Unnamed: 0'], inplace=True)

        # mergen dataframes
        self.df = pd.merge(self.df, weather, left_index=True, right_index=True)

        return self.df

    
    def generatePlots(self, destination, columns):
        # TODO:
        #   distributions plots (https://seaborn.pydata.org/generated/seaborn.displot.html)                                 Dominik
        #   boxplots (https://seaborn.pydata.org/generated/seaborn.boxplot.html)                                            Marius
        #   violin plots (https://seaborn.pydata.org/generated/seaborn.violinplot.html)                                     Niklas
        #   corrolation heatmap (https://seaborn.pydata.org/generated/seaborn.heatmap.html)                                 Tristan
        #   bivariate plots (https://seaborn.pydata.org/examples/layered_bivariate_plot.html)                               Jonas
        #   pair plots (https://seaborn.pydata.org/generated/seaborn.pairplot.html)                                         Jonas
        #   linear regression with marginal distributions (https://seaborn.pydata.org/examples/regression_marginals.html)   Dominik

        for col in columns:
            for row in columns:
                if row == col:
                    # TODO: univariate plots
                    pass
                else:
                    # TODO: bivariate plots
                    pass


    def restrictDaytimeInterval(self, startTime, endTime):
        pass


    def saveDataframe(self, path):
        """Save dataframe as HDF5 file.

        Arguments:
            path (str): The destination folder for the file, ending with /
        """
        store = pd.HDFStore(path + self.id + '.h5')
        store['df'] = df


    def loadDataframe(self, path):
        """Load dataframe from HDF5 file.

        Args:
            path (str): Path to HDF5 file

        Returns:
            dataframe: Dataframe
        """
        store = pd.HDFStore(path)
        return store['df']