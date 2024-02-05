## Module 3 - Data warehouse
A data warehouse is a system that aggregates data from different sources into a single, central and consistent data store to support data analysis. It is used for On Line Analytical Processing (OLAP), which differs from On Line Transactionnal Processing (OLTP), suited for production systems.

### Components of a data warehouse architecture 

![Alt text](image.png)

source : [IBM/data-warehouse](https://www.ibm.com/topics/data-warehouse)

* **ETL**: It is a process of moving data from the source to the data warehouse ;
* **Metadata**: data giving information about the data into the warehouse ;
* **Staging area**: sometimes, the architecture of a data warehouse includes a staging area, which is a data base for storing raw data from all the sources, during the process of ETL, before loading it into the data warehouse.

### BigQuery
BigQuery is a serverless data warehouse (meaning there are no servers to manage or database software to install). It offers scalability and high availabity.
It has built in feature like machine learning, geospatial analysis or business intelligence. It maximizes flexibility by separating the compute engine that analyzes data from the storage.

#### Loading data into bigquery
We will have to load the 2022 green data into external table (from parquet format). See homework for the process.