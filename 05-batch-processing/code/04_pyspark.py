#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-18
"""
    Testing pyspark
"""
import pyspark
import time # for keeping the spark job running
from pyspark.sql import SparkSession
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items

while True:

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .getOrCreate()

    # We will use the measurement file generated for the 1 billion raw chalenge
    df = spark.read \
        .option("header", "true") \
        .text('../data/fhvhv_tripdata_2021-06.csv')
    
    df.show()
    print(df.head(5), '\n')
    print(df.schema, '\n')

    print('Testting with panda dataframe')
    df_pd = pd.read_csv('../data/head_1001.csv')
    print(df_pd, df_pd.dtypes, '\n')

    print('creating a spark  dataframe from pandas')
    spark.createDataFrame(df_pd).show()
    
    s = input('type "quit" to end the program--> ')
    if s == "quit":
        break

# For UI to stick
#time.sleep(5000)