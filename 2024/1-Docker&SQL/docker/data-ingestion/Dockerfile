FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY data-ingestion.py data-ingestion.py

ENTRYPOINT ["python","data-ingestion.py"]