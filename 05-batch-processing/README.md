## Batch processing

There are multiple ways of processing data:
* batch processing - the topic of this week ;
* streaming processing.

Batch processing can be defined as the act of creating one pipeline in order to load an entire dataset in one single job, that can be scheduled to run on a defined time basis.

Stream processing on the other hand, is an event based pipeline job that will run if trigered by the pre identified event.

The focus of this week will be batch processing. Batch jobs are generaly programmed to run daily or hourly, they can be also scheduled to run weekly or even many times per hour.

### Advantages of batch jobs
Batch jobs have many advantages, some of them are the following :
* they are easy to manage - since the job workflow is pretty linear ;
* they can be rerun easily - in case anything happen ;
* easy to scale - either up or down depending on the volume of data to process.

The main disadvantage is the delay of loading the data. However, in many cases there is no need in loading the data in real time.

### Technologies
The technologies for batch processing are usaly programming languages like python scripts or SQL, or other tools like Spark (batch) or Flink (streamin). the last two are frameworks for distributed data processing.

In the previous weeks, we saw how to process data in batch using either SQL or Python scipts, so the focus will be processing with Spark.

### Spark
Apache Spark is a large-scale engine processing. Data can be processed either on a single node or on multiple nodes; it is also a multi language processing engine. It can be used with Java and Scala. Spark is actually written in scala, so the native way of communicating with Spark is scala, but there are wrappers for other languages like Python or R. The one for python is actualy popular and is called PySpark. Even though we cover Spark for batch here, it can also be used for streaming.

What are use cases for Spark:
* process data from a datalake ;
* transform data for machine learning training.

#### Installing Spark
Spark works fine with Java version 8, 11 or 17.
download spark : https://spark.apache.org/downloads.html
I'm using version 3.4.2 of Spark.

Spark has a system called partition that enables the possibility of processing a large file in distributed manner, by chunking it in smaller files and speeding up the process.

##### Spark dataframe
A DataFrame is a Dataset organized into named columns. It is conceptually equivalent to a table in a relational table. Functions applied on a Spark dataframe are ether actions or transformations. Transformations are lazy functions, meaning they are not executed immediately ; they are actually triggered when called with an action functions (eager), which execute immediately.

Spark also offers some functions and user defined functions. Those can help to implement a specific business logic that cannot be defined using sql queries. But most of the time, it's better to combine Spark with SQL queries.

##### Spark SQL (SparQL)
Spark has built in functions that enable to apply querying operation similar to SQL. however, it's also possible to use SQL directly, by creating a temporary table with the dataframe being manipulated, as followed :

```
df_name.registerTempTable('temporary_table_name')
```

Then you can write sql queries calling your temporary table :
```
spark.sql(
"""
select *
from 
    temporary_table_name
""")
```

This offer a great advantage in having the possibility to query files in a datalake using SQL.

##### Spark internals
This paragraph is mainly about spark cluster and the way they work to optimize the data processing.


#### Troubleshouting:
If you encounter the following error :
```
AttributeError: 'DataFrame' object has no attribute 'iteritems'. Did you mean: 'isetitem'?
```

Note that Pandas remove iteritems from version 2 and onward, so if using a Spark version inferior to 3.4, you can either downgrade the version of panda to 1.5.3, or use the following hack if you don't want to downgrade pandas :
```
import pandas as pd
pd.DataFrame.iteritems = pd.DataFrame.items
```

Or you could also upgrade Spark version to at least 3.4.1 (since it seems the issue solved from there).
source --> https://stackoverflow.com/questions/76404811/attributeerror-dataframe-object-has-no-attribute-iteritems