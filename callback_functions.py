"""
File: callback_functions.py
Description: home made libary with functions especially used for the dashboard.
"""

import numpy as np
from datetime import datetime

'''This function takes a numpy.datetime64 date object
It returns a string with the month and the year'''
def get_month(date64):
    datetime_object = np.datetime_as_string(date64, unit='D')
    date_as_datetime = datetime.strptime(datetime_object, '%Y-%m-%d')
    return date_as_datetime.strftime("%B %Y")