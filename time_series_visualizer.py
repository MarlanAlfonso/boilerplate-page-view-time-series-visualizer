import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Load data and set index to date column
df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    index_col='date',
    parse_dates=True
)

# 2. Clean data — remove top 2.5% and bottom 2.5% of page views
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]


def draw_line_plot():
    # Use a copy of the data
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(32, 10))

    ax.plot(df_line.index, df_line['value'], color='red', linewidth=1)

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Use a copy of the data
    df_bar = df.copy()

    # Extract year and month from the datetime index
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Pivot: rows = years, columns = months, values = mean page views
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Rename columns from month numbers to month names
    month_names = [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    df_bar.columns = month_names

    fig, ax = plt.subplots(figsize=(15, 10))

    df_bar.plot(kind='bar', ax=ax)

    ax.set_title('')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Use a copy of the data
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    # Extract year and month information
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Define correct month order for x-axis
    month_order = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

    fig, axes = plt.subplots(1, 2, figsize=(28, 10))

    # Box plot 1: Year-wise (Trend)
    sns.boxplot(
        data=df_box,
        x='year',
        y='value',
        ax=axes[0]
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    # Box plot 2: Month-wise (Seasonality)
    sns.boxplot(
        data=df_box,
        x='month',
        y='value',
        order=month_order,
        ax=axes[1]
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig