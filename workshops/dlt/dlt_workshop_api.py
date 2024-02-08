#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date : 2024-02-08
'''
python code from dlt workshop
- Downloading paginated data from a API
'''

import requests

BASE_API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

def paginated_getter():
    """function for streaming the data from the API"""
    page_number = 1
    while True:
        # set the query parameters
        params = {'page': page_number}

        #Make a get request to the API
        response = requests.get(BASE_API_URL, params=params)
        response.raise_for_status() #Raise an HTTPError for bad responses
        page_json = response.json()
        print(f'got the {page_number} with {len(page_json)} records.')

        #if the page has no records, stop iterating
        if page_json:
            yield page_json
            page_number += 1
        else:
            #No more data, break the loop
            break

if __name__ == "__main__":
    """Use the generator to iterate over pages"""
    for page_data in paginated_getter():
        #Process each page as needed
        print(page_data)