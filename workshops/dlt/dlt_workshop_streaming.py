#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date : 2024-02-08
'''
python code from dlt workshop
- Downloading a file from an API, using stream processing
'''

import requests
import json

def download_and_yield_rows(url):
    response = requests.get(url, stream=True)
    response.raise_for_status() #raise an HTTPError for bad responses
    
    for line in response.iter_lines():
        if line:
            yield json.loads(line)


url = "https://storage.googleapis.com/dtc_zoomcamp_api/yellow_tripdata_2009-06.jsonl"


i = 0
# Use the generator to iterate over rows with minimal memory usage
for row in download_and_yield_rows(url):
    #process each row as needed
    print(row)
    i += 1
    if i == 10:
        break