#%% Imports
import csv
import datetime
import json
import sys
import time
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from IPython.display import display

#===========================================================================================================
#Timeseries mit Pandas verwenden.

#%% CSV laden.
dataPath = "BeispieldatenPv/655364/655364_WR_7_Harsch_1_2019-07-01-2019-07-29_2.csv"
timeSeriesData = pd.read_csv(dataPath)
display(timeSeriesData)

#%% Daten ein bisschen hübsch machen <3

#Outputgröße ändern.
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Selektion der Daten für das Beispiel.
timeSeriesData = timeSeriesData[['Time','AcPower','Edaily','Temp1','Dci','Dcp','Dcu']]
display(timeSeriesData)

#%% Datentypen auslesen.
display(timeSeriesData.dtypes)

#===========================================================================================================
#Timeseries erstellen.
#Wird eine CSV mit Pandas geladen, ist das Dataframe erstmal eine gewöhnliche Series.
#Wir müssen den Zeitindex selbst erstellen.

#%% time Spalte in Datetime Objekt umwandel.
# Das Datum in time Spalte ist nicht im Datetime-Standardformat (YY-MM-DD). Einfaches Casten würde zu
# Konvertierungsfehlern führen. Statt dessen muss das Eingabeformat mit angegeben werden.
timeSeriesData['Time'] = pd.to_datetime(timeSeriesData['Time'], format='%d.%m.%y %H:%M')
display(timeSeriesData.dtypes)

#%% time als Index setzen.
timeSeriesData.set_index('Time', inplace=True)
display(timeSeriesData)
# Alternative : pd.read_csv(dataPath, index_col=0, parse_dates=True).
# Oft werden vorher mehrere Dataframes konsolidiert. Deshalb muss der Index meistens später angelget werden.

#===========================================================================================================
#Pandas Timeseries Funktionen.

#%% Datetime Funktionen.
# Felder basierend auf der Zeit anlegen.
timeSeriesData['Year'] = timeSeriesData.index.year
timeSeriesData['Month'] = timeSeriesData.index.month
timeSeriesData['Day'] = timeSeriesData.index.day

#%% Plotten
columns = timeSeriesData.columns.difference(['Year', 'Month', 'Day']) # exclude columns
timeSeriesData.loc['2019-07-15'][columns].plot(subplots=True, figsize=(11, 9))

#%% Alle Tage als Subplots
grouped = timeSeriesData.groupby('Day')['AcPower']
rowlength = 7
rows=int(np.ceil(grouped.ngroups/7))
fig, axs = plt.subplots(figsize=(9,4), 
                        nrows=rows, ncols=rowlength,
                        gridspec_kw=dict(hspace=0.4))

targets = zip(grouped.groups.keys(), axs.flatten())
for i, (key, ax) in enumerate(targets):
    ax.plot(grouped.get_group(key))
ax.legend()
plt.show()