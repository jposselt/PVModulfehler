#%% Imports
import datetime
import time
import json
import matplotlib as mlp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from IPython.display import display

#===========================================================================================================
#%% Konverter-Funktion

def dateToUnixTime(date):
    """
    Wandelt eine Datum + Uhrzeit in den entsprechenden Unix-Zeitstempel um

    Parameters
    ----------
    date : datetime.datetime
        Datum und Uhrzeit

    Returns
    -------
    int
        Unix-Zeitstempel in Sekunden seit 1.1.1970
    """
    return int(time.mktime(date.timetuple()))

#===========================================================================================================
#%% Darksky API Parameter

WEATHER_API_URL_BASE = "https://api.darksky.net/forecast/"
WEATHER_API_KEY = "799038c4e3522036d1ab6f8c64bb79b5"
WEATHER_API_ADDS = "?lang=de&units=si"

# Minden Campus Koordinaten
lat = "52.296449"
lon = "8.904943"

# Datum der Analyse als Unix-Zeitstempel
date = datetime.datetime(2018, 8, 2)
timestamp = dateToUnixTime(date)
display(timestamp)

#===========================================================================================================
#%% Wetterdaten anfordern
completeApiUrl = WEATHER_API_URL_BASE + WEATHER_API_KEY + "/" + lat + "," + lon + "," + str(timestamp) + WEATHER_API_ADDS
display(completeApiUrl)
request = requests.get(completeApiUrl)
response = json.loads(request.text)

#===========================================================================================================
#%% Wetterdaten als 2D Pandas Dataframe
weatherAsDataframe = pd.DataFrame(response['hourly']['data'])

#===========================================================================================================
#%% Unix-Zeitstempel in Datetime umwandeln
weatherAsDataframe['time'] = pd.to_datetime(weatherAsDataframe['time'],unit='s')

#===========================================================================================================
#%% Zeit als Index setzen
weatherAsDataframe.set_index('time', inplace=True)

#===========================================================================================================
#%% Dataframe anzeigen
display(weatherAsDataframe)

#===========================================================================================================
#%% Alle Spalten plotten
weatherAsDataframe.plot(subplots=True,figsize=(11, 9))