import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from analysis.Weather import DarkskyApiDownloader
from utils.fileUtils import loadMultipleFilesByPattern

from IPython.display import display

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
        self.df = self.df[['Time','AcPower','Edaily','Dci','Dcp','Dcu','AnalysisGroup_string','string_id']]

        # setup category for east and west orientations
        self.df["AnalysisGroup_string"] = self.df["AnalysisGroup_string"].astype('category')
        self.df.rename(columns = {'AnalysisGroup_string':'orientation'}, inplace = True)

        # convert time column to DatetimeIndex
        self.df['Time'] = pd.DatetimeIndex(self.df['Time'], dayfirst=True)

        # make time column the index
        self.df.set_index('Time', inplace=True)

        # create time based columns
        self.df['minuteOfDay'] = self.df.index.hour * 60 + self.df.index.minute
        self.df['dayOfYear']   = self.df.index.dayofyear
        self.df['weekOfYear']  = self.df.index.week

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


    def generateBivariatePlot(self, x, y, destination, size_x=6, size_y=6, style="dark"):
        """Generate bivariate distribution plot

        Args:
            x (str): Variables that specifies positions on the x axes.
            y (str): Variables that specifies positions on the y axes.
            destination (str): Destination folder for resulting plot
            size_x (int, optional): Figure width in inches. Defaults to 6.
            size_y (int, optional): Figure height in inches. Defaults to 6.
            style (str, optional): Style option passed to seaborn. Defaults to "dark".
        """
        sns.set_theme(style=style)
        fig, ax = plt.subplots(figsize=(size_x, size_y))
        sns.scatterplot(x=x, y=y, data=self.df)
        sns.histplot(x=x, y=y, data=self.df, bins=50, pthresh=.1, cmap="mako")
        sns.kdeplot(x=x, y=y, data=self.df, levels=5, color="w", linewidths=1)
        fig.savefig(destination + x + "_" + y + ".png")
        plt.close(fig)


    def generatePairplot(self, columns, destination):
        """Generate plot of pairwise relationships in a dataset.

        Args:
            columns (list[str]): List of variables included in plot
            destination (str): Destination folder for resulting plot
        """
        plot = sns.pairplot(self.df[columns], diag_kind="kde")
        plot.map_lower(sns.kdeplot, levels=4, color=".2")
        plot.savefig(destination + "Pairplot.png")
        plt.close(plot.fig)
    

    def generateCorrelationHeatmap(self, columns, destination, size=10):
        """Generate a heatmap for the correlation matrix

        Args:
            columns (list[str]): List of variables included in plot
            destination (str): Destination folder for resulting plot
            size (int, optional): Figure width and height in inches. Defaults to 10.

        Returns:
            dataframe: Correlation matrix
        """
        fig, ax = plt.subplots(figsize=(size,size))
        corrMatrix = self.df[columns].corr()
        heatmap = sns.heatmap(corrMatrix, center=0, annot=True, linewidths=.5, ax=ax)
        fig.savefig(destination + "Heatmap.png")
        plt.close(fig)
        return corrMatrix


    def generateRegressionPlot(self, x, y, destination, size=10, style="darkgrid"):
        sns.set_theme(style=style)
        plot = sns.jointplot(
            x=x, y=y,
            data=self.df, 
            kind="reg",
            truncate=False,
            color="m",
            height=size
        )
        plot.savefig(destination + x + "_" + y + "_regression.png")
        plt.close(plot.fig)
        

    def generatePlots(self, columns, destination, heatmap=True, regplot=True, pairplot=False, biplot=True):
        if heatmap:
            self.generateCorrelationHeatmap(columns, destination, 12)

        if pairplot:
            self.generatePairplot(columns, destination)
        
        for col in columns:
            for row in columns:
                if row == col:
                    # TODO: univariate plots
                    pass
                else:
                    if regplot:
                        self.generateRegressionPlot(row, col, destination)
                    if biplot:
                        self.generateBivariatePlot(row, col, destination)


    def restrictDaytimeInterval(self, startTime, endTime):
        return self.df.between_time(startTime, endTime)


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