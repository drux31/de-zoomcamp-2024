#!/usr/bin/env python
# coding: utf-8

"""
This script is a simple pipeline to load the yellow taxi trips
data into postgres db runing in docker
"""
import configparser
from shutil import unpack_archive
from pathlib import Path
#from glob import glob
import psycopg2
import pandas as pd
import csv
from datetime import datetime

# get db postgres connection info
parser = configparser.ConfigParser()
parser.read("pipeline.conf")

dbname = parser.get("pg_config", "database")
user = parser.get("pg_config", "username")
password = parser.get("pg_config", "password")
host = parser.get("pg_config", "host")
port = parser.get("pg_config", "port")

# Read the CSV file with pandas (we're reading only the firts 100 lines)
# because the file contains more than 1 million lines
df = pd.read_csv('data/yellow_tripdata_2021-01.csv', nrows=100)

## print the df
#print(df)


# convert "tpep_pickup_datetime" and and "tpep_dropoff_datetime"
# from Text to datetime
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

'''
-->  generate the schema
the following line extracts the structure of the df
and generate the equivalent database schema (table definitions)
'''
ddl_table_creation = pd.io.sql.get_schema(df, name='yellow_taxi_data')
print(ddl_table_creation)

## we will covert the colums   "tpep_pickup_datetime" 
## and "tpep_dropoff_datetime" from TEXT to datatime.
## using python csv package only 

#create the db connection
conn = psycopg2.connect(f"dbname={dbname} " +
                        f"user={user} " +
                        f"password={password} " +
                        f"host={host}", 
                        port=port)

#create a cursor
file_name = 'data/yellow_tripdata_2021-01.csv'


# Create a new CSV file in which
# null values are replaced by zeros
# https://stackoverflow.com/questions/47151375/python-modifying-a-csv-file


try :
    with conn.cursor() as cur :
        with open(f'{file_name}', 'r', encoding="utf8") as file :
            cur.execute('drop table if exists yellow_taxi_data;')
            cur.execute(ddl_table_creation)
            next(file)
            cur.copy_from(file,
                            'yellow_taxi_data',
                            sep=',',
                            columns=('VendorID', 
                                     'tpep_pickup_datetime', 
                                     'tpep_dropoff_datetime',
                                     'passenger_count',
                                     'trip_distance', 
                                     'RatecodeID',
                                     'store_and_fwd_flag', 
                                     'PULocationID',
                                     'DOLocationID',
                                     'payment_type',
                                     'fare_amount',
                                     'extra',
                                     'mta_tax',
                                     'tip_amount',
                                     'tolls_amount', 
                                     'improvement_surcharge',
                                     'total_amount', 
                                     'congestion_surcharge'))
            cur.execute('select count(*) from yellow_taxi_data;')
            data = cur.fetchall()
            print(data)
        file.close()
except :
    conn.rollback()
    raise
else :
    conn.commit()
finally :
    conn.close()

'''
with open('data/output.csv', 'w', newline='') as f:
    fieldnames = [
                  'VendorID', 
                  'tpep_pickup_datetime', 
                  'tpep_dropoff_datetime',
                  'passenger_count',
                  'trip_distance', 
                  'RatecodeID',
                  'store_and_fwd_flag', 
                  'PULocationID',
                  'DOLocationID',
                  'payment_type',
                  'fare_amount',
                  'extra',
                  'mta_tax',
                  'tip_amount',
                  'tolls_amount', 
                   'improvement_surcharge',
                   'total_amount', 
                   'congestion_surcharge'
                   ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    with open('data/yellow_head_100.csv', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            print(row)
            writer.writerow(
                {
                  'VendorID': row['VendorID'],
                  'tpep_pickup_datetime': datetime.strptime(row['tpep_pickup_datetime'], '%Y-%m-%d %H:%M:%S'), 
                  'tpep_dropoff_datetime': datetime.strptime(row['tpep_dropoff_datetime'], '%Y-%m-%d %H:%M:%S'),
                  'passenger_count': row['passenger_count'],
                  'trip_distance': row['trip_distance'], 
                  'RatecodeID': row['RatecodeID'],
                  'store_and_fwd_flag': row['store_and_fwd_flag'],  
                  'PULocationID': row['PULocationID'],
                  'DOLocationID': row['DOLocationID'],
                  'payment_type': row['payment_type'],
                  'fare_amount': row['fare_amount'],
                  'extra': row['extra'],
                  'mta_tax': row['mta_tax'],
                  'tip_amount': row['tip_amount'],
                  'tolls_amount': row['tolls_amount'], 
                   'improvement_surcharge': row['improvement_surcharge'],
                   'total_amount': row['total_amount'], 
                   'congestion_surcharge': row['congestion_surcharge']
                }
            )
            #print((row['tpep_pickup_datetime']))
            #print('datetime version : ', datetime.strptime(row['tpep_pickup_datetime'], '%Y-%m-%d %H:%M:%S'))
        csvfile.close()
f.close()
df_output = pd.read_csv('data/output.csv')
print(pd.io.sql.get_schema(df_output, name='yellow_taxi_data_bis'))

'''