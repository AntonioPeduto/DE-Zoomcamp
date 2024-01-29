# 1) Import libraries to be used
import os
import re
from time import time
import argparse
import pandas as pd 
from sqlalchemy import create_engine

# 2) Definition of function "main"
def main(args):
    """
    Function defined to do the following steps:
        - download file data source
        - extract data from file source
        - saving data into database
    """
    # 2.1) Definition/extraction of parameters 
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    dbname = args.dbname
    table = args.table
    url = args.url
    # 2.2) Download file data source
    os.system(f"wget {url}")
    match = re.search(r"(?<=/)[^/]+$",str(url))
    file_name = match.group()
    match = re.search(r".[a-zA-Z]+$",file_name)
    if match and match.group() == '.gz':
        os.system(f"gunzip -d {file_name}")
        file_name = re.sub(".[a-zA-Z]+$",'',file_name)
    # 2.3) Loading data (not all)
    df = pd.read_csv(file_name,nrows=1)
    # 2.4) modify type of a few columns in particulare for datetime
    # Initialize list of columns to convert to datetime
    columns_datetime = []
    for column in df.columns:
        # check if the current column is datetime
        match = re.search(r'.*date.*time.*',str.lower(column))
        # if curren column name include datetime
        if match :
            # convert current column to datetime
            df[column] = pd.to_datetime(df[column])
            # append current column in columns_datetime
            columns_datetime.append(column)
    # 2.5) Creation of engine connection with db
    engine = create_engine(f"postgresql://{user}:{password}@{host}/{dbname}")
    # 2.6) Creation of table
    df.head(0).to_sql(name=table, con=engine, if_exists='replace', index=False)
    # 2.7) Creation of iterator
    df_iter = pd.read_csv(file_name, iterator=True, chunksize=100000)
    # 2.8) Data ingestion
    # for each iter dataframe
    for df in df_iter:
        # Get current time
        time_start = time()
        # Convert a few columns to datetime
        for column in columns_datetime:
            # check if the current column is datetime
            match = re.search(r'.*date.*time.*',str.lower(column))
            # if curren column name include datetime
            if match :
                # convert current column to datetime
                df[column] = pd.to_datetime(df[column])
        # Inserting records into database
        df.to_sql(name=table, con=engine, if_exists='append', index=False)
        # Get current time
        time_end = time()
        # print message
        print(f"{len(df)} records have been inserted into the table {table} in {time_end - time_start}s.")

# 3) If this script is being run as the main program
if __name__=='__main__':
    # 3.1) Creation of a parser to set input parameters
    parser = argparse.ArgumentParser(description="Script defined for data ingestion.")
    # 3.2) Adding arguments
    # user
    parser.add_argument('--user', help='User name for postgres')
    # password
    parser.add_argument('--password', help='Password of user name for postgres')
    # host
    parser.add_argument('--host', help='Host for postgres')
    # port
    parser.add_argument('--port', help='Port for postgres')
    # database name
    parser.add_argument('--dbname', help='Database name for postgres')
    # table name
    parser.add_argument('--table', help='Table name for postgres')
    # URL
    parser.add_argument('--url', help='URL to download file data source')
    # 3.3) Parsing Arguments
    args = parser.parse_args()
    # 3.4) Execution of function main with input parameters
    main(args)
