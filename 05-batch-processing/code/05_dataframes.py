#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-18
"""
    Testing pyspark Dataframes
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items

spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .getOrCreate()
    
df = spark.read.parquet('../data/fhvhv/2021/06/')

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
    print('"s" --> to print the dataframe with some columns\n',
          '"f" --> to print on spefific column value\n',
          '"sc" --> to print the dataframe schema\n',
          '"d" --> to print formated date\n',
          '"q" --> to quit the program\n',
          '-----------------------------------------------------\n')
    s = input('Your choice--> ')
    match s:
        case 'q':
            break
        case 's':
            df.select('dispatching_base_num', 'pickup_datetime', 'dropoff_datetime').show()
        case 'sc':
            df.printSchema()
        case 'f':
            df.select('dispatching_base_num', 'pickup_datetime', 
                      'dropoff_datetime') \
                      .filter(df.dispatching_base_num == 'B02764') \
                      .show()
        case 'd':
                        df.select('dispatching_base_num', 
                                  F.to_date('pickup_datetime'), 
                                  'dropoff_datetime') \
                      .filter(df.dispatching_base_num == 'B02764') \
                      .show()
# For UI to stick
#time.sleep(5000)