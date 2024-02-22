#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-22
"""
    Testing Spark SQL
"""
import pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .getOrCreate()

## Preparing the data
df_green = spark.read.parquet('../data/parquet/green/*/*')
df_yellow = spark.read.parquet('../data/parquet/yellow/*/*')

df_green = df_green \
    .withColumnRenamed('lpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime', 'dropoff_datetime')
df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime', 'pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime', 'dropoff_datetime')

## Common coluns
common_collumns = []
yellow_cols = set (df_yellow.columns)
for col in df_green.columns:
    if col in yellow_cols:
        common_collumns.append(col)

df_green_sel = df_green \
                .select(common_collumns) \
                .withColumn('service_type', F.lit('green'))

df_yellow_sel = df_yellow \
                .select(common_collumns) \
                .withColumn('service_type', F.lit('yellow'))

## Creating the fact trip data :
df_trip_data = df_green_sel.unionAll(df_yellow_sel)
df_trip_data.registerTempTable('trips_data')

while True:
    '''
    |-- dispatching_base_num: string (nullable = true)
    |-- pickup_datetime: timestamp (nullable = true)
    |-- dropoff_datetime: timestamp (nullable = true)
    |-- PULocationID: integer (nullable = true)
    |-- DOLocationID: integer (nullable = true)
    |-- SR_Flag: integer (nullable = true)
    |-- Affiliated_base_number: string (nullable = true)
    '''
    print('What do you want to do ?: ')
    print('"sy" --> show the yellow dataframe\n',
          '"sg" --> show the green dataframe\n',
          '"scy" --> to print the yellow dataframe schema\n',
          '"scg" --> to print the green dataframe schema\n',
          '"set" --> to print the shared colums between both dataset\n',
          '"gy" --> to print the row count by service type\n',
          '"gys" --> to print the row count by service type using sql query\n',
          '"rm" --> Show the monthly revenue by zones\n',
          '"q" --> to quit the program\n',
          '-----------------------------------------------------\n')
    s = input('Your choice--> ')
    match s:
        case 'q':
            break
        case 'sg':
            df_green.show()
        case 'scg':
            df_green.printSchema()
        case 'sy':
            df_yellow.show()
        case 'scy':
            df_yellow.printSchema()
        case 'set':
            print(common_collumns)
        case 'gy':
            df_trip_data \
                .filter(F.year('pickup_datetime').isin([2020, 2021])) \
                .groupBy('service_type') \
                .count() \
                .show()
            '''
            df_trip_data.groupBy('service_type') \
                .count() \
                .show()
            '''
        case 'gys':
            spark.sql("""
            select 
                service_type,
                count(1)
            from
                trips_data
            where extract(year from pickup_datetime) in (2020, 2021)
            group by service_type
            
            """).show()
        case 'rm':
            spark.sql("""
            select 
                -- Reveneue grouping 
                PULocationID as revenue_zone,
                date_trunc('month', pickup_datetime) as revenue_month, 
                service_type, 

                -- Revenue calculation 
                sum(fare_amount) as revenue_monthly_fare,
                sum(extra) as revenue_monthly_extra,
                sum(mta_tax) as revenue_monthly_mta_tax,
                sum(tip_amount) as revenue_monthly_tip_amount,
                sum(tolls_amount) as revenue_monthly_tolls_amount,
                sum(improvement_surcharge) as revenue_monthly_improvement_surcharge,
                sum(total_amount) as revenue_monthly_total_amount,

                -- Additional calculations
                count(1) as total_monthly_trips,
                avg(passenger_count) as avg_montly_passenger_count,
                avg(trip_distance) as avg_montly_trip_distance

            from trips_data
            where extract(year from pickup_datetime) in (2020, 2021)
            group by revenue_zone, revenue_month, service_type
            
            """).show()
        
spark.stop()
# For UI to stick
#time.sleep(5000)