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