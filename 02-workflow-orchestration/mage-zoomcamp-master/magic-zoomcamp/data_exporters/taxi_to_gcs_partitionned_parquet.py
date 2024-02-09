import pyarrow as pa
import pyarrow.parquet as pq 
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/drux-de-zoomcamp-mage-demo.json"

bucket_name = 'mage-zoomcamp-drux'
project_id = "drux-de-zoomcamp"

table_name = "green_taxi_data"

root_path = f'{bucket_name}/{table_name}'

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data(data, *args, **kwargs) -> None:
  
    table = pa.Table.from_pandas(data)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['tpep_pickup_date'],
        filesystem=gcs
    )