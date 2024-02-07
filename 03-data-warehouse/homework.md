### Load 2022 green data into BigQuery

#### Setup

##### Step 1 - Load green data into cloud storage
Since the is no transformation, we will not use mage in this case (it would be like using a gun to kill a mousquito)

1. download the data localy from the following link : 

https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-*.parquet

```
def extract_data(url, month):
    """Doanload the data from the url localy"""
    file_name = f"green_data/green_tripdata_2022-{month}.parquet"
    os.system(f'wget {url} -O {file_name}')
    return file_name
```

2. Load the data directly to cloud storage without any transformation.

* first make sure to install google cloud utilities (cloud storage in this case) :
```
conda install google-cloud-storage
```

* next, extract the google credential to path, so you can connect to google cloud:
```
export GOOGLE_APPLICATION_CREDENTIALS="path to your service account json file"
```

* next import parquet file into cloud storage :
```
from google.cloud import storage

def write_to_bucket(filename, bucket_name, folder_name):
    """Write green data parquet file into the given bucket"""
    # Instasiate a client
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    sub_file = filename.split('/')
    # The destination blob is just the name of our file into cloud storage
    destination_blob = bucket.blob(f'{folder_name}/{sub_file[1]}')

    destination_blob.upload_from_filename(filename)
    print(f"file {filename} uploaded to {destination_blob}")
```

* our main looks like the following :
```
def main():
    """Main for the program"""
    # Name of the bucket 
    bucket_name = 'dtc_data_lake_drux-de-zoomcamp'
    #folder name
    folder_name = 'green_data_2022'
    semi_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022"
    months = ['01', '02', '03', '04', '05', '06', 
              '07', '08', '09', '10', '11', '12']
    for month in months:
        url = f"{semi_url}-{month}.parquet"
        filename = extract_data(url, month)
        write_to_bucket(filename, bucket_name, folder_name)
```

##### Step 2 
###### strep2.1 Create an external table into BigQuery
We will create an external table, based on the parquet file loaded into cloud storage :
```
-- creating an external table from green taxi data of 2022
create or replace external table `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022`
options (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-bucket-drux/green_data_2022/green_tripdata_2022-*.parquet']
);
```

let's check that we have our data :
```
select * from `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022` limit 10
```
Make sure that the bucket and the dataset are in the same region, or you will not be able to query the data, even if you succed in creating the external table.

Note that the external table is not stored into BigQuery, it is actually stored into google cloud storage.

###### strep2.2 Create a materialized table into BigQuery
Now we can create a materialised table from the external table created previously.
```
-- creating the table from the external table
create or replace table `drux-de-zoomcamp.ny_taxi.green_tripdata_2022` as (

  select * from `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022`

);
```

##### question 1
count of records for the 2022 Green taxi data
```
-- count of records for the 2022 Green Taxi Data
select count(*) from `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022` ;
-- 840402
```

##### question 2
Estimated amount of data that will be read whe running the queries on external and materialised table
```
-- count distinct number of PULocationIDs
-- external table -- 0 MB
select count(distinct PULocationID) from `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022`; 

-- materialized table -- 6.41 MB
select count(distinct PULocationID) from `drux-de-zoomcamp.ny_taxi.green_tripdata_2022`;  -- 6.41MB
```

##### question 3
Number of records that have a fare_mount of 0
```
-- number of rows with fare_amount = 0
select count(*) from `drux-de-zoomcamp.ny_taxi.external_green_tripdata_2022`
where fare_amount = 0;
```
##### question 4

