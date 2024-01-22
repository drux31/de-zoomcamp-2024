#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2023-01-21
"""
This script is a simple pipeline to load the yellow taxi trips
data into postgres db runing in docker
"""
import configparser
import gzip
#from shutil import unpack_archive
import os
from pathlib import Path
from glob import glob
import argparse
import psycopg2
import pandas as pd
import csv

def get_args():
    '''
    Getting input args
    Parameters : 
        -- table name for the data to be stored
        -- url of the CSV
    '''
    parser = argparse.ArgumentParser(description='Ingest CSV data into Postgres')
    parser.add_argument('table_name', help='Table name for postgres')
    parser.add_argument('url', help='URL for the CSV file to load into Postgres')
    args = parser.parse_args()
    return args


def get_db():
    '''Get the DB parameters : 
        Postgres connection info
    '''
    # get db postgres connection info
    config_parser = configparser.ConfigParser()
    config_parser.read("pipeline.conf")
    return config_parser


def extract_data(url: str) -> str :
    '''
    get the URL parameter and download the corresponding 
    CSV file
    '''
    # checking the url extension
    if url.endswith('.csv.gz'):
        csv_name = 'data/output.csv.gz'
    else:
        csv_name = 'data/output.csv'

    #Downloading the file
    os.system(f'wget {url} -O {csv_name}')
    return csv_name


def main() :
    params = get_args()
    config_parser = get_db()
    table_name = params.table_name
    url = params.url

    gzip_file = extract_data(url)
    
    dbname = config_parser.get("pg_config", "database")
    user = config_parser.get("pg_config", "username")
    password = config_parser.get("pg_config", "password")
    host = config_parser.get("pg_config", "host")
    port = config_parser.get("pg_config", "port")

    # Read the CSV file with pandas (we're reading only the firts 100 lines)
    # because the file contains more than 1 million lines
    df = pd.read_csv(gzip_file, nrows=10, compression='gzip')
    print(df)

    # convert "tpep_pickup_datetime" and and "tpep_dropoff_datetime"
    # from Text to datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    '''
    -->  generate the schema
    the following line extracts the structure of the df
    and generate the equivalent database schema (table definitions)
    '''
    ddl_table_creation = pd.io.sql.get_schema(df, name=table_name)
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
        query = f"""
        insert into {table_name} 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        table_dl = """
        CREATE TABLE yellow_taxi_data (
            VendorID INTEGER,
            tpep_pickup_datetime TIMESTAMP,
            tpep_dropoff_datetime TIMESTAMP,
            passenger_count INTEGER,
            trip_distance REAL,
            RatecodeID INTEGER,
            store_and_fwd_flag TEXT,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            payment_type INTEGER,
            fare_amount REAL,
            extra REAL,
            mta_tax REAL,
            tip_amount REAL,
            tolls_amount REAL,
            improvement_surcharge REAL,
            total_amount REAL,
            congestion_surcharge REAL
        );
        """
        
        with conn.cursor() as cur :
            with gzip.open(gzip_file, 'rt') as gz_file:
                csv_obj = csv.DictReader(gz_file, delimiter=',') 
                #, quoting=csv.QUOTE_NONNUMERIC)
                #next(csv_obj)
                #cur.copy_from(csv_obj, table_name, sep=',')
                records = []
                for row in csv_obj:
                    VendorID = row['VendorID'] if len(row['VendorID']) > 0 else '0'
                    tpep_pickup_datetime = row['tpep_pickup_datetime']
                    tpep_dropoff_datetime = row['tpep_dropoff_datetime']
                    passenger_count = row['passenger_count'] if len(row['passenger_count']) > 0 else '0'
                    trip_distance = row['trip_distance']
                    RatecodeID = row['RatecodeID'] if len(row['RatecodeID']) > 0 else '0'
                    store_and_fwd_flag = row['store_and_fwd_flag']
                    PULocationID = row['PULocationID'] if len(row['PULocationID']) > 0 else '265'
                    DOLocationID = row['DOLocationID'] if len(row['PULocationID']) > 0 else '265'
                    payment_type = row['payment_type'] if len(row['payment_type']) > 0 else '5'
                    fare_amount = row['fare_amount']
                    extra = row['extra']
                    mta_tax = row['mta_tax']
                    tip_amount = row['tip_amount']
                    tolls_amount = row['tolls_amount']
                    improvement_surcharge = row['improvement_surcharge']
                    total_amount = row['total_amount']
                    congestion_surcharge = row['congestion_surcharge']
                    if len(VendorID) <= 0:
                        VendorID = '0'
                    
                    test = (VendorID, 
                            tpep_pickup_datetime,
                            tpep_dropoff_datetime,
                            passenger_count,
                            trip_distance,
                            RatecodeID,
                            store_and_fwd_flag,
                            PULocationID,
                            DOLocationID,
                            payment_type,
                            fare_amount,
                            extra,
                            mta_tax,
                            tip_amount,
                            tolls_amount,
                            improvement_surcharge,
                            total_amount,
                            congestion_surcharge)
                    #records = '(' + ', '.join(row) + ',)'
                    #print(query, test)
                    records.append(test)

                cur.execute(f'drop table if exists {table_name};')
                cur.execute(table_dl)
                cur.executemany(query, records)

                cur.execute(f'select count(*) from {table_name};')  
                data = cur.fetchall()
                print(data)              
                gz_file.close()
    except(Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        print("Exception with insertion: ",error)
    else :
        conn.commit()
    finally :
        if conn is not None:
            conn.close()
            print("Database connection terminated")


if __name__ == '__main__':
    main()