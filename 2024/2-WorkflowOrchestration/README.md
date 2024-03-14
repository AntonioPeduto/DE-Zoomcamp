# Workflow Orchestration

## Description

In this project, we'll be working with the green taxi dataset located here:

https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download


The goal will be to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a database and Google Cloud.

To achieve this goal, we'll use the open-source data pipeline tool: [__Mage__](https://www.mage.ai/). 

The files inside of the current folder that are essentials to achieve the goal of this project are the following:

- [Dockerfile](./Dockerfile) -> file used to define docker image for Mage.
- [requirements.txt](./requirements.txt) -> file that specifies the list of packages to be installed inside of a container from the image for Mage.
- [docker-compose.yaml](./docker-compose.yaml) -> file defined to create a two docker-containers inside of the same network:
    - magic -> container from the image for Mage in Dockerfile
    - postgres -> container from the image for postgres
- [env](./.env) -> file for the definition of environment variables used in this project.
- [my-key.json](./my-key.json) -> service-account key (.json) created in the previous [project](../Docker&SQL/ReadMe.md).

The ETL pipeline __green_taxi_data__ inside of the project created in Mage are:

- __load_green_taxi_data__ -> Data loader block used to read data for the final quarter of 2020 (months 10,11,12).
- __transform_green_taxi_data__ -> Transformer block used to transform the extracted data:
    - Removing rows where the passenger count and the trip distance are both equals to zero.
    - Creating a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    - Renaming columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    - Adding three assertions:
        - vendor_id is one of the existing values in the column (currently)
        - passenger_count is greater than 0
        - trip_distance is greater than 0.
        
        . Replace the table if it already exists.
- __export_green_taxi_data_PostgresDB__ -> Exporter block used to write the dataset to a table called green_taxi in a schema mage. Such table will be replaced if it already exists.
- __export_green_taxi_data_gcp_parquet__ -> Exporter block used to write the dataset as a parquet file to a bucket in GCP. 
- __export_green_taxi_data_gcp_parquet_partitioned__ -> Exporter block used to write the dataset as parquet files to a bucket in GCP, partitioned by lpep_pickup_date, by using the pyarrow library.
- __export_green_taxi_data_gcp_BigQuery__ -> Exporter block used to insert the dataset in a table of a data warehouse in BigQuery.

For the latest three exporter block is necessary to modify the configuration file __io_config.yaml__ in the mage project by modifing the settings to access to GCP services

```bash
# Google
GOOGLE_SERVICE_ACC_KEY_FILEPATH: "/home/src/my-key.json"
GOOGLE_LOCATION: <your_location> # Optional
```
## Requirements
To start this project of Mage and then running the ETL process, you wiil need of the following requirements:

- docker
- docker-compose
- GCP account

## Run
To start the Mage project, you can execute the following command:

```bash
cd <path_current_folder>
sudo docker-compose up
```
Then you can access to the Mage project and run the ETL process to extract, transform and load data in postgres and GCP, by accessing the url of the corresponding container in your laptop

```bash
http://localhost:6789
```

## Data Analysis
To analize the data extracted, there will be different options:
- access to BigQuery Studio GCP service of your account
- access to postgres container in your laptop by using jupyter to access to the database that contains the extracted data

```bash
# Import libraries
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

# Loading environment variables from .env file
# load_dotenv() will first look for a .env file and if it finds one, 
# it will load the environment variables from the file and make them accessible to your project 
# like any other environment variable would be
load_dotenv()

POSTGRES_DBNAME=os.getenv('POSTGRES_DBNAME')
POSTGRES_SCHEMA=os.getenv('POSTGRES_SCHEMA')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST=os.getenv('POSTGRES_HOST')
POSTGRES_PORT=os.getenv('POSTGRES_PORT')

# Create connection with database
engine = create_engine(f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DBNAME}")

# Execute query
query_example=f'SELECT * FROM {POSTGRES_SCHEMA}.green_taxi;'
pd.read_sql(sql=query_example, con=engine)
```
