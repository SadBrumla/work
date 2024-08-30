import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib.figure import Figure


# ========================================================================================================================
# functions used to find sub dataframe with x values on column 0 and y values in the other columns

def find_sub_df(df,x_string,y_string):
    sub_df = get_column(df,x_string.upper())
    y_string_list = y_string.replace(" ",",").upper().split(",")
    for y in y_string_list:
        y_series = get_column(df,y)
        sub_df = pd.concat([sub_df,y_series],axis = 1)
    
    return sub_df

def column_index(name):
    """Excel-style column name to number, e.g., A = 1, Z = 26, AA = 27, AAA = 703."""
    n = 0
    for c in name:
        n = n * 26 + 1 + ord(c) - ord('A')
    return n - 1


def get_column(df, column_str):
    column = column_index(column_str)
    return df.iloc[:,[column]]

# ========================================================================================================================

def interpolate(X,Y,int_factor):      
        
    if int_factor == 0:
        return [None, None]
    
    elif len(X) > len(Y):
        X = X[:len(Y)]
    
    elif len(X) < len(Y):
        Y = Y[:len(X)]

    else:
        try:
            coeff = np.polyfit(X,Y,int_factor)
            f = np.poly1d(coeff)
            xx =   np.linspace(min(X),max(X),100)
            yy = f(xx)
        except:
            return[None,None]

        return [xx,yy]
    
# ========================================================================================================================

def auto_scale_axis():
    pass

