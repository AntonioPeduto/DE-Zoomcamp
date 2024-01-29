#! /bin/bash

# ----------------------------------------------------------------------------------------
# This script has been created for creation of docker containers and data-ingestion process
# starting from a url from which downloading a data source file  
# then extracting the information from the source file
# and finally loading such information into a target table into a database. 
# All thiese steps defined inside of docker containers
# and using POSTEGRES, PGADMIN and python
# ----------------------------------------------------------------------------------------

# 1) Creation of containers inside of te same network.
# Such containers are defined inside of the file "docker-compose.yaml"
sudo docker compose up -d


# 2) Creation of image defined by the Dockerfile -> data-ingestion:v1
sudo docker build -t data-ingestion:v1  ./data-ingestion



# 3) Creation/execution of a container from the image data-ingestion:v1
# for data-ingestion of the table green_trip_data
sudo docker run -it \
--network docker_pg-network \
data-ingestion:v1 \
--user=root \
--password=root \
--host=pg-postgres \
--port=5432 \
--dbname=ny_taxi \
--table=green_trip_data \
--url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"



# 4) Creation/execution of a container from the image data-ingestion:v1
# for data-ingestion of the table taxi_zone
sudo docker run -it \
--network docker_pg-network \
data-ingestion:v1 \
--user=root \
--password=root \
--host=pg-postgres \
--port=5432 \
--dbname=ny_taxi \
--table=taxi_zone \
--url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"