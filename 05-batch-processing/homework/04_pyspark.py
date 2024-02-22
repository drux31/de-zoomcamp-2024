#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-22
"""
    Spark - Homework
"""
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import pandas as pd

while True:

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('homework') \
        .getOrCreate()

    print(spark.version)
    break
spark.stop()
    
    