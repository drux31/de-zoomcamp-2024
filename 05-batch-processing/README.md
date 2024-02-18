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
I'm using version 3.3 of Spark.

