#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-18
"""
    Testing pyspark
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import pandas as pd


spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('../data/fhvhv_tripdata_2021-06.csv')

## Loop to persist the Spark cluster
while True:
    
    df.show()
    print(df.head(5), '\n')
    print(df.schema, '\n')

    print('Testting with panda dataframe')
    df_pd = pd.read_csv('../data/head_1001.csv')
    print(df_pd, df_pd.dtypes, '\n')

    print('creating a spark  dataframe from pandas')
    df1 = spark.createDataFrame(df_pd)
    print(df1.schema)

    schema = types.StructType([
        types.StructField('dispatching_base_num', types.StringType(), True),
        types.StructField('pickup_datetime', types.TimestampType(), True), 
        types.StructField('dropoff_datetime', types.TimestampType(), True),
        types.StructField('PULocationID', types.IntegerType(), True), 
        types.StructField('DOLocationID', types.IntegerType(), True), 
        types.StructField('SR_Flag', types.IntegerType(), True), 
        types.StructField('Affiliated_base_number',types.StringType(), True)
    ])
    
    print('new Spark dataframe with persisted schema')
    df = spark.read \
        .option("header", "true") \
        .schema(schema) \
        .csv('../data/fhvhv_tripdata_2021-06.csv')
    
    ## df.show() prints 20 lines,
    #so we use heads to limit the number of printed lines
    print(df.head(5))

    ## Creating repartition with spark for processing distribution
    df = df.repartition(24)

    #Write the chunked files to parquet locally
    df.write.parquet('../data/fhvhv/2021/06/')

    s = input('type "q" to end the program--> ')
    if s == "q":
        break