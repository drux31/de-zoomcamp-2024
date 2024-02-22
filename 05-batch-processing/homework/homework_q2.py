#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-22
"""
    Spark - Homework question 2
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import pandas as pd
import urllib.request


#fhv_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-10.csv.gz'

filename = 'fhv_tripdata_2019-10.csv.gz'
#urllib.request.urlretrieve(fhv_url, f"../data/csv/fhv/{filename}")

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

schema = types.StructType([
        types.StructField('dispatching_base_num', types.StringType(), True),
        types.StructField('pickup_datetime', types.TimestampType(), True), 
        types.StructField('dropoff_datetime', types.TimestampType(), True),
        types.StructField('PULocationID', types.IntegerType(), True), 
        types.StructField('DOLocationID', types.IntegerType(), True), 
        types.StructField('SR_Flag', types.IntegerType(), True), 
        types.StructField('Affiliated_base_number',types.StringType(), True)
    ])

df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv(f'../data/csv/fhv/{filename}')

output_path = '../data/parquet/fhv/'

while True:
    df.show()
    
    df \
    .repartition(6) \
    .write.parquet(output_path)

    res = input('type "q" to end the program--> ')
    if res == 'q':
        break

spark.stop()
    
    