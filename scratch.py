#!/usr/bin/env python3


# ME499-S20 Python Lab 5
# Programmer: Jacob Gray
# Last Edit: 5/12/2020

from pathlib import Path
import os.path
import requests
import json
from carbon import get_current_day

date = get_current_day()


print(os.path.exists('data/carbon_2019-10-31.json'))
