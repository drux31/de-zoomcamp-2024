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
from psycopg2 import extras
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
            next(file) # skip the first line
            
            #cur.copy_from(file, 'yellow_taxi_data', sep=',')
            
            for row in file:
                print(row)
                if row[3] == 0:
                    continue
                
                if len(row[0]) <= 0:
                    row[0] = '0'
                cur.execute("""
                            insert into yellow_taxi_data
                            "values
                            (%d, %s, %s, %d, %s, %d, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)
                            """, 
                            row)

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