#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date : 2024-02-08
'''
python code from dlt workshop
-- Downloading a single file from an API
-- This practice should be avoided as the whole file will be loaded
-- into memory if we need to process it afterward.
'''

import requests
import json

url = "https://storage.googleapis.com/dtc_zoomcamp_api/yellow_tripdata_2009-06.jsonl"

def download_and_read_json_url(url):
    response = requests.get(url)
    response.raise_for_status() #raise an HTTPError for bad responses
    data = response.text.splitlines()
    parsed_data = [json.loads(line) for line in data]
    return parsed_data

downloaded_data = download_and_read_json_url(url)

if downloaded_data:
    # Process or print the downloaded data as needed
    print(downloaded_data[:5])