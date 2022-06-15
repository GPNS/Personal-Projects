"""
Code for Medical Data Visualizer of FCC (not done as there is an error in the heatmap values. Wasn't able to find it
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
#df['overweight'] = df["weight"]/((df["height"]/100)**2)
#df['overweight'] = df['overweight'].apply(lambda x: 1 if x > 25 else 0)
df["overweight"] = np.where(
    df["weight"] / (df["height"]/100)**2 > 25,
    1,
    0,
)
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
#df["cholesterol"] = df["cholesterol"].apply(lambda x: 1 if x > 1 else 0)
df["cholesterol"] = np.where(df["cholesterol"] == 1, 0, 1)
df["gluc"] = np.where(df["gluc"] == 1, 0, 1)

#df["gluc"] = pd.cut(df['gluc'], bins=[0,1,np.inf], labels=[0, 1])
#df["gluc"] = df["gluc"].apply(lambda x: 1 if x > 1 else 0)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    names = sorted(['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    # Test doesn't work if not alphabetical
    df_cat = pd.melt(df, id_vars='cardio', value_vars=names)


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.

    # Draw the catplot with 'sns.catplot()'
    temp = sns.catplot(data=df_cat, kind='count', x='variable', hue='value', col='cardio')
    temp.set_axis_labels("variable", "total")  # Need to change label required by tests and return only figure
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
    #Each condition needs to be true for row to be conserved
    #df_heat = df[(df['ap_lo'] <= df['ap_hi']) &
    #   (df['height'] >= (df['height'].quantile(0.025))) & #Removes lowest values of height
    #   (df['height'] <= (df['height'].quantile(0.975))) & #Removes highest values of height
    #   (df['weight'] >= (df['weight'].quantile(0.025))) &
    #   (df['weight'] <= (df['weight'].quantile(0.975)))]
    df_heat = df.loc[
        (df["ap_lo"] <= df["ap_hi"])
        & (df["height"] >= df["height"].quantile(0.025))
        & (df["height"] <= df["height"].quantile(0.975))
        & (df["weight"] >= df["weight"].quantile(0.025))
        & (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    #mask = np.triu(np.ones_like(corr , dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 8))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr,
                mask = mask,
                vmax=0.4 ,
                square = True,
                annot=True,
                fmt='.1f')

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
A=draw_heat_map()