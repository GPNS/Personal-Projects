"""
Code for Medical Data Visualizer of FCC
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
height = df['height']/100  # Get height in m
BMI = df['weight']/height**2  # Calculate BMI
df.loc[BMI < 25, 'overweight'] = 0  # If value of BMI less than 25 at same index of df in column (creates it) 'overweight' the value is 0
df.loc[BMI >= 25, 'overweight'] = 1
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0  # If value in cholesterol is 1 then the new value in cholesterol is now 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1
df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    names = sorted(['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    # Test doesn't work if not alphabetical
    df_cat = pd.melt(df, id_vars='cardio', value_vars=names)

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.

    # Draw the catplot with 'sns.catplot()'
    temp = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio')
    temp.set_axis_labels("variable", "total")  # Sets axis labels
    fig = temp.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

#Clean the data. Filter out the following patient segments that represent incorrect data:
#diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
#height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
#height is more than the 97.5th percentile
#weight is less than the 2.5th percentile
#weight is more than the 97.5th percentile



# Draw Heat Map
def draw_heat_map():
    # Clean the data
    #Each condition needs to be true for row to be conserved need to be done at once not subsequently or df 'resets'
    df_heat = df.loc[
        (df["ap_lo"] <= df["ap_hi"])
        & (df["height"] >= df["height"].quantile(0.025))
        & (df["height"] <= df["height"].quantile(0.975))
        & (df["weight"] >= df["weight"].quantile(0.025))
        & (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    #mask = np.zeros_like(corr)
    #mask[np.triu_indices_from(mask)] = True
    mask = np.triu(np.ones_like(corr))
    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, mask=mask, annot=True, linewidths=.5, vmin = 0, vmax = .3, fmt=".1f")

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
