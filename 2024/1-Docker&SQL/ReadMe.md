# Docker & SQL

## Description
In this project we'll execute a data-ingestion process by extracting the information from two data source files specified by the following urls:

1. https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
2. https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

The information extracted from the two source files will be loaded into the two corresponding tables inside of a database created in a docker cointainer:

1. green_trip_data
2. taxi_zone

After the loading of data, such data can be analized by using a second container.
The architecture of the system is showed by the following image

![img](/Docker&SQL/images/DataIngestion.png)

The containers created are the following:
- __pg-postgres__ -> docker container created from the image __postgres:13__ to create a database in which to save data
- __data-ingestion__ -> docker container created from the image defined inside of the __Dockerfile__ to extract data from the source files and saving such data into the database inside of the container __pg-postgres__
- __pg-admin__ -> docker container created from the image __dpage/pgadmin__ to use the open source platform pgAdmin for data analysis.

### Directory tree
The files inside of the current directory "Docker&SQL" are showed by the following tree.

```bash
.
├── docker
│   ├── data
│   │   └── database
│   │       ├──...
│   ├── data-ingestion
│   │   ├── data-ingestion.py
│   │   └── Dockerfile
│   ├── docker-build&data-ingestion.sh
│   └── docker-compose.yaml
├── Homeworks.ipynb
├── images
│   ├── DataIngestion.png
│   ├── PGADMIN.png
│   └── PostgreSQL.png
├── ReadMe.md
└── terraform_with_variables
    ├── main.tf
    ├── terraform.tfstate
    ├── terraform.tfstate.backup
    └── variables.tf

```

where

- ./docker/data/database -> folder used to share data between host machine and containers
    to access all subfolder is necessary to change the permission by the following command:
    ```bash
    sudo chmod a+wrx <subfolder>
    ```
- ./docker -> folder containing all the files and subfolder used fro the data-ingestion process
- ./docker/data-ingestion -> folder containing files used to define a new image for the data-ingestion process
- ./terraform_with_variables -> folder containing files created to use Terraform
- ./Homeworks.ipynb -> file create to answer a few question by using jupyter lab and other packages.
- ./images -> folder containg the images used inside of this file (ReadMe.md)

## Requirements
To execute the data-ingestion process will be necessary install in your environment the following requirements:

- docker
- docker-compose

To work on the file __Homework.ipynb__ inyour host machine, additional requirements are necessary:
- python 3.9
- pandas
- sqlalchemy
- jupyter notebooks or jupyter lab
- GCP account
- terraform

### Seeting up environment

### Docker
You can install [docker engine](https://docs.docker.com/engine/) and [docker-compose](https://docs.docker.com/compose/install/) by following the instructions.

### Anaconda and conda
You can setup an environment in the host machine by using [Anaconda](https://www.anaconda.com/download).
#### Create environment
After installation of Anaconda, open the terminal and run the following command to setup your environment.
```bash
conda create -n <name_env> python=3.9
```
where __<name_env>__ represents the name of your conda environment.
Activate it:
```bash
conda activate <name_env>
```
Installing libraries by executing the following commands
```bash
conda install pandas sqlalchemy psycopg2
conda install -c conda-forge jupyterlab
```
### Terraform
You can install Terraform in your working environment by using the following [link](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/install-cli)

### GCP
You can use a free version (300 $ credits).

1. Create an account with your Google email ID
2. Setup your first project if you haven't already
    - example -> "DTC DE Course", and note down the "Project ID" (we'll use this later when deploying infra with TF)
3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/client-libraries) for this project
4. Grant the following roles: __Viewer__, __Storage Admin__, __Storage Object Admin__, __BigQuery Admin__.
5. Download service-account-keys (.json) for auth.
6. Install [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
7. Set environment variable to point to your downloaded GCP keys: 
```bash
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"
```
To export this environment variable to all session in your system, you can insert the previous command inside of the file __.bashrc__.
8. Enable these APIs for your project:
    
    - https://console.cloud.google.com/apis/library/iam.googleapis.com
    - https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com



## Execution data ingestion
To start the data-ingestion process will be sufficient to activate your __conda environment__ and to run the commands bash inside of the file __data-ingestion(data-ingestion.sh)__:

```bash
conda activate <name_env>
cd ./docker 
chmod u+wrx data-build&data-ingestion.sh
./data-build&data-ingestion.sh
```

## Data analysis
To open the file __Homeworks.ipynb__ you can use __jupyter lab__ by executing the following command:
```bash
cd ..
jupyter lab
```
then copy the link in the output of the previous command to open __jupyter lab__ in a browser.
To analize the data and to answer the questions inside of the file __Homeworks.ipynb__ you can access to PGADMIN inside of the specific container __pg-admin__ by a browser and access the address __localhost:8080__ to connect to the database __ny_taxi__ after having inserted credentials.
