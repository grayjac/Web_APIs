#!/usr/bin/env python3


# ME499-S20 Python Lab 5
# Programmer: Jacob Gray
# Last Edit: 5/12/2020


import time
from datetime import datetime as dt
import requests
import urllib.request as req  # Request library that lets you get data from web
import json  # JSON module
import os.path


def get_current_day(unix=time.time()):
    """
    :param unix: Unix timestamp
    :return: Returns the current day in UTC from a timestamp.
    """
    return dt.utcfromtimestamp(int(unix)).strftime("%Y-%m-%d")


def query_carbon(date=get_current_day(), use_cache=True):
    """
    Retrieves carbon forecast data from https://carbon-intensity.github.io/api-definitions/#intensity.
    :param date: Date of interest for forecast data. ISO 8601 formatted "YYYY-MM-DD"
    :param use_cache: Boolean.
    :return: Forecast data?
    """

    if use_cache == True:
        if os.path.exists('data/carbon_{}.json'.format(date)):
            with open('data/carbon_{}.json'.format(date), 'r') as readfile:
                return json.load(readfile)
        else:
            print('No file here!')

    headers = {'Accept': 'application/json'}
    r = requests.get('https://api.carbonintensity.org.uk/intensity/date/{}'.format(date), params={},
                     headers=headers)
    if r.ok:
        print('Request successful')
    else:
        raise Exception

    data_dict = r.json()

    js = json.dumps(data_dict, sort_keys=True, indent=4)
    with open('data/carbon_{}.json'.format(date), 'w+') as writefile:
        writefile.write(js)

    return data_dict


if __name__ == '__main__':
    print(type(query_carbon('2020-05-12')))


