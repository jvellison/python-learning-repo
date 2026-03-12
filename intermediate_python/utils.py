import pandas as pd
from config_903 import DateCols, EthnicSubcategories
from dateutil.relativedelta import relativedelta

import numpy as np

def format_dates(column): 
    column.replace(r"^\s*$",pd.NaT, regex=True)
    column = column.fillna(pd.NaT) # fill empty spaces
    try:
        column = pd.to_datetime(column, format="%d/%m/%Y")
        return column
    except:
        raise ValueError(f"Unknown date format in {column.name}, expected dd/mm/YYYY")
    
def calculate_age_buckets(age):
    # Used to make age buckets matching published data
    if age < 1:
        return "a) Under 1 year"
    elif age < 5:
        return "b) 1 to 4 years"
    elif age < 10:
        return "c) 5 to 9 years"
    elif age < 16:
        return "d) 10 to 16 years"
    elif age >= 16:
        return "e) 16 years and over"
    else:
        return "f) Age error"
    

def clean_903_table(df: pd.DataFrame, collection_end: pd.Timestamp) -> pd.DataFrame:
    '''
    Takes tables from the 903 as dataframes and outputs cleaned tables. Later include what cleaning it actually does.
    '''
    #print('Function works')

    clean_df = df.copy()

    # TODO remove index column # easy to see what you need to do later

    if "index" in df.columns:
        clean_df.drop("index",axis=1, inplace=True)

    # TODO convert date columns

    for column in clean_df.columns:
        if column in DateCols.cols.value:
            # TODO make datetime
            #clean_df[column] = pd.to_datetime(column, dayfirst=True)
            #clean_df[column] = format_dates(clean_df[column])
            clean_df[f"{column}_dt"] = format_dates(clean_df[column])

    # TODO make ethnic main group column
    # clean_df['ethnic main group'] = clean_df['ETHNIC'].map('WROM':'WHITE') #messy, slower
    if "ETHNIC" in clean_df.columns:
        clean_df['ETHNICITY'] = clean_df['ETHNIC'].apply(
            lambda ethnicity: EthnicSubcategories[ethnicity].value
        )

    # TODO make age column
    if "DOB_dt" in clean_df.columns:
        clean_df['AGE'] = clean_df['DOB_dt'].apply(
            lambda dob: relativedelta(dt1 = collection_end, dt2 = dob).normalized().years
        )
        # TODO add age buckets column
        clean_df["AGE_BUCKETS"] = clean_df['AGE'].apply(calculate_age_buckets)

    
    return clean_df

def group_calculation(df, column, measure_name):
    '''
    A function to group a df by input column, outputs with count and
    percentage to a datafrane with renamed columns.
    '''
    grouped = df.groupby(column).size()
    grouped = grouped.to_frame(f'{measure_name} - Count').reset_index()
    grouped = grouped.rename(columns={column:'Value'})

    grouped[f'{measure_name} - Percentage'] = (grouped[f'{measure_name} - Count'] / 
                                                    grouped[f'{measure_name} - Count'].sum()) * 100
    return grouped

def time_difference(start_col, end_col, business_days=False):
    if business_days:
        # np.busday_count can only use datetime64[D] type data, so we need to
        # convert the objects
        time_diff = np.busday_count(
            start_col.values.astype("datetime64[D]"),
            end_col.values.astype("datetime64[D]")
        )
    else:
        time_diff = end_col - start_col
        time_diff = time_diff / pd.Timedelta(days=1) # divide by 1 day to just give number
    
    return time_diff.astype("int") # so full days, not a decimal - always rounds down