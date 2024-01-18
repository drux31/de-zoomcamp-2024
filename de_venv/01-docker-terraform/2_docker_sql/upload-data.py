
#!/usr/bin/env python
# coding: utf-8

"""
This script is a simple pipeline to load the yellow taxi trips
data into postgres db runing in docker
"""
#import configparser
from shutil import unpack_archive
from pathlib import Path
#from glob import glob
#import psycopg2
import pandas as pd

# get db postgres connection info
#parser = configparser.ConfigParser()
#parser.read("pipeline.conf")

# Read the CSV file with pandas (we're reading only the firts 100 lines)
# because the file contains more than 1 million lines
df = pd.read_csv('data/yellow_tripdata_2021-01.csv', nrows=100)

print(df)