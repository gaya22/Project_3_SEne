"""
File: auxiliary_functions.py
Description: home made libary with functions used in the main code and in the dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime

'''This function gives back a dataframe of all the outgoing flows of a country.
    It works only with the cleaned dataframe, that has date as index.'''
def exit_flows(country, df):
    ex_flows = pd.DataFrame() # Create a dataframe to host the values
    for col in df.columns: # I verify if inside my origin dataframe there is the country that I want
        if "->" in col:
            parts = col.split("->")
            if country in parts[0]: # I verify that is the country from where flow exits
                ex_flows["to " + parts[1]] = df[col]
    return ex_flows

'''This function gives back a dataframe of all the incoming flows of a country.
    It works only with the cleaned dataframe, that has date as index.'''
def entry_flows(country, df):
    en_flows = pd.DataFrame()
    for col in df.columns:
        if "->" in col:
            parts = col.split("->")
            if country in parts[1]:
                en_flows["from " + parts[0]] = df[col]
    return en_flows

'''This function takes the cleaned dataframe, a specific country and the direction.
    The direction can be "outgoing"/"from" or "incoming"/"to".
    It uses exit_flows or entry_flows functions depending on the argument "direction".'''
def flows_from_direction(country, df, direction):
    if direction == "from" or "outgoing":
        flow_df = exit_flows(country, df) # dataframe of the exit flows
    elif direction == "to" or "incoming":
        flow_df = entry_flows(country, df) # dataframe of the entry flows
    else:
        flow_df = pd.DataFrame()
    return flow_df

'''This function just returns a list of all the countries involved in the study that have extit flows
    It works only with the cleaned dataframe, that has date as index.'''
def get_exit_countries(df):
    excountries = pd.Series()
    for col in df.columns:
        parts = col.split("->")
        excountries = pd.concat([excountries, pd.Series(parts[0])], ignore_index=True)
    excountries.drop_duplicates(inplace=True)
    return excountries.tolist()

'''This function just returns a list of all the countries involved in the study that have enter flows
    It works only with the cleaned dataframe, that has date as index.'''
def get_enter_countries(df):
    encountries = pd.Series()
    for col in df.columns:
        parts = col.split("->")
        encountries = pd.concat([encountries, pd.Series(parts[0])], ignore_index=True)
    encountries.drop_duplicates(inplace=True)
    return encountries.tolist()

'''This function just returns a list of all the countries involved in the study
    It works only with the cleaned dataframe, that has date as index.'''
def get_countries(df):
    countries = pd.Series()
    for col in df.columns:
        countries = pd.concat([countries, pd.Series(col.split("->"))], ignore_index=True)
    countries.drop_duplicates(inplace=True)
    return countries.tolist()

'''This function returns a dataframe with the countries as index and the total exit and enter flows of the whole period
    It works only with the cleaned dataframe, that has date as index.'''
def countries_tot_flows(df):
    countries = get_countries(df) # Firstly it creates a list with the countries we have
    tot_df = pd.DataFrame(index=countries) # Create a dataframe with countries as index
    mylist_exit = [] # Intialize a list to host the values of exit flows
    mylist_enter = [] # Intialize a list to host the values of enter flows
    for ind in tot_df.index: # Iterate on countries
        mylist_exit.append(exit_flows(ind, df).values.sum()) # Calculate the exit flows and sum all
        mylist_enter.append(entry_flows(ind, df).values.sum()) # Calculate the enter flows and sum all
    tot_df["tot_exit_flows"] = mylist_exit # Assign thevalues of the exit list to the dataframe
    tot_df["tot_enter_flows"] = mylist_enter # Assign the values of the enter list to the dataframe
    return tot_df

'''This function takes a numpy.datetime64 date object
    It returns a string with the month and the year'''
def get_month(date64):
    datetime_object = np.datetime_as_string(date64, unit='D')
    date_as_datetime = datetime.strptime(datetime_object, '%Y-%m-%d')
    return date_as_datetime.strftime("%B %Y")
 
 # ciao