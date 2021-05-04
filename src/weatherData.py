#%% Imports
import csv
import datetime
import json
import sys
import time
import tensorflow as tf
from tensorflow import keras
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


#Eigene Libs laden in IPython.
sys.path.append("pfad/zu/eurem/libs/ordner/wenn/vorhanden/")

#===========================================================================================================
#%%Darksky API verwenden.

WEATHER_API_URL_BASE = "https://api.darksky.net/forecast/"
WEATHER_API_KEY = "-"
WEATHER_API_ADDS = "?lang=de&units=si"

#Minden Campus
lat = "52.296449"
lon = "8.904943"
time = "1533168200"

completeApiUrl = WEATHER_API_URL_BASE + WEATHER_API_KEY + "/" + lat + "," + lon + "," + time + WEATHER_API_ADDS
print(completeApiUrl)
request = requests.get(completeApiUrl)
response = json.loads(request.text)
print(response)

#%%Wetterdaten als Dataframe.
weatherAsDataframe = pd.DataFrame(response['hourly']['data'])
print(weatherAsDataframe)

#===========================================================================================================
#Timeseries mit Pandas verwenden.

#%% CSV laden.
dataPath = "pfad/zu/deiner/datei/"
timeSeriesData = pd.read_csv(dataPath)
print(timeSeriesData)

#%% Daten ein bisschen hübsch machen <3

#Outputgröße ändern.
pd.set_option('print.max_rows', 500)
pd.set_option('print.max_columns', 500)
pd.set_option('print.width', 1000)

#Zellen umbenennen.
timeSeriesData = timeSeriesData.rename(columns = {"Unnamed: 0": "time"}) 

#Selektion der Daten für das Beispiel.
timeSeriesData = timeSeriesData[['time','voltage','temperature','string_current']]
print(timeSeriesData)

#%% Datentypen auslesen.
print(timeSeriesData.dtypes)

#===========================================================================================================
#Timeseries erstellen.
#Wird eine CSV mit Pandas geladen, ist das Dataframe erstmal eine gewöhnliche Series.
#Wir müssen den Zeitindex selbst erstellen.

#%% time Spalte zu Datetime casten.
timeSeriesData['time'] = pd.DatetimeIndex(timeSeriesData['time'])
print(timeSeriesData.dtypes)

#%% time als Index setzen.
timeSeriesData.set_index('time', inplace=True)
print(timeSeriesData)
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
print(timeSeriesData.sample(5, random_state=0))

#%% Selektion von Zeiträumen (1 Tag).
print(timeSeriesData.loc['2018-08-22'])

#%% Selektion von Zeiträumen (Zeitspanne).
print(timeSeriesData.loc['2018-08-22 09:00':'2018-08-22 17:00'])
#Es ist auch möglich, den Tag nicht anzugeben, um einen ganzen Monat zu selektieren.

#%% Plotten
#Die X Achse wird automatisch generiert.
timeSeriesData.loc['2018-08-12']['voltage'].plot()

#%% Plotten, mehrere Tage.
timeSeriesData.loc['2018-08-12':'2018-08-13']['string_current'].plot()

#%% Plotten, mehrere Tage mit Subplots.
timeSeriesData.loc['2018-08-12':'2018-08-13'].plot(subplots=True,figsize=(11, 9))
#Tipp: Seaborn oder Plotly ansehen!

#%% Frequenzen- wir können Daten explizit mit einer bestimmten Frequenz ansprechen.
#Beispieldaten selektieren.
tmpData = timeSeriesData.loc['2018-08-12', ['string_current']].copy()
print(tmpData)

#%% Alle 4 Minuten.
tmpData_4min = tmpData.asfreq('4T')
print(tmpData_4min)

#%% Lücken füllen.
tmpData_4min['string_current fill'] = tmpData.asfreq('4T',method='ffill')
print(tmpData_4min)

#%% Resampling- die Frequenz der Daten nach oben oder unten ändern.
# Dafür kann die Resample Funktion genutzt werden. Sie bietet wesentlich mehr Kontrolle und Funktionen, als 
# die vorherige Variante.
tmpData_hourly = timeSeriesData.resample('H').mean()
print(tmpData_hourly)
#Hierbei wird ein Zeitindex erstellt und die Daten per Aggregation zugeordnet.
#Dadurch entstehen aber auch Lücken. Diese können gewollt sein oder müssen gefüllt werden.
#Siehe Dokumentation.

# %% Rolling windows- eine Variante, um Zeitabschnitte zu verarbeiten.
#Dadurch können zum Beispiel Trends visualisiert werden.
rollingAvgVoltage = timeSeriesData['voltage'].rolling(7, center=True).mean()
print(rollingAvgVoltage.head(30))

#%% Rolling window. 
timeSeriesDataSelection = timeSeriesData.loc['2018-08-13']['string_current']
rollingAvgVoltage = timeSeriesDataSelection.rolling(30, center=True).mean()
fig, ax = plt.subplots(figsize=(11, 9))
ax.plot(timeSeriesDataSelection,
marker='.', linestyle='-', linewidth=0.5, label='string_current')
ax.plot(rollingAvgVoltage,
marker='o', markersize=5, linestyle='-', label='string_current Trend')
ax.legend();
#%%