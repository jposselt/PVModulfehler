import requests
import json
from datetime import datetime
import pandas as pd
from os import path
import utils.dataUtils as dataUtils


class DarkskyApiDownloader:
    """Class for interactiong with the https://darksky.net/dev API.
    """
    def __init__(self,apiKey,urlAdditional="?lang=de&units=si",urlBase = "https://api.darksky.net/forecast/"):
        """Constructor

        Args:
            apiKey (str): Your API Key for Darksky.
            urlAdditional (str, optional): Additional Parameter for the API Request. Defaults to "?lang=de&units=si".
            urlBase (str, optional): Base API Url. Defaults to "https://api.darksky.net/forecast/".
        """
        self.urlBase = urlBase
        self.apiKey = apiKey
        self.urlAdditional = urlAdditional

    def downloadWeatherData(self,lat,lon,days,destination,prefix="weatherdata_"):
        """Downloads the Weather for a list auf days

        Args:
            lat (str): Latitude of the location for the weather report
            lon (str): Longitude of the location for the weather report
            days (list[datetime]): List of days for which to get weather reports
            destination (str): The destination folder for the files, ending with /
            prefix (str, optional): Prefix for the weather report files. Defaults to "weatherdata_".

        Returns:
            list[str]: List of weather report files
        """
        counter = 0
        maxcnt = len(days)
        outFiles = []
        for day in days:
            counter = counter+1
            finalPath = destination + prefix + day.strftime("%Y_%m_%d") + '.csv'
            outFiles.append(finalPath)
            if not path.exists(finalPath):
                print('Downloading Weatherdata ' + str(counter) + '/' + str(maxcnt) + " " + str(day))
                timestamp = datetime.timestamp(day)
                completeApiUrl = self.urlBase + self.apiKey + "/" + lat + "," + lon + "," + str(int(timestamp)) + self.urlAdditional
                request = requests.get(completeApiUrl)
                response = json.loads(request.text)
                tmpDf = pd.DataFrame(response['hourly']['data'])
                tmpDf.to_csv(finalPath)
            else:
                print('Found existing Weatherdata ' + str(counter) + '/' + str(maxcnt) + " " + str(day))
        return outFiles

    def combineAndPreprocessWeatherdata(self, reports, destination=None, resampleTime=None, prefix="weather_"):
        """ Combine and preprocess weather reports

        Args:
            reports (list[str]): [description]
            destination (str, optional): [description]. Defaults to None.
            resampleTime (str, optional): [description]. Defaults to None.
            prefix (str, optional): [description]. Defaults to "weather_".

        Returns:
            dataframe: [description]
        """
        weatherDf = pd.concat(map(pd.read_csv, reports))
        weatherDf.fillna(0, inplace=True)
        weatherDf['time'] = pd.to_datetime(weatherDf['time'],unit='s')
        weatherDf = dataUtils.createTimeIndexForDataframe(weatherDf,'time')

        if not resampleTime == None: 
            interploateFloats = ['visibility','windBearing','windGust','windSpeed','temperature','apparentTemperature','pressure','cloudCover','dewPoint','humidity','uvIndex']
            weatherDf = weatherDf.resample(resampleTime).mean()
            weatherDf[interploateFloats] = weatherDf[interploateFloats].interpolate(limit=13)
            weatherDf.fillna(method='ffill', inplace=True)
        
        weatherDf = weatherDf.add_prefix(prefix)

        if not destination==None:
            weatherDf.to_csv(destination)

        return weatherDf
