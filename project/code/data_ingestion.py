#!/usr/bin/env python
# coding: utf-8
# author : drux31<contact@lnts.me>
# date : 2024-02-26
'''
python for data ingestion/extraction for the project
'''
import duckdb
from queries import query_union_lieux, query_union_usagers

def get_con(db_name):
    """Open a connection with duckdb"""
    con = duckdb.connect(db_name)
    return con

def create_staging(db_name):
    """read data from duckdb database"""
    con = get_con(db_name)
    ## Create the staging schema
    con.sql("CREATE SCHEMA IF NOT EXISTS staging")
    con.sql("select table_schema, table_name, table_type"
            + " from information_schema.tables").show()
    '''
    # Load the usagers data
    con.sql("create or replace table staging.usagers_all as ("
            + query_union_usagers + ")")
    con.sql("select count(*) from staging.usagers_all").show()
    con.sql("drop table staging.usagers_all")

    #Load the lieux data  
    con.sql("create or replace table staging.lieux_all as ("
            + query_union_lieux + ")")
    con.sql("select count(*) from staging.lieux_all").show()
    con.sql("drop table staging.lieux_all")
    '''
    con.sql("describe raw_data.caracteristiques_2019").show()
    con.sql("describe raw_data.caracteristiques_2020").show()
    con.sql("describe raw_data.caracteristiques_2021").show()
    con.sql("describe raw_data.caracteristiques_2022").show()

    con.close()

def main(db_name):
    """
    main data ingestion function
    """
    create_staging(db_name)
    
if __name__ == "__main__":
    main(db_name='project.db')