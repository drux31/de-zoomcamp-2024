### Project general architecture
![alt general architecture for the capstone project](<capstone project architecture.png>)

#### Staging 
The data is extracted from the web and stored into a duckDB database, into a staging schema.
we then need to install only duckDB :
```
pip install duckdb
```
Since we using mainly Python and SQL, there are no additional packages needed.

#### Transformation
For the transformation part, we wil work with dbt-core and duckDB as an underlying datawarehouse.

We then need to install dbt-core and the ducdb extension : 
```
pip install dbt-core dbt-duckdb
```