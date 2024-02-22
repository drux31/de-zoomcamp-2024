#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-22
"""
    Spark - Homework question 3
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

df_fhv = spark.read.parquet('../data/parquet/fhv/*')
df_fhv.registerTempTable('fhv_data')

while True:
    df_fhv.show()
    spark.sql("""
            select 
                pickup_datetime,
                dropoff_datetime,
                datediff(hour, pickup_datetime, dropoff_datetime) as longest_trip_in_hour
            from
                fhv_data
            order by 3 desc
            limit 10                    
            """).show()
    
    res = input('type "q" to end the program--> ')
    if res == 'q':
        break

spark.stop()
    
    