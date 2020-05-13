#!/usr/bin/env python3


# ME499-S20 Python Lab 5
# Programmer: Jacob Gray
# Last Edit: 5/12/2020


import time
from datetime import datetime as dt
import requests
import json  # JSON module
import os.path
from matplotlib import pyplot as plt
import numpy as np


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

    if use_cache:
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


def plot_carbon(date=get_current_day()):
    """
    Outputs a plot of the predicted and realized carbon intensities for a given date.
    :param date: Date of interest for forecast data. ISO 8601 formatted 'YYYY-MM-DD'.
    :return: Plot.
    """

    data_dict = query_carbon(date)
    t = np.linspace(0, 24, num=len(data_dict['data']), endpoint=False)
    actual = []
    forecast = []

    for i in range(len(data_dict['data'])):
        actual.append(data_dict['data'][i]['intensity']['actual'])
        forecast.append(data_dict['data'][i]['intensity']['forecast'])

    actual_plt = plt.plot(t, actual, label="Actual Intensity")
    forecast_plt = plt.plot(t, forecast, label='Forecast Intensity')
    plt.legend(loc='upper left')
    plt.title('{} Carbon Intensity vs Time'.format(date))
    plt.xlabel('Time (hrs from midnight)')
    plt.ylabel('Carbon Intensity')

    return plt.savefig('plots/carbon_{}.png'.format(date))


if __name__ == '__main__':
    plot_carbon('2020-04-15')
