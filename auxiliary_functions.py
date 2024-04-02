"""
File: auxiliary_functions.py
Description: home made libary with functions used in the main code.
"""

import pandas as pd 

'''This function gives back a dataframe of all the outgoing flows of a country.
    It works only with the cleaned dataframe, that has date as index.'''
def exit_flows(country, df):
    ex_flows = pd.DataFrame()
    for col in df.columns:
        parts = col.split("->")
        if country in parts[0]:
            ex_flows["to " + parts[1]] = df[col]
    return ex_flows

'''This function gives back a dataframe of all the incoming flows of a country.
    It works only with the cleaned dataframe, that has date as index.'''
def entry_flows(country, df):
    en_flows = pd.DataFrame()
    for col in df.columns:
        parts = col.split("->")
        if country in parts[1]:
            en_flows["from " + parts[0]] = df[col]
    return en_flows

'''This function just returns a list of all the countries involved in the study
    It works only with the cleaned dataframe, that has date as index.'''
def get_countries(df):
    countries = pd.Series()
    for col in df.columns:
        countries = pd.concat([countries, pd.Series(col.split("->"))], ignore_index=True)
    countries.drop_duplicates(inplace=True)
    return countries.tolist()
