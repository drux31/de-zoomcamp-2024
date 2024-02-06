### Load 2022 green data into BigQuery

#### Step 1 - Load green data into cloud storage
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