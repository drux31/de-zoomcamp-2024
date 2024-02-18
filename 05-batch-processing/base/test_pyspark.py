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

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('../data/taxi_zone_lookup.csv')

df.show()

#df.write.parquet('../data/zones')
#print("creating parquet file")
print(pyspark.__file__)

# For UI to stick
time.sleep(5000)