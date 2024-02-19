#!/usr/bin/env python
# coding: utf-8
# author: drux31 <contact@lnts.me>
# date : 2024-02-18
"""
    File for preparing data for the week
"""
import urllib.request
import urllib.error
import pandas as pd
#import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import types
import argparse
import os
import sys

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""
    parser = argparse \
        .ArgumentParser(description='Dowload csv files from github.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('year', type=int, help='YEAR TO DOWNLOAD FROM!')
    parser.add_argument('service', type=str, help='SERVICE TO DOWNLOAD!')

    return parser.parse_args()

# --------------------------------------------------
def main():
    """Process the files"""
    args = get_args()
    year = args.year
    service = args.service

    semi_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
    months = ['01', '02', '03', '04', '05', '06', 
              '07', '08', '09', '10', '11', '12']
    
    for month in months:
        # csv file_name
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"
        full_url = f"{semi_url}{service}/{file_name}"
        print (full_url)
        os.makedirs(f'../data/csv/{service}/{year}/{month}')
        try:
            res = urllib.request.urlretrieve(full_url, f"../data/csv/{service}/{year}/{month}/{file_name}")
            print(f"created {file_name} in ../data/csv/{service}/{year}/{month}/")
        except:
           print(repr(sys.exception()))

# --------------------------------------------------
if __name__ == '__main__':
    main()

