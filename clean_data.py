# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import re

data=pd.read_csv(r'C:\Users\Brand\Desktop\Aviation2-master\Aviation2-master\cocktail.csv')

col_list=[]
clean_data=pd.DataFrame()
for col in data.columns:
    col_clean=col.lower().strip()
    if col_clean not in col_list:
        clean_data[col_clean]=data[col]
        col_list.append(col_clean)
    else:
        clean_data[col_clean]=data[col].fillna('').astype(str)+clean_data[col_clean].fillna('').astype(str)
  
text='1-1/2 oz'

re.search('^[\.|0-9]*[\.|\s|\-|\/|0-9]*[0-9]',text)

      
unit_dict={}
value_dict={}      
exception_list=[]
for col in clean_data:
    unit_dict[col]=[]
    for value in clean_data[col]:
        try:
            num=re.search('^[\.|0-9]*[\.|\s|\-|\/|0-9]*[0-9]',value)
            if num[0] not in value_dict:
                value_dict[num[0]]=value
            if value[num.span()[1]:] not in unit_dict[col]:
                unit_dict[col].append(value[num.span()[1]:])
        except:
            exception_list.append(value)


    
def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

def convert(value):
    if '-' in str(value):
        try:
            left,right=value.split('-')
            left=convert_to_float(left.strip())
            right=convert_to_float(right.strip())
            return (left+right)/2
        except:
            return left[0]
    else:
        try:
            return convert_to_float(value)
        except:
            if value =='' or pd.isna(value)==True:
                return 0
            else:
                return 1
        

        
for key in value_dict.keys():
    value_dict[key]=convert(key)
    
    
unit_dict_clean={
    "oz":1,
    "tsp":0.167,
    "tblsp":0.167,
    "spoon":0.167,
    "jigger":1.5,
    "bottle":25,
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

def get_clean_value(x):
    try:
        num=re.search('^[\.|0-9]*[\.|\s|\-|\/|0-9]*[0-9]',x)
        return num[0]
    except:
        return x

def get_unit(x):
    try:
        num=re.search('^[\.|0-9]*[\.|\s|\-|\/|0-9]*[0-9]',x)
        unit=x[num.span()[1]:]
        for key in unit_dict_clean.keys():
            if key in unit:
                return key
        return ''
    except:
        return ''
    
def convert_unit(x,original_unit,new_unit):
    try:
        return x*unit_dict[original_unit]/unit_dict[new_unit]
    except:
        return x
    
    

clean_data_step2=pd.DataFrame(index=clean_data.index)
col_unit_dict={}
for col in clean_data.columns:
    try:
        col_unit=clean_data[col].where(lambda x:x !='').dropna().apply(lambda x:get_unit(str(x))).value_counts().idxmax()
        if col_unit=='part':
            col_unit='oz'
    except:
        col_unit='part or not unit'
    col_unit_dict[col]=col_unit
    clean_data_step2[col+' ('+col_unit+')']=clean_data[col].apply(lambda x:convert_unit(convert(get_clean_value(x)),get_unit(x),col_unit))
    
clean_data_step2.fillna(0,inplace=True)
clean_data_step2.to_csv(r'C:\Users\Brand\Desktop\Aviation2-master\Aviation2-master\cocktail_clean.csv')
