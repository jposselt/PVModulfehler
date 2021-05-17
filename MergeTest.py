#%% Imports
from utils.fileUtils import loadMultipleFilesByPattern
from IPython.display import display
from datetime import datetime
from os import path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils.aiUtils as aiUtils

import json
import requests
import glob

#%% Outputgröße ändern.
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#%% Daten einlesen

# Hard coded zum Testen. (siehe auch Zeile 56)
files, data = loadMultipleFilesByPattern("../../PVDaten/Real/LimesysDataParsedTmp/1/1_Biercamp1_West_1_2019-01-01-2019-01-31_0.csv")

#%% Geographische Koordinaten
lat = str(data['Latitude_plant'].iloc[0])
lon = str(data['Longitude_plant'].iloc[0])

#%% Nicht relevante Spalten entfernen
data = data[['Time','AcPower','Edaily','Temp1','Dci','Dcp','Dcu','AnalysisGroup_string']]

#%% Ost/West Ausrichtung in Kategorie umwandel und umbenennen
data["AnalysisGroup_string"] = data["AnalysisGroup_string"].astype('category')
data["AnalysisGroup_string"] = data["AnalysisGroup_string"].cat.codes
data.rename(columns = {'AnalysisGroup_string':'Orientation'}, inplace = True)

#%% Daten in Zeitreihe umwandeln

# Time (im Format DD.MM.YY) in DatetimeIndex umwandeln
data['Time'] = pd.DatetimeIndex(data['Time'], dayfirst=True)

# Time als Index setzen.
data.set_index('Time', inplace=True)

#%% List aller Tage mit PV-Daten als datetime.datetime Objekte
days = data.index.normalize().unique().to_pydatetime()
display(days)

#%% Wetterdaten laden

# Magic Number: Das Unterverzeichnis aus dem die Solardaten stammen (siehe Zeile 24)
plantID = "1"

# Verzeichnis in dem die täglichen Wetterdaten abgelegt werden
dailyDir = "./out/tmp/"

# Pfad unter dem die Wetterdaten für alle Tage als eine CSV gespeichert werden
finalPath = "./out/final/" + plantID + "_weather.csv"

urlAdditional = "?lang=de&units=si"
urlBase = "https://api.darksky.net/forecast/"
apiKey = "799038c4e3522036d1ab6f8c64bb79b5"

counter = 0
maxcnt = len(days)
for day in days:
    counter = counter+1
    destination = dailyDir + plantID + "_" + day.strftime("%Y_%m_%d") + ".csv"
    if not path.exists(destination):
        print('Downloading Weatherdata ' + str(counter) + '/' + str(maxcnt) + " " + str(day))
        timestamp = datetime.timestamp(day)
        completeApiUrl = urlBase + apiKey + "/" + lat + "," + lon + "," + str(int(timestamp)) + urlAdditional
        request = requests.get(completeApiUrl)
        response = json.loads(request.text)
        tmpDf = pd.DataFrame(response['hourly']['data'])
        tmpDf.to_csv(destination)
    else:
        print('Found existing Weatherdata ' + str(counter) + '/' + str(maxcnt) + " " + str(day))

#%% Wetterdaten in Dataframe umwandeln

# Resampling auf 15 Minuten (wie bei Solardaten)
resampleTime = '15T'

weatherDf = pd.concat(map(pd.read_csv, glob.glob(path.join('', dailyDir + '*.csv'))))
weatherDf.fillna(0,inplace=True)
weatherDf['time'] = pd.to_datetime(weatherDf['time'],unit='s')
weatherDf = aiUtils.createTimeIndexForDataframe(weatherDf,'time')

if not resampleTime == None: 
    interploateFloats = ['visibility','windBearing','windSpeed','temperature','apparentTemperature','cloudCover','dewPoint','humidity']
    weatherDf = weatherDf.resample(resampleTime).mean()
    weatherDf[interploateFloats] = weatherDf[interploateFloats].interpolate(limit=13)
    weatherDf.fillna(method='ffill',inplace=True)
        
weatherDf = weatherDf.add_prefix('weather_')
weatherDf.to_csv(finalPath)

#%% Überflüssige Spalte entfernen
weatherDf.drop(columns=['weather_Unnamed: 0'], inplace=True)

#%% Wetter und Solardaten mergen
merged = pd.merge(data, weatherDf, left_index=True, right_index=True)
display(merged)

# %%
