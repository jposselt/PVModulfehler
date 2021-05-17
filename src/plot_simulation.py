import matplotlib.pyplot as plt
import datetime
import pandas

class DataFetcherSimulated:
    """Class is used to extact data from the given csv files 
    """
    def __init__(self, file_name, sheet_name, columns):
        self.file_name = file_name
        self.sheet_name = sheet_name
        self.columns = columns
        self.extract_info()
        self.extract_data()

    def extract_info(self):
        info = pandas.read_excel(self.file_name, sheet_name=self.sheet_name, usecols="A,B")
        self.info = {}
        for row in range(info.shape[0]):
            if not info.iat[row, 0] == None:
                self.info[info.iat[row, 0]] = info.iat[row, 1]
    
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
    
    def plot_data(self):
        self.data.plot(subplots=True, x='Time', legend=True, figsize=(60, 30), title=self.info['Faults：'], fontsize=30, grid=True, xlabel='Time')


    def scatter_plot(self, x, y):
        title = "Scatterplot " + y + " over " + x
        return self.data.plot(subplots=True, x=x, y=y, legend=True, figsize=(60, 30), title=title, fontsize=30, grid=True, xlabel=x, ylabel=y, kind='scatter')


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
