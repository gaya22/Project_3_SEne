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

'''This function gives back a tuple that has the only purpose to fill the table
    with the pick of fraction of electricity generated by gas'''
def get_pick_gas(df):
    df_pick=pd.DataFrame(columns=["Country", "Date", "Fraction of electricity generated by gas", "Electricity generated from natural gas GWh"])
    pick_countries = ['MD', 'MT', 'NL', 'LV', 'IE', 'LT', 'IT']
    df = df[["Fraction of electricity generated by gas", "Electricity generated from natural gas GWh"]]
    for country in pick_countries:
        country_data = df.loc[(country, slice(None)), :]
        max_row_index = country_data['Fraction of electricity generated by gas'].idxmax()
        max_row = country_data.loc[max_row_index]
        country_name = max_row_index[0]  # Extract country from the index
        date = max_row_index[1].strftime("%B %Y")  # Extract date from the index
        df_pick = pd.concat([df_pick, pd.DataFrame({"Country": country_mapping[country_name],
                                                     "Date": [date],
                                                     "Fraction of electricity generated by gas": [max_row["Fraction of electricity generated by gas"]],
                                                     "Electricity generated from natural gas GWh": [max_row["Electricity generated from natural gas GWh"]]})], ignore_index=True)
    return df_pick

'''This function is created just to remove some code from the dashboard.
    It contains a portion of text that will be shown in the webpage (Italy data exploration)'''
def considerations():
    mystr = "The amount of electricity generated by gas is not a good indicator of how much gas Italy imports, while the gas comsumed is. "
    mystr += "The electricity import goes similarly with gas imports. "
    mystr += "Electricity exports and electricity available to market (that is to say: electricity surplus) are not that well correlated to the metric of our interest. "
    mystr += "The electricity generated shows some peaks in correspondance to the gas imports, but most of it looks delayed of some months. "
    mystr += "The comparison between gas imports and gas consumption shows that when Italy consumes lots of gas, it also imports a lot of gas (picks) if it is winter, as it can also be noted with a relevant negative correlation value between the average temperature in the country and and the gas conumned. "
    mystr += "If it's summer, Italy still relies on gas for electricity generation but it doesn't import as much gas. "
    mystr += "Data also shows that Italy relies on stocking gas in the winter to use it later in the summer. "
    mystr += "On the other hand, the amount of gas produced and the amount of gas exported are so little to not have any impact on the rest of the metrics. "
    mystr += "The data about population does not seem to look well correlated to anything else. "
    mystr += "It is very interesting to see that gas/electricity prices for industries/households are highly correlated with the complete data, this goes to confirm the fact that gas is an important factor in electricity generation for Italy. "
    mystr += "The former is not the case before 2020: only the electricty and gas prices for industries seem to be higly correlated, while the others exhibit positive, but not strong, correlation. "
    mystr += "\nOther correlations regarding the import/export values to certain neighbour countries are being noticed, as a higher gas export to Switzerland when the temperature gets colder, probably due to the high demand in cold winters."
    mystr += "The correlation that relates the most with the goal of our project is about gas prices, that are clearly tied with the imports from certain countries, mainly due to some historical events happened through the last years. "
    mystr += "Our data suggests that principally when gas prices get higher, both for households and industrial uses, imports from Austria tend to decrease as imports from other countries as Albania increase. "
    mystr += "This trend can be justified clearly with the conflict happening between Russia and Ukraine that led to a strong increase in gas prices in all Europe, we can suppose that most of the russian gas was arriving from Austria and so imports were decreased as prices and availability has changed. "
    mystr += "In 2022 Austria fastly stopped being the main gas exporter to Italy, and other markets increased to satisfy the demand, as Tunisia and Albania. "
    mystr += "Another observation migth come out from liquified natural gas import, as it seems to be imported principally when the gas production is low and viceversa, we can so underline how the use of regasification plants present in the territory are fundamental to balance gas price and import mix. "
    mystr += "However, the prices at which Italy imports electricity and gas are not available. "
    return mystr

'''This function is created just to remove some code from the dashboard.
    It contains a portion of text that will be shown in the webpage (Russo-Ukrainian war impact)'''
def forecast_introduction():
    mystr = 'This comparison will be done through a forecast of data from 2022 on. To address that, the most important features were selected, and some others were created. '
    mystr += 'The data used for the forecast has to be necessarily without the war influence, so just'
    mystr+= 'From the previous analysis, we know that gas consumption and gas stocks are periodic and well autocorrelated, and as such we can employ an autoregression model to forecast their values from 2022 to today. '
    return mystr