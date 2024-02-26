#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date : 2024-02-26
'''
python code from dlt workshop
- Downloading a file from an API, using stream processing
'''

import requests
import gzip

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from structure import schema
import duckdb

def web_to_local(short_url):
    """
    Download the file and save it locally for future use
    """
    #filename = 'openfoodfacts-products.jsonl.gz'
    filename= 'en.openfoodfacts.org.products.csv.gz'
    url = f'{short_url}/{filename}'
    response = requests.get(url, stream=True)
    response.raise_for_status() #raise an HTTPError for bad responses
    
    with open(f'../data/{filename}', 'wb') as fd:
        n = 1
        for chunk in response.iter_content(chunk_size=102400):
            fd.write(chunk)
            print(f"written chunck {n}")
            n+=1
        fd.close()
    return filename


def read_and_yield_rows(filename):
    """
    Read the file from the local storage
    """
    with gzip.open(f'../data/{filename}', 'rb') as fd:
        for line in fd:
            if line:
                yield line.decode()


def main(short_url):
    """
    main data ingestion function
    """
    i = 0
    #filename = web_to_local(short_url)
    filename= 'en.openfoodfacts.org.products.csv.gz'
    # Use the generator to iterate over rows with minimal memory usage
    for row in read_and_yield_rows(filename):
        #process each row as needed
        print(row, '\n')

        i += 1
        if i == 2:
            break

    spark = (
        SparkSession.builder
        .master("local[*]") 
        .appName('project') 
        .getOrCreate()
    )
    cursor = duckdb.connect()
    print(cursor.execute('SELECT 42').fetchall())

    df_foods = (
            spark.read 
            .schema(schema) 
            .option("header", "true") 
            .option("delimiter", "\t")
            .csv(f'../data/{filename}')
    )
    
    df_foods.select(df_foods.code, 
                    df_foods.creator,
                    df_foods.quantity,
                    df_foods.nutriscore_score,
                    df_foods.data_quality_errors_tags,
                    df_foods.ecoscore_score).show()
    #df_foods.show()
    
if __name__ == "__main__":
    short_url = 'https://static.openfoodfacts.org/data'
    #https://static.openfoodfacts.org/data/
    main(short_url)