from config import *
import pandas as pd

def filter_profit_movies(df,budget_limit_above=None):
    """
    this function will return pandas dataframe after filtering input dataframe
    revenue greater than budget and adding filter to avoid below 0 budget movies
    :param DataFrame
    :return: DataFrame
    """
    if not budget_limit_above:
        budget_limit_above = min_budget_limit
    df['budget'] = df['budget'].apply(pd.to_numeric)
    df =  df[(df['budget'] > budget_limit_above) & (df['revenue'] > df['budget'])]
    return df

def extract_year_from_release_date(df):
    """
    this function will return pandas dataframe
    :param DataFrame
    :return: DataFrame
    """
    df['year'] = pd.DatetimeIndex(df['release_date']).year
    return df

def calc_ratio_from_budget_and_revenue_filter_top_once(df,num=None):
    """
    this function will return pandas dataframe by taking dataframe as input and calculating ration
    budget/revenue on those columns and adding ratio column to df
    :param DataFrame : dataframe with movies data in it
    :return: DataFrame : dataframe with ratio
    """
    if not num:
        num = top
    df = df.fillna(0)
    df['ratio'] = df['budget'] / df['revenue']
    df.sort_values(by=['ratio'], inplace=True, ascending=False)
    df = df.head(num).reset_index(drop=True)
    return df