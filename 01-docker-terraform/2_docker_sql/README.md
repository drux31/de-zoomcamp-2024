### Docker and SQL

#### Docker
Docker is a container. Those are sets of platform as a service, that use OS-level virtualization to deliver a packaged software. They are great for isolation, configuration and fast deployment.
You can have several container running in a host machine, and communicating with each others via configured channels.

&rarr; Why use docker for a data enginner ?
* reproductibility ;
* fast setup for local experiment ;
* integration test (CI/CD) ;
* running pipelines on the cloud ;
* experimenting specific tools (Spark, serverless - AWS Lambda).

&rarr; For our lesson :
inside the working directory :
1. create a docker file called Dockefile (```touch Dockerfile```);

2. add some information ; for example, we would a docker container running python 3.9 with pandas installed :
	```
	FROM Python:3.9 # will use python 3.9 or greater
	
	RUN pip install pandas # install the additional pandas library
	
	ENTRYPOINT [ "bash" ] # use bash as an executable environment
	```
3. build the docker image :
	```
	docker build -t test:pandas .
	```
	we basically ask docker to build and image with the tag test:pandas in the current repository (the dot at the end), using the existing Dockerfile.
	
4. Once you've built the image, you can run the container :
	```
	docker run -it test:pandas
	```
	This will launch a new bash terminal with python3.9 and pandas installed, and you're all set.

5. Now we can change our Dockerfile slightly :
	```
	FROM python3:.9

	RUN pip install pandas 

	WORKDIR /app # new line added #1

	COPY pipeline.py pipeline.py # this will copy our local pipeline file to container.

	ENTRYPOINT ["python", "pipeline.py"] # this new version tells docker to execute the pipeline python file.

	```

6. Create a pipeline.py python file (you can copy the one in 2_docker_sql/basic folder) ;

7. execute steps 3 and 4 again to see the result.

That's it for the basics.

#### sql
##### Installing postgres in Docker

in order to postgres with docker, run the following command :
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5431:5432 \
postgres:14.3 
```
When this code is executed, it launches a container with a running postgres database, waiting for a connection. Since I already have a postgres db running on my local machine, I'll use the port 5431 and forward it to the 5432 port that my local machine is listening to.
In order to connect, to newly create db  (you should be prompted to type your password -- root in our case):
```
pgcli -h localhost -p 5431 -U root -d ny_taxi
```
when connected, you should see this :
```
Server: PostgreSQL 14.3 (Debian 14.3-1.pgdg110+1)
Version: 3.5.0
Home: http://pgcli.com
root@localhost:ny_taxi>
```
pgcli is client that allos to connect to a pg database, with a prettier interface than the native client (pgsql).

###### Ingestion script
We will build a script that will download a CSV file from the internet and load it into our postgres db running into docker.
1. create the ingestion file :
```
touch upload-data.py
```
this file wil contain the script for downloading CSV file about the NYC yellow trip data and  and inserting it into postgres. Look into the file in the repo.
Some tips : 
to dowload the yellow taxi data we will use : 
```
get https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```
Once downloaded, we cannot load it immediately into panda because the file is too big. So in order to analyze it, we will create a small chunk that we will use to study the data : 
```
gzip -d yellow_tripdata_2021-01.csv.gz # this will unzip the file
head -n 100 yellow_tripdata_2021-01.csv > yellow_head_100.csv # This will copy the first 100 lines into a new file called yeallow_head_100.csv
```

We can now proceed to the analysis of our data, using openoffice or excel. You can also directly open the file using pandas in the ```upload-data.py``` file: 
```
import pandas as pd

'''
create a new padans dataframe with only a 100 lines
for a short analysis. Opening the complete file would 
cause some perf issues, the file having more than 1 million
lines
'''
df = pd.read_csv('data/yellow_tripdata_2021-01.csv', nrows=100)
print(df)
```
By printing the Dataframe, you have a glimpse of the data you're manipulating. You can also take a look at the [data dictionnary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) which has detailed information about the data.

I decided to use python CSV package and psycopg2 only to load my data into the postgres in Docker. But you can follow the official course by using Pandas. I only used Pandas for the followings :
* convert the pickup and dropoff datetime from string to datetime : 
```
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
```

* extract the table definition script ; note that it is not completely correct, but it is sufficient for our purpous here
```
ddl_table_creation = pd.io.sql.get_schema(df, name='yellow_taxi_data')
print(ddl_table_creation)
```

I used a variable beacause I will use it later in my file.

Having our table definition script, it's time to load the data into postgres. You can have a look in the upload-data.csv file. What I did globally was : 
* read the CSV file in order to remove empty data (VendorID and passenger_count). Those were causing error during the loading file (Trying to insert enpty string into an integer field) ;
* created a new CSV file with the cleansed data ;
* loaded the new the CSV file into postgres using the method copy_from, from the cursor of psycopg2.
My objective is later to ennhance the speed of the loading script, just using those tools. 
After loading my database, i have 1271413 rows instead of 1369765, because I removed the empty data.


#### Dockerizing the ingestion script
We will dockerize our upload-data.py. If you worked on Jupyter notebook, remember to first transform your file into a python file:
```
jupyter nbconvert --to=script filename.ipynb
```

At first, we will parameterize the script, givig database name, table name and CSV url as input. The other information a carried within the config file.

Since we are using a configuration file (see ```pipeline.conf```) , we are going to give only two parameters (instead of what is in the course) : 
* table name ;
* url for downloading the CSV file.

I you take a look in the file ```ingest_data.py``` , you'll notice that we changed our script, so that we need to call it like this :
```
./ingest_data.py yellow_taxi_data https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

