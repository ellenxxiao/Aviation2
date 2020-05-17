#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 16 17:21:03 2020

@author: ellenxiao
"""
import numpy as np

def cocktail(letter):
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?f="+letter
    resp = requests.request("GET",url)
    json_data = json.loads(resp.text)
    return json_data
cocktail_a = cocktail('c')

df = pd.DataFrame({'DrinkID':[],'DrinkName':[],'Category':[],'Ingredient1':[],'Ingredient2':[],'Ingredient3':[],
                  'Ingredient4':[],'Ingredient5':[],'Ingredient6':[],'Ingredient7':[],'Ingredient8':[],'Ingredient9':[],
                  'Ingredient10':[],'Ingredient11':[],'Ingredient12':[],
                  'Ingredient13':[],'Ingredient14':[],'Ingredient15':[],'Measure1':[],'Measure2':[],'Measure3':[],
                  'Measure4':[],'Measure5':[],'Measure6':[],'Measure7':[],'Measure8':[],'Measure9':[],
                  'Measure10':[],'Measure11':[],'Measure12':[],
                  'Measure13':[],'Measure14':[],'Measure15':[]})

for i in range(97,123):
    json_data = cocktail(chr(i))
    try:
        for drink in json_data['drinks']:
            DrinkID = drink['idDrink']
            DrinkName = drink['strDrink']
            Category = drink['strCategory']
            Ingredient1 = drink['strIngredient1']
            Ingredient2 = drink['strIngredient2']
            Ingredient3 = drink['strIngredient3']
            Ingredient4 = drink['strIngredient4']
            Ingredient5 = drink['strIngredient5']
            Ingredient6 = drink['strIngredient6']
            Ingredient7 = drink['strIngredient7']
            Ingredient8 = drink['strIngredient8']
            Ingredient9 = drink['strIngredient9']
            Ingredient10 = drink['strIngredient10']
            Ingredient11 = drink['strIngredient11']
            Ingredient12 = drink['strIngredient12']
            Ingredient13 = drink['strIngredient13']
            Ingredient14 = drink['strIngredient14']
            Ingredient15 = drink['strIngredient15']
            Measure1 = drink['strMeasure1']
            Measure2 = drink['strMeasure2']
            Measure3 = drink['strMeasure3']
            Measure4 = drink['strMeasure4']
            Measure5 = drink['strMeasure5']
            Measure6 = drink['strMeasure6']
            Measure7 = drink['strMeasure7']
            Measure8 = drink['strMeasure8']
            Measure9 = drink['strMeasure9']
            Measure10 = drink['strMeasure10']
            Measure11 = drink['strMeasure11']
            Measure12 = drink['strMeasure12']
            Measure13 = drink['strMeasure13']
            Measure14 = drink['strMeasure14']
            Measure15 = drink['strMeasure15']
            row_insert = [DrinkID,DrinkName,Category,Ingredient1,Ingredient2,Ingredient3,Ingredient4,Ingredient5,
                          Ingredient6,Ingredient7,Ingredient8,Ingredient9,Ingredient10,Ingredient11,Ingredient12,
                          Ingredient13,Ingredient14,Ingredient15,Measure1,Measure2,Measure3,Measure4,
                          Measure5,Measure6,Measure7,Measure8,Measure9,Measure10,Measure11,
                          Measure12,Measure13,Measure14,Measure15]
            df.loc[-1] = row_insert
            df.index = df.index + 1
    except:
        print('Error',chr(i))
df.set_index('DrinkID',inplace=True)

ingredient_list = []
for col in list(df.columns[2:17]):
    ingredient_list = ingredient_list + list(df[col].unique())
ingredient_no_null = list(filter(None,ingredient_list))
ingredient_arr = np.array(ingredient_no_null)
ingredient_unique = np.unique(ingredient_arr)

df1 = pd.DataFrame(columns=ingredient_unique, index=df.index)
df1['DrinkName'] = df['DrinkName']

for index in df.index:
    df1.loc[index][df.loc[index]['Ingredient1']] = df.loc[index]['Measure1'] 
    df1.loc[index][df.loc[index]['Ingredient2']] = df.loc[index]['Measure2']
    df1.loc[index][df.loc[index]['Ingredient3']] = df.loc[index]['Measure3']
    df1.loc[index][df.loc[index]['Ingredient4']] = df.loc[index]['Measure4']
    df1.loc[index][df.loc[index]['Ingredient5']] = df.loc[index]['Measure5']
    df1.loc[index][df.loc[index]['Ingredient6']] = df.loc[index]['Measure6']
    df1.loc[index][df.loc[index]['Ingredient7']] = df.loc[index]['Measure7']
    df1.loc[index][df.loc[index]['Ingredient8']] = df.loc[index]['Measure8']
    df1.loc[index][df.loc[index]['Ingredient9']] = df.loc[index]['Measure9']
    df1.loc[index][df.loc[index]['Ingredient10']] = df.loc[index]['Measure10']
    df1.loc[index][df.loc[index]['Ingredient11']] = df.loc[index]['Measure11']
    df1.loc[index][df.loc[index]['Ingredient12']] = df.loc[index]['Measure12']
    df1.loc[index][df.loc[index]['Ingredient13']] = df.loc[index]['Measure13']
    df1.loc[index][df.loc[index]['Ingredient14']] = df.loc[index]['Measure14']
    df1.loc[index][df.loc[index]['Ingredient15']] = df.loc[index]['Measure15']

df1.set_index('DrinkName',inplace=True)
df1.to_csv('/Users/ellenxiao/Documents/Udemy/cocktail/cocktail.csv')

