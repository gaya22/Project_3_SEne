"""
File: cleaning_electricity.py
Description: This code has the aim to clean a bit the row file of electricity data, to have them more readable in the next steps.
             The data are downloaded from https://ember-climate.org/data-catalogue/monthly-electricity-data/
"""

import pandas as pd

df = pd.read_csv('monthly_full_release_long_format-4.csv')

# This dataframe contains a lot of interesting data but it has informations just from 2018.
# We have to figure out wether to use it anyways or not.
# Here is the info of the dataframe:
"""
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 392112 entries, 0 to 392111
    Data columns (total 18 columns):
    #   Column               Non-Null Count   Dtype  
    ---  ------               --------------   -----  
    0   Area                 392112 non-null  object 
    1   Country code         348792 non-null  object 
    2   Date                 392112 non-null  object 
    3   Area type            392112 non-null  object 
    4   Continent            348792 non-null  object 
    5   Ember region         348792 non-null  object 
    6   EU                   348792 non-null  float64
    7   OECD                 348792 non-null  float64
    8   G20                  348792 non-null  float64
    9   G7                   348792 non-null  float64
    10  ASEAN                348792 non-null  float64
    11  Category             392112 non-null  object 
    12  Subcategory          392112 non-null  object 
    13  Variable             392112 non-null  object 
    14  Unit                 392112 non-null  object 
    15  Value                391352 non-null  float64
    16  YoY absolute change  243380 non-null  float64
    17  YoY % change         208295 non-null  float64
    dtypes: float64(8), object(10)
    memory usage: 53.8+ MB
"""

# And the categories that it has:
"""
    Category
    Electricity generation    238014
    Power sector emissions    132762
    Electricity demand          9170
    Electricity imports         9170
    Electricity prices          2996
    Name: count, dtype: int64
"""