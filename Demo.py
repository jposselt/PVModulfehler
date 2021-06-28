
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
timeSeriesData = timeSeriesData[
    [
        'Time',
        'AcPower',
        'Edaily',
        'Temp1',
        'Dci',
        'Dcp',
        'Dcu'
    ]
]
display(timeSeriesData)

#%% Datentypen auslesen.
display(timeSeriesData.dtypes)

#===========================================================================================================
#Timeseries erstellen.
#Wird eine CSV mit Pandas geladen, ist das Dataframe erstmal eine gewöhnliche Series.
#Wir müssen den Zeitindex selbst erstellen.

#%% time Spalte zu Datetime casten.
timeSeriesData['Time'] = pd.DatetimeIndex(timeSeriesData['Time'])
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
timeSeriesData['day'] = timeSeriesData.index.day

# Zufällig 5 Datensätze anzeigen.
display(timeSeriesData.sample(5, random_state=0))

# %%
#%% Selektion von Zeiträumen (1 Tag).
display(timeSeriesData.loc['2019-07-15'])

#%% Plotten
#Die X Achse wird automatisch generiert.
timeSeriesData.loc['2019-07-15']['AcPower'].plot()

#===========================================================================================================
#Fehlersuche

#%%
# Gibt es fehlende Werte?
timeSeriesData.isnull().any()

#%%
# Prüfe Datumsangaben
display(np.sort(timeSeriesData['Year'].unique()))  # Erwartet: [2019]
display(np.sort(timeSeriesData['Month'].unique())) # Erwartet: [7]
display(np.sort(timeSeriesData['day'].unique()))   # Erwartet: [1, ..., 29]

#%%
# Tag- und Monatswerte entsprechen nicht den Erwartungen.
# Plotten der Häufigkeiten der Monatswerte:
timeSeriesData['Month'].value_counts(normalize=True).sort_index().plot.bar()

#%%
# Das Gleiche noch mal für Tage
timeSeriesData['day'].value_counts(normalize=True).sort_index().plot.bar()

#%%
# Wie sich herausstellt sind einige der Monats und Tageswerte vertauscht. Ursache dafür ist
# Konvertierung der ursprünglichen Zeitangaben im Format dd.mm.yy HH:MM mit DatetimeIndex().
# Diese Methode geht vom Format YY-MM-DD aus. Statt dessen müsste man die Methode to_datetime()
# verwenden und das Eingabeformat als Parameter übergeben.

#timeSeriesData['Time'] = pd.DatetimeIndex(timeSeriesData['Time']) # FALSCH
#timeSeriesData['Time'] = pd.to_datetime(timeSeriesData['Time'], format='%d.%m.%y %H:%M') # RICHTIG
