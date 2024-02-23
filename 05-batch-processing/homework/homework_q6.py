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

## Loading zones
schema_zones = types.StructType([
                    types.StructField('locationid', types.IntegerType(), True), 
                    types.StructField('borough', types.StringType(), True), 
                    types.StructField('zone', types.StringType(), True), 
                    types.StructField('service_zone', types.StringType(), True)
                    ])
df_zones = spark.read \
    .option("header", "true") \
    .schema(schema_zones) \
    .csv('../data/taxi_zone_lookup.csv')
df_zones.createOrReplaceTempView('zones_data')

while True:
    '''
    fhv schema
    dispatching_base_num|    
    pickup_datetime|   
    dropoff_datetime|
    PULocationID|
    DOLocationID|
    SR_Flag|
    Affiliated_base_number
    '''
    df_zones.show()

    spark.sql("""
            select 
                z1.zone as pickup_zone,
                count(1) as nb_pickups
            from
                fhv_data fhv
            join zones_data z1 on z1.locationid = fhv.PULocationID
            group by 1
            order by 2 asc
            limit 10                    
            """).show()
    
    res = input('type "q" to end the program--> ')
    if res == 'q':
        break

spark.stop()
    
    