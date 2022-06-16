import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import datetime
import calendar
# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
df['date'] = pd.to_datetime(df['date'])  #Get Date value is correct format so python understands
df = df.set_index('date')  # Change index to date

# Clean data
# Removes when the page views were in the top 2.5% or bottom 2.5% of dataset
df = df.loc[(df["value"] >= df["value"].quantile(0.025))
            & (df["value"] <= df["value"].quantile(0.975))]
#df = df.value[(df.value > df.value.quantile(0.025)) & (df.value < df.value.quantile(0.975))]  # Transform df to series

def draw_line_plot():
    # Draw line plot
    fig = df.plot.line()
    fig = fig.get_figure()
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_copy = df.value
    fig , ax = plt.subplots(figsize=(10 , 10)) # Initalize figure
    bar_plot = df_copy.groupby([df.index.year , df.index.month]).mean().unstack()  # Cleaning data to seperate year and month
    bar_plot.plot(ax=ax , kind='bar')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')

    handles , labels = ax.get_legend_handles_labels()  # Handles = year
    new_labels = [datetime.date(1900 , int(monthinteger), 1).strftime('%B') for monthinteger in labels]  # Get month labels
    ax.legend(handles=handles , labels=new_labels , loc='upper left' , bbox_to_anchor=(1.02 , 1))

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # for month_name in calendar.month_name:
    #   df_box = df_box.value[df_box.month == month_name]

    month_avg = df_box.groupby(['month']).mean()['value']  # Get a series of average values for each month
    new_order = ['Jan' , 'Feb' , 'Mar' , 'Apr' , 'May' , 'Jun' , 'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov' ,
                 'Dec']  # Give order by hand
    month_avg = month_avg.reindex(new_order , axis=0).to_frame()  # Reindexs according to above order

    year_avg = df_box.groupby(['year']).mean()['value']

    df_box['month'] = pd.Categorical(df_box['month'] , categories=new_order , ordered=True)
    df_box.sort_values(by='date' , inplace=True)  # at this part it is sorted according to date, great

    # Draw box plots (using Seaborn)
    fig , axs = plt.subplots(ncols=2)  # Initalize figure
    plot1 = sns.boxplot(data=df_box , y="value" , x='month' , ax=axs[1])  # ax= axs[0] to allow where are each plot
    plot1.set(ylabel="Page Views" , xlabel='Month', title='Month-wise Box Plot (Seasonality)')
    plot2 = sns.boxplot(data=df_box , y="value" , x='year' , ax=axs[0])
    plot2.set(ylabel="Page Views" , xlabel='Year',title="Year-wise Box Plot (Trend)")
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig