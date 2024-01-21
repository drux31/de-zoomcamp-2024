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
        csv_name = 'output.csv.gz'
        compression = 'gzip'
    else:
        csv_name = 'data/output.csv'

    #Downloading the file
    #os.system(f'wget {url} -O data/{csv_name}')
    #unpack the CSV file if compressed
    if compression :
        #print(compression)
        file_name = Path(f'data/{csv_name}')
        #unzip the csv file
        repo = Path('data/')
        unpack_archive(file_name, repo) #, compression)

        #search for the unziped csv
        csv_file = glob('./data/*.csv')
        csv_name = csv_file[0]
    return csv_name


def main() :
    params = get_args()
    config_parser = get_db()
    table_name = params.table_name
    url = params.url

    csv_file = extract_data(url)

    dbname = config_parser.get("pg_config", "database")
    user = config_parser.get("pg_config", "username")
    password = config_parser.get("pg_config", "password")
    host = config_parser.get("pg_config", "host")
    port = config_parser.get("pg_config", "port")

    # Read the CSV file with pandas (we're reading only the firts 100 lines)
    # because the file contains more than 1 million lines
    df = pd.read_csv(csv_file, nrows=100)
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
        with conn.cursor() as cur :
            with open(csv_file, 
                    'r', 
                    encoding="utf8", 
                    newline='') as infile, open('data/output_bis.csv', 
                                                'w', 
                                                encoding="utf8", 
                                                newline='') as outfile:
                input = csv.DictReader(infile)
                output = csv.DictWriter(outfile, fieldnames=input.fieldnames)
                output.writeheader()
                for row in input:
                    if len(row['VendorID']) <= 0 or len(row['passenger_count']) <= 0:
                        continue
                    output.writerow(row)
                infile.close()
                outfile.close()
            with open('data/output_bis.csv', encoding='utf8') as f:
                '''Load the new output_bis.csv file into postgres'''
                cur.execute(f'drop table if exists {table_name};')
                cur.execute(ddl_table_creation)
                next(f)
                cur.copy_from(f, table_name, sep=',')
                
            cur.execute(f'select count(*) from {table_name};')
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


if __name__ == '__main__':
    main()