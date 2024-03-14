#Import libraries
import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

# Set environment variable GOOGLE_APPLICATION_CREDENTIALS that is used by pa.fs.GcsFileSystem()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/my-key.json'
# Set bucket name
bucket_name = 'mage-bucket-apeduto'
# Set project id
project_id = 'iron-pottery-412215'
# Set table name
table_name = 'green_taxi_data'
# Set root path
root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    # Patition of data by data['lpep_pickup_date']
    table = pa.Table.from_pandas(data)
    gcs = pa.fs.GcsFileSystem()
    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols = ['lpep_pickup_date'],
        filesystem = gcs
    )