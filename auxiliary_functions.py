"""
File: auxiliary_functions.py
Description: home made libary with functions used in the main code and in the dashboard.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import dash
from dash import html

country_mapping = {
    'AL': 'Albania',
    'AT': 'Austria',
    'BA': 'Bosnia and Herzegovina',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CH': 'Switzerland',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'EL': 'Greece',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IS': 'Iceland',
    'IT': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'ME': 'Montenegro',
    'MK': 'North Macedonia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RU': 'Russia',
    'RS': 'Serbia',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'UK': 'United Kingdom',
    'XK': 'Kosovo',
    'UA': 'Ukraine',
    'GE': 'Georgia',
    'MD': 'Moldova'
}

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
    The direction can be "outgoing"/"from" or "incoming"/"to" or "net".
    It uses exit_flows or entry_flows functions depending on the argument "direction".'''
def flows_from_direction(country, df, direction):
    flow_exits = exit_flows(country, df)
    flow_entries = entry_flows(country, df)
    if direction in ["from", "outgoing"]:
        return flow_exits # dataframe of the exit flows
    elif direction in ["to", "incoming"]:
        return flow_entries # dataframe of the entry flows
    elif direction == "net":
        flow_exits.columns = [col.split(' ', 1)[1] for col in flow_exits.columns]
        flow_entries.columns = [col.split(' ', 1)[1] for col in flow_entries.columns]
        flows = flow_entries.copy()
        for col in flow_exits.columns:
            if col in flows.columns: # If exit flow column exists in entry flows
                flows[col] = flows[col] - flow_exits[col] # Calculate net flow
            else:
                flows[col] = -flow_exits[col]
        return flows
    else:
        return pd.DataFrame()

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

'''This function takes a dataframe and returns a html Ul list of the names of the columns'''
def list_of_columnnames(df):
    names = df.columns.values
    list_items = [html.Li(name) for name in names]
    return html.Ul(list_items)
    
'''This function gives back the list of the name of the countries involved in the feature analysis'''
def get_country_feat_names():
    return list(country_mapping.values())
