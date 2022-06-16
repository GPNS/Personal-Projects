"""
Code for Sea Level Predictor of FCC

"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')
    # Create scatter plot
    x = df['Year']
    extra_years = pd.Series(list(range(df['Year'].iloc[-1] + 1 , 2051)))  # Create extra series with the missing years
    y = df['CSIRO Adjusted Sea Level']
    fig , ax = plt.subplots(figsize=(12 , 8))
    plt.scatter(x , y , c="blue" , label='Originial Data')  # Create Scatter plot

    # Create first line of best fit
    res = linregress(x=x , y=y)  # Create regression based on all of the data
    x_fitted_line = pd.concat([x , extra_years])  # Add missing year to the end of the year series
    plt.plot(x_fitted_line , res.intercept + res.slope * x_fitted_line , 'black' , label='fitted line')
    # Create second line of best fit
    df_modern = df.loc[(df["Year"] >= 2000)]  # Isolate the data that comes after 2000
    x_recent = df_modern["Year"]
    y_recent = df_modern['CSIRO Adjusted Sea Level']

    res_recent = linregress(x=x_recent , y=y_recent)  # Create new regression based on recent data

    x_modern = pd.concat([x_recent , extra_years])  # Concate to have plot till 2050
    plt.plot(x_modern , res_recent.intercept + res_recent.slope * x_modern , 'r' , label='fitted line recent')
    plt.legend()
    # Add labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Sea Level (inches)')
    ax.set_title('Rise in Sea Level')
    #fig.suptitle('Rise in Sea Level')  # Adds a sub title

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()