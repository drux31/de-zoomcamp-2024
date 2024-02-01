### Week 2 - Homework
The goal is to construct an ETL pipeline that loads the data, performs some transformations, and writes the data to a dataabase or google cloud.

#### Create a new pipeline
First we create a pipeline named ```green_taxi_etl``` (via the Mage UI).

#### Add a data loader block
the data will read the final quarter or 2020 (months 10, 11, 12) using pandas.

```
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    green_data = 'green_tripdata_2020'
    months = [10, 11, 12]
    folder = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green'
    temp_data = []    
    
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'Passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID': pd.Int64Dtype(),
                    'store_and_fwd_flag': str,
                    'PULocationID': pd.Int64Dtype(),
                    'DOLocationID': pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra': float,
                    'mta_tax': float,
                    'tip_amount': float,
                    'tolls_amount': float,
                    'improvement_surcharge': float,
                    'total_amount': float,
                    'congestion_surcharge': float
                }
    
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    for m in months:
        url = f"{folder}/{green_data}-{m}.csv.gz"
        temp_data.append(pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates))
    
    return pd.concat(temp_data)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output.head() is not None, 'The output is undefined'

```

#### Add a transformer block
the transformer block should perform the following : 
* Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
* Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
* Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
* Add three assertions:
    * vendor_id is one of the existing values in the column (currently)
    * passenger_count is greater than 0
    * trip_distance is greater than 0

```
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Preprocessing: column befor rename - {data.columns[0]}")
    print(f"Preprocessing: rows with a null vendor ID column : {data['VendorID'].isna().sum()}")
    print(f"Preprocessing: rows with a zero trip distance: {data['trip_distance'].isin([0]).sum()}")
    
    print('\n')
    data = data[data['passenger_count'] > 0]
    print('-- removing rows with zero passenger_count')
    data = data[data['trip_distance'] > 0]
    print('-- removing rows with zero trip_distance')
    data = data.dropna(subset=['VendorID'])
    print('-- removing rows with NA vendor id')
    data = data.rename(columns={"VendorID": "vendor_id"})
    print('-- renaming column')
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    print('-- adding a new column')
    print('\n')
    print(f"Postprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")
    print(f"Postrocessing: column befor rename - {data.columns[0]}")
    print(f"Postrocessing: adding a new column - {data.columns[20]}")
    print(f"Postprocessing: rows with a null vendor ID column : {data['vendor_id'].isna().sum()}")
    print(f"Postprocessing: rows with zero passengers: {data['trip_distance'].isin([0]).sum()}")
    print('\n')

    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with no trip distance'
    assert output['vendor_id'].isna().sum() == 0, 'The vendor ID Has no value'

```

#### Create a data exporter 
##### Postgres (SQL Loader)
* schema name: mage ;
* table name: green_taxi ;
* write policy: replace.
* querry: ```select * from {{ df_1 }}```

##### Google (Python)

We reused a big part of the code used to load yellow data into GCS :

```
import pyarrow as pa
import pyarrow.parquet as pq 
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/google-credential-file.json"

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
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
```
#### Scheduling the pipeline
The trigger is created via the UI, and the code is exported into a YAML file as seen below :
```
triggers:
- envs: []
  name: green_data_pipeline_scheduler
  pipeline_uuid: green_taxi_etl
  schedule_interval: '@daily'
  schedule_type: time
  settings: {}
  sla: null
  start_time: 2024-02-02 05:00:00
  status: inactive
  variables: {}
```

#### Questions 
1. data loading- nb rows once the dataset is loaded :  ```266,855 rows x 20 columns``` ;
2. data transformation - nb rows left unppon filtering: ```139,370 rows``` ;
3. data transformation - command creating a new column : ```data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date``` ;
4. data transformation - existing values of VendorID in the dataset: 1 or 2 ;
5. data transformation - number of columns needed to be renamed : 4 ;
6. data exporting - number of partitions : 56.

