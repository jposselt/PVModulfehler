"""
"  python script to extract data from csv files into pandas dataframe
"  The script supplies a class to extract the data from specially formatted csv files.
"  It additionaly defines a function with which multiple scatterplots can be performed
"  Script: plot_simulation.py
"  Version: 1.1
"""

import matplotlib.pyplot as plt
import datetime
import pandas

class DataFetcherSimulated:
    """CLASS DataFetcherSimulated
    "  DataFetcherSimulated is used to extact data from the given csv files
    "  file_name: the name to the input csv file with simulated data
    "  sheet_name: the name of the sheet within the file
    "  columns: the columns which will be evaluated
    """
    def __init__(self, file_name, sheet_name, columns):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.columns = columns
        self.extract_info()
        self.extract_data()

    """ FUNCTION extract_info
    "   This function is used to retreive the info about the photovoltaik system in question.
    "   It retreives the data from within the class
    """
    def extract_info(self):
        info = pandas.read_excel(self.file_name, sheet_name=self.sheet_name, usecols="A,B")
        self.info = {}
        for row in range(info.shape[0]):
            if not info.iat[row, 0] == None:
                self.info[info.iat[row, 0]] = info.iat[row, 1]
    
    """FUNCTION extract_data
    "  The function extract_data extracts raw data from the given file and preprocesses it
    "  with given options to create a pandas data frame that will be stored class internally.
    """
    def extract_data(self):
        raw_data = pandas.DataFrame(pandas.read_excel(self.file_name, sheet_name=self.sheet_name, skiprows=3, usecols="H,I,J,K,L,M,N"))
        day = 1
        old_time = datetime.time(0)
        for row in range(raw_data.shape[0]):
            if raw_data.iat[row, 0] < old_time:
                day += 1
            old_time = raw_data.iat[row, 0]
            raw_data.iat[row, 0] = datetime.datetime.combine(datetime.date(year=2021, month=1, day=day), raw_data.iat[row, 0])

        self.data = pandas.DataFrame(raw_data, columns=self.columns)
    
    """FUNCTION plot_data
    "   This function supplies an easy plot with predetermined parameters
    """
    def plot_data(self):
        self.data.plot(subplots=True, x='Time', legend=True, figsize=(60, 30), title=self.info['Faults：'], fontsize=30, grid=True, xlabel='Time')

    """FUNCTION scatter_plot
    "   the function scatter_plot can plot data with predetermined parameters
    "   Return: the plot that can then be processed further
    """
    def scatter_plot(self, x, y):
        title = "Scatterplot " + y + " over " + x
        return self.data.plot(subplots=True, x=x, y=y, legend=True, figsize=(60, 30), title=title, fontsize=30, grid=True, xlabel=x, ylabel=y, kind='scatter')

"""FUNCTION plot_mult
"   This function can plot multiple values at ones
"   It utilizes pyplot.
"""
def plot_mult(objs, x, y, title='', xlabel='', ylabel=''):
    for ob in objs:
        plt.scatter(ob.data[x], ob.data[y], s=1)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

#df_shade = DataFetcherSimulated(r'../Daten_Simuliert/daten_schatten.xls', '1subs_fixed shadow', ['Time', 'S', 'T', 'S1', 'P', 'V', 'I'])

#df_shade.extract_data()
#print(df_shade.info)
#print(df_shade.data)
#df_shade.plot_data()
