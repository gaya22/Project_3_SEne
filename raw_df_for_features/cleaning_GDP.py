"""
File: cleaning_GDP.py
Description: This code has the aim to clean a bit the row files of GDP, to have them more readable in the next steps.
             The data are downloaded from https://data-explorer.oecd.org/
"""

import pandas as pd

df_GR = pd.read_csv('raw_df_for_features/GDP_GrowRate_OECD.csv')
df_I = pd.read_csv('raw_df_for_features/GDP_Index_OECD.csv')

columns_to_drop = ["STRUCTURE", "STRUCTURE_ID", "STRUCTURE_NAME", "ACTION", "FREQ", "Frequency of observation", "MEASURE", 
                   "UNIT_MEASURE", "ACTIVITY", "ADJUSTMENT", "TRANSFORMATION", "Time period", "Observation value", 
                   "OBS_STATUS", "Unit multiplier", "Decimals", "BASE_PER", "Base period"]

cleaned_GR = df_GR.drop(columns=columns_to_drop)
cleaned_I = df_I.drop(columns=columns_to_drop)

cleaned_GR.to_csv('GDP_GrowRate.csv', encoding='utf-8', index=True)
cleaned_I.to_csv('GDP_Index.csv', encoding='utf-8', index=True)
