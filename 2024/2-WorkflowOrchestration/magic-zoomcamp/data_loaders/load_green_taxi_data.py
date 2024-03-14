import pandas as pd
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Block created for loading data from specific urls.

    Returns:
        df -> dataframe containing data extracted from urls.
    """
    # Specify the urls from which extracting data
    urls = ['https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz', \
            'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz', \
            'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz']

    # Specification of type of columns
    dtypes = {
                'VendorID':pd.Int64Dtype(), \
                'store_and_fwd_flag':str, \
                'RatecodeID':pd.Int64Dtype(), \
                'PULocationID':pd.Int64Dtype(), \
                'DOLocationID':pd.Int64Dtype(), \
                'passenger_count':pd.Int64Dtype(), \
                'trip_distance':float, \
                'fare_amount':float, \
                'extra':float,
                'mta_tax':float, \
                'tip_amount':float, \
                'tolls_amount':float, \
                'ehail_fee':float, \
                'improvement_surcharge':float, \
                'total_amount':float, \
                'payment_type':pd.Int64Dtype(), \
                'trip_type':pd.Int64Dtype(), \
                'congestion_surcharge':float
            }
    # Specification of columns dates
    dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    # Initialization of the list of dataframes
    list_df = []
    # For each url
    for url in urls:
        # Getting data
        df_current = pd.read_csv(url, dtype=dtypes, compression='gzip', parse_dates=dates)
        # Appending current dataframe in list_df
        list_df.append(df_current)
    # Union of dataframes extracted
    df = pd.concat(list_df, ignore_index=True)
    # return dataframe
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
