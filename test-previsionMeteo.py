#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import requests
import requests_cache
import json
from datetime import datetime
from datetime import timedelta

# Import general config
import config


# Setting up a cache for requests ======================================================================================
requests_cache.install_cache('opeWeatherCache', expire_after=timedelta(minutes=15))



# Requete pour récupérer le temps actuel à Plabennec ===================================================================
try:
    weather     = requests.get("http://api.openweathermap.org/data/2.5/weather?id="+config.openWeatherCityName+"&units=metric&appid="+config.openWeatherAPI)
    if( weather.status_code == requests.codes.ok ):
        print("Tout va bien, server accessible")
except:
    print("oups")
    exit()

forecast    = requests.get("http://api.openweathermap.org/data/2.5/forecast?id="+config.openWeatherCityName+"&units=metric&appid="+config.openWeatherAPI)
weatherActualCondition  = weather.json()
weatherForcast          = forecast.json()
weatherForcast          = weatherForcast['list']

def ConvertTimeStamp( timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d (%Hh)')
    #return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# icone du temps (see https://openweathermap.org/weather-conditions )
weatherIcoName  = weatherActualCondition['weather'][0]['icon']
#temperature     = str("%.1f" % weatherActualCondition['main']['temp'])
temperatureMin  = weatherActualCondition['main']['temp_min']
temperatureMax  = weatherActualCondition['main']['temp_max']
humidity        = weatherActualCondition['main']['humidity']


print(json.dumps(weatherForcast,indent=2))