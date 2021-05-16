import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime as dt
from darksky import forecast

# Key
key = "799038c4e3522036d1ab6f8c64bb79b5"

# Lade die Daten, vielleicht in Zukunft mit pyocclient aus sciebo? Erste Versuche haben nichtr geklappt
filePath = "data/32771/32771_WR2_1200_Westgaube_1_2019-01-01-2019-01-31_0.csv"
timeSeriesData = pd.read_csv(filePath)
timeSeriesData = timeSeriesData[['Time','AcPower','Edaily','Temp1','Dci','Dcp','Dcu', 'Latitude_plant', 'Longitude_plant']]
timeSeriesData['Time'] = pd.to_datetime(timeSeriesData['Time'], format='%d.%m.%y %H:%M')

# Die Zeit wird zur Indizierung verwendet und hierfür verwendet
timeSeriesData.set_index('Time', inplace=True)
timeSeriesData.sort_index(0)

latitude = timeSeriesData["Latitude_plant"][0]
longitude = timeSeriesData["Longitude_plant"][0]

# Mittels groupby können die einzelnen Tage dargestellt werden
for index, day in timeSeriesData.groupby(timeSeriesData.index.date):
    # Das 15 min Intervall ist äußerst grob und liefert pro Tag ungefähr 30-40 Werte
    # Die Aufnahme startet je nach Fall früher oder später -> Wir nehmen maximalen Zeitraum von z.B 5:00 bis 22:00 an. Nicht gegebene Werte müssen gefüllt werrden (z.B. null)
    # Ein Tag hat demnach (17*60)/15 = 68 Merkmalsvektoren
    # Jeder Merkmalsvektore besitzt die Inhalte 'AcPower','Edaily','Temp1','Dci','Dcp','Dcu' und Wetterdaten 
    # Und dann Normalisieren und dann Hauptkomponentenanalyse für jeden Zeitpunkt vielleicht?
    plantForecast = forecast(key, latitude, longitude, time=day.index[0].isoformat())
    print(plantForecast.hourly.data[0].temperature)
    exit()

plt.show()