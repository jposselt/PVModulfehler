import os
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

    def preprocessData(self, keepColumns):
        """Preprocess and add weather data

        Args:
            keepColumns (list[str]): Keep these columns at the end.

        Returns:
            dataframe: Processed dataframe
        """
        # setup category for east and west orientations
        self.df["AnalysisGroup_string"] = self.df["AnalysisGroup_string"].astype('category')
        self.df.rename(columns = {'AnalysisGroup_string':'orientation'}, inplace = True)

        # convert time column to DatetimeIndex
        self.df['Time'] = pd.DatetimeIndex(self.df['Time'], dayfirst=True)

        # make time column the index
        self.df.set_index('Time', inplace=True)

        # create time based columns
        self.df['minuteOfDay']     = self.df.index.hour * 60 + self.df.index.minute
        self.df['dayOfYear']       = self.df.index.dayofyear
        self.df['year']            = self.df.index.year
        self.df['fracMinuteOfDay'] = self.df['minuteOfDay'] / (60*24)
        self.df['fracDayOfYear']   = self.df.apply(fracDayOfYear, axis=1)

        # list all days in dataframe as datetime.datetime objects
        days = self.df.index.normalize().unique().to_pydatetime()

        # download weather reports
        reports = []
        prefix = "weatherdata_" + self.id + "_"
        if 'Latitude_plant' in self.df.columns and 'Longitude_plant' in self.df.columns:
            # extract geographic coordinates
            lat = str(self.df['Latitude_plant'].iloc[0])
            lon = str(self.df['Longitude_plant'].iloc[0])
            reports = self.darksky.downloadWeatherData(lat, lon, days, self.reportsDir, prefix)
        else:
            print("No location data found. No weather data can be downloaded. There may be existing data, though.")

        # combine weather reports
        if reports:
            weather = self.darksky.combineAndPreprocessWeatherdata(reports, resampleTime='15T', prefix="")
        else:
            print("Searching for existing weather data.")
            for day in days:
                filePath = self.reportsDir + prefix + day.strftime("%Y_%m_%d") + '.csv'
                if os.path.isfile(filePath):
                    reports.append(filePath)
                else:
                    print("No weather data found for date " + day.strftime("%Y_%m_%d"))
            weather = self.darksky.combineAndPreprocessWeatherdata(reports, resampleTime='15T', prefix="")

        # mergen dataframes
        self.df = pd.merge(self.df, weather, left_index=True, right_index=True)

        # remove columns
        self.df = self.df[keepColumns]

        return self.df


    def normalize(self, columns):
        """Normalize data columns

        Args:
            columns (list[sting]): Data columns to normalize
        """
        for col in columns:
            max_value = self.df[col].max()
            min_value = self.df[col].min()
            self.df[col] = (self.df[col] - min_value) / (max_value - min_value)


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
    

    def generateCorrelationHeatmap(self, columns, destination, xsize=10, ysize=10):
        """Generate a heatmap for the correlation matrix

        Args:
            columns (list[str]): List of variables included in plot
            destination (str): Destination folder for resulting plot
            size (int, optional): Figure width and height in inches. Defaults to 10.

        Returns:
            dataframe: Correlation matrix
        """
        sns.set(font_scale=1.4)
        fig, ax = plt.subplots(figsize=(xsize,ysize))
        corrMatrix = self.df[columns].corr()
        heatmap = sns.heatmap(corrMatrix, center=0, annot=True, linewidths=.5, ax=ax)
        fig.savefig(destination + "Heatmap.png")
        plt.close(fig)
        return corrMatrix


    def generateRegressionPlot(self, x, y, destination, size=10, style="darkgrid"):
        """Generate regression plot

        Args:
            x (string): Data columns used as x-axis
            y (string): Data columns used as y-axis
            destination (string): Destination folder for resulting plot
            size (int, optional): Size of the generated plot in inches. Defaults to 10.
            style (str, optional): Style of the generated plot. Defaults to "darkgrid".
        """
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
        """Generate various plots illustrating relationsships between data columns

        Args:
            columns (list[string]): List of data columns to use
            destination (string): Path to folder for resulting plots
            heatmap (bool, optional): Generate a heatmap of correlation coefficients. Defaults to True.
            regplot (bool, optional): Generate regression plots. Defaults to True.
            pairplot (bool, optional): Generate matrix of pair plots. Defaults to False.
            biplot (bool, optional): Generate bivariate distribution plots. Defaults to True.
        """
        if heatmap:
            self.generateCorrelationHeatmap(columns, destination, 12, 12)

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
        """Restrict data to certain daytime hours

        Args:
            startTime (datetime.time or str): Initial time as a time filter limit
            endTime (datetime.time or str): End time as a time filter limit

        Returns:
            dataframe: restricted dataframe
        """
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

def isleap(year):
    """Check leap year

    Args:
        year (int): Year

    Returns:
        bool: True if input is a leap year
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def fracDayOfYear(row):
    """Calculate fractional day of year

    Args:
        row (?): Dataframe row

    Returns:
        float: fractional day of year
    """
    nDays = 365
    if isleap(row['year']):
        nDays = 366
    return row['dayOfYear'] / nDays