We directly execute our file, since we added a **shebang** (```#!/usr/bin/env python```) and made our file executable (```chmod +x ingest_data.py```). the output after the execution is something like this : 
```
VendorID tpep_pickup_datetime tpep_dropoff_datetime  passenger_count  trip_distance  ...  tip_amount tolls_amount  improvement_surcharge  total_amount  congestion_surcharge
0         1  2021-01-01 00:30:10   2021-01-01 00:36:12                1           2.10  ...        0.00            0                    0.3         11.80                   2.5
1         1  2021-01-01 00:51:20   2021-01-01 00:52:19                1           0.20  ...        0.00            0                    0.3          4.30                   0.0
2         1  2021-01-01 00:43:30   2021-01-01 01:11:06                1          14.70  ...        8.65            0                    0.3         51.95                   0.0
3         1  2021-01-01 00:15:48   2021-01-01 00:31:01                0          10.60  ...        6.05            0                    0.3         36.35                   0.0
4         2  2021-01-01 00:31:49   2021-01-01 00:48:21                1           4.94  ...        4.06            0                    0.3         24.36                   2.5
5         1  2021-01-01 00:16:29   2021-01-01 00:24:30                1           1.60  ...        2.35            0                    0.3         14.15                   2.5
6         1  2021-01-01 00:00:28   2021-01-01 00:17:28                1           4.10  ...        0.00            0                    0.3         17.30                   0.0
7         1  2021-01-01 00:12:29   2021-01-01 00:30:34                1           5.70  ...        0.00            0                    0.3         21.80                   2.5
8         1  2021-01-01 00:39:16   2021-01-01 01:00:13                1           9.10  ...        0.00            0                    0.3         28.80                   0.0
9         1  2021-01-01 00:26:12   2021-01-01 00:39:46                2           2.70  ...        3.15            0                    0.3         18.95                   2.5

[10 rows x 18 columns]
CREATE TABLE "yellow_taxi_data" (
"VendorID" INTEGER,
  "tpep_pickup_datetime" TIMESTAMP,
  "tpep_dropoff_datetime" TIMESTAMP,
  "passenger_count" INTEGER,
  "trip_distance" REAL,
  "RatecodeID" INTEGER,
  "store_and_fwd_flag" TEXT,
  "PULocationID" INTEGER,
  "DOLocationID" INTEGER,
  "payment_type" INTEGER,
  "fare_amount" REAL,
  "extra" REAL,
  "mta_tax" REAL,
  "tip_amount" REAL,
  "tolls_amount" INTEGER,
  "improvement_surcharge" REAL,
  "total_amount" REAL,
  "congestion_surcharge" REAL
)
[(1369765,)]
Database connection terminated
```

The execution should take some time, which is normal but it is ok for the purpous at hand. However, notice that the script can be greatly optimized.

Now that our script is parametrized, we can now create our docker file (Dockerfile): 
```
FROM python:3.9.1

RUN apt-get install wget

RUN pip install pandas psycopg2-binary

WORKDIR /app

COPY ingest_data.py ingest_data.py

COPY pipeline.conf pipeline.conf # configuration file

RUN mkdir /app/data

ENTRYPOINT [ "python", "ingest_data.py" ]
```

Some points are important to note here :
 * configuration file with sensitive datas should not be included in the image (expacially if it's chared ; I did this here for the purpous of simplicity ;
 * you should create a .dockerignore in your working directory if you have other files than the one needed to build your image, or you can create a subdirectory (which I did).

to create our image : 
```
docker build -t taxi_ingest:v001 .
```

Now we are ready to run our image ; but first,  we need to create a network so our image can connect to the container with the postgres database :

```
docker network create pg-network
```

Now we launch our container with postgres in the network :
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5431:5432 \
--network=pg-network \
--name pg-database \
postgres:14.3
```

After that, we have to change our config file like this :
```
host = pg-database
port = 5432
username = root
password = root
database = ny_taxi
```

and now we're ready to execute our containerized ingestion script  :
```
docker run --network=pg-network taxi_ingest:v001 \
yellow_taxi_data \
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```
