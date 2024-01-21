#!/usr/bin/env python
# coding: utf-8

"""
This script is a simple pipeline to load the yellow taxi trips
data into postgres db runing in docker
"""
import configparser
#from shutil import unpack_archive
import psycopg2
import pandas as pd
import csv

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
df = pd.read_csv('data/taxi_zone_lookup.csv', nrows=100)
print(df)

'''
-->  generate the schema
the following line extracts the structure of the df
and generate the equivalent database schema (table definitions)
'''
ddl_table_creation = pd.io.sql.get_schema(df, name='zones')
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
# Create a new CSV file in which
# null values are replaced by zeros
# https://stackoverflow.com/questions/47151375/python-modifying-a-csv-file
try :
    with conn.cursor() as cur :
        with open('data/taxi_zone_lookup.csv', encoding='utf8') as f:
            '''Load the new output.csv file into postgres'''
            cur.execute('drop table if exists zones;')
            cur.execute(ddl_table_creation)
            next(f)
            cur.copy_from(f, 'zones', sep=',')
            
        cur.execute('select count(*) from zones;')
        data = cur.fetchall()
        print(data)
        f.close()
except :
    conn.rollback()
    raise
else :
    conn.commit()
finally :
    conn.close()