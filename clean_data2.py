#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 24 22:28:32 2020

@author: ellenxiao
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_csv('/Users/ellenxiao/Documents/Udemy/cocktail/cocktail_clean.csv')
df = df.set_index('drinkname')

unit_dict_clean={
    "oz":1,
    "tsp":0.167,
    "tblsp":0.5,
    "spoon":0.167,
    "jigger":1.5,
    "bottle":12,
    "L":33.814,
    "shot":1.5,
    "cl": 0.33814,
    "dash":0.33,
    "ml":0.034,
    "drop": 0.0017,
    "cup": 8,
    "can":12,
    "pinch":0.01,
    "gallon":128,
    "pint": 16,
    "part":1,
    }

for col in df.columns:
    if '(bottle)' in col:
        df[col] = df[col] * 12
    elif '(tsp)' in col:
        df[col] = df[col] * 0.167
    elif '(shot)' in col:
        df[col] = df[col] * 1.5
    elif '(ml)' in col:
        df[col] = df[col] * 0.034
    elif '(cup)' in col:
        df[col] = df[col] * 8
    elif '(can)' in col:
        df[col] = df[col] * 12
    elif '(pinch)' in col:
        df[col] = df[col] * 0.01
    elif '(pint)' in col:
        df[col] = df[col] * 16
    elif '(spoon)' in col:
        df[col] = df[col] * 0.167
    elif '(tblsp)' in col:
        df[col] = df[col] * 0.5
    elif '(dash)' in col:
        df[col] = df[col] * 0.33
    elif '(cl)' in col:
        df[col] = df[col] * 0.33814

# delete ()
df_col = []

for col in list(df.columns):
    if col.find('()') != -1:
        df_col.append(col.replace(' ()',''))
    else:
        df_col.append(col)

df.columns = df_col

ingredient = pd.read_csv('/Users/ellenxiao/Documents/Udemy/cocktail/drink_ingredient.csv')
ingredient = ingredient.set_index('Name')



for index in ingredient.index:
    for col in ingredient.columns:
        if pd.isna(ingredient.loc[index,col]) == False:
            if ingredient.loc[index,col] not in df.columns:
                df[ingredient.loc[index,col]] = df[index]
            else:
                df[ingredient.loc[index,col]] = df[ingredient.loc[index,col]] + df[index]
                

measurable_list = ['rum', 'grain alcohol', 'vodka', 'brandy', 'bitters',
       'campari', 'whiskey', 'beer', 'soda', 'syrup', 'champagne', 'coke', 'milk', 'coffee',
       'wine', 'gin', 'tequila', 'yoghurt']

for col in list(df.columns):
    if col not in measurable_list:
        df[col] = df[col].apply(lambda x: 1 if x > 0 else 0 )
        

df.to_csv('/Users/ellenxiao/Documents/Udemy/cocktail/cocktail_clean2.csv')

