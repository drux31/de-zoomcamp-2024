#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-19
"""
    Transforming CSV Taxi data into parquet
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import pandas as pd
import argparse
import os

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""
    parser = argparse \
        .ArgumentParser(description='Dowload csv files from github.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('year', type=int, help='YEAR TO DOWNLOAD FROM!')
    parser.add_argument('service', type=str, help='SERVICE TO DOWNLOAD!')

    return parser.parse_args()


# --------------------------------------------------
def get_schema(service):
    """generate the schema for the given service"""
    match service:
        case 'green':
            green_schema = types.StructType([
                types.StructField("VendorID", types.IntegerType(), True),
                types.StructField("lpep_pickup_datetime", types.TimestampType(), True),
                types.StructField("lpep_dropoff_datetime", types.TimestampType(), True),
                types.StructField("store_and_fwd_flag", types.StringType(), True),
                types.StructField("RatecodeID", types.IntegerType(), True),
                types.StructField("PULocationID", types.IntegerType(), True),
                types.StructField("DOLocationID", types.IntegerType(), True),
                types.StructField("passenger_count", types.IntegerType(), True),
                types.StructField("trip_distance", types.FloatType(), True),
                types.StructField("fare_amount", types.FloatType(), True),
                types.StructField("extra", types.FloatType(), True),
                types.StructField("mta_tax", types.FloatType(), True),
                types.StructField("tip_amount", types.FloatType(), True),
                types.StructField("tolls_amount", types.FloatType(), True),
                types.StructField("ehail_fee", types.FloatType(), True),
                types.StructField("improvement_surcharge", types.FloatType(), True),
                types.StructField("total_amount", types.FloatType(), True),
                types.StructField("payment_type", types.IntegerType(), True),
                types.StructField("trip_type", types.IntegerType(), True),
                types.StructField("congestion_surcharge", types.FloatType(), True)
            ])
            return green_schema
        case 'yellow':
            yellow_schema = types.StructType([
                types.StructField("VendorID", types.IntegerType(), True),
                types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
                types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
                types.StructField("passenger_count", types.IntegerType(), True),
                types.StructField("trip_distance", types.FloatType(), True),
                types.StructField("RatecodeID", types.IntegerType(), True),
                types.StructField("store_and_fwd_flag", types.StringType(), True),
                types.StructField("PULocationID", types.IntegerType(), True),
                types.StructField("DOLocationID", types.IntegerType(), True),
                types.StructField("payment_type", types.IntegerType(), True),
                types.StructField("fare_amount", types.FloatType(), True),
                types.StructField("extra", types.FloatType(), True),
                types.StructField("mta_tax", types.FloatType(), True),
                types.StructField("tip_amount", types.FloatType(), True),
                types.StructField("tolls_amount", types.FloatType(), True),
                types.StructField("improvement_surcharge", types.FloatType(), True),
                types.StructField("total_amount", types.FloatType(), True),
                types.StructField("congestion_surcharge", types.FloatType(), True)
            ])
            return yellow_schema


# --------------------------------------------------
def create_parquet(service, input_path, output_path, schema):
    """write parquet file"""
    spark = SparkSession.builder \
            .master("local[*]") \
            .appName('test') \
            .getOrCreate()

    df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv(input_path)

    df \
    .repartition(12) \
    .write.parquet(output_path)


# --------------------------------------------------
def get_months(year):
    """return the number of months equivalent to the year"""
    if year == 2021:
        return ['01', '02', '03', '04', '05', '06', '07']
    else:
        return ['01', '02', '03', '04', '05', '06', 
              '07', '08', '09', '10', '11', '12']


# --------------------------------------------------
def main():
    """Process the files"""
    args = get_args()
    year = args.year
    service = args.service
  
    schema = get_schema(service)
    print(schema)
    months = get_months(year)
    for month in months:
        input_path = f'../data/csv/{service}/{year}/{month}/'
        #os.makedirs(f'../data/parquet/{service}/{year}/{month}')
        output_path = f'../data/parquet/{service}/{year}/{month}/'
        create_parquet(service, input_path, output_path, schema)


# --------------------------------------------------
if __name__ == '__main__':
    main()