### Week 5 - Batch processing | homework
We put what we learned about Spark in practice with this homework.

#### Question 1 - out from executing spark.version

```
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

print(spark.version)
```

&rarr; answer : 3.4.2

#### Question 2 - FHV Ocotber 2019
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

![alt text](image.png)

&rarr; answer : 6MB

#### Question 3 - count records
How many taxi trips were there on the 15th of October? 
**Tips**: Consider only trips that started on the 15th of October. 

```
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .getOrCreate()

df_fhv = spark.read.parquet('../data/parquet/fhv/*')
df_fhv.registerTempTable('fhv_data')

spark.sql("""
        select 
            count(1)
        from
            fhv_data
        where 
            cast(pickup_datetime as date) = '2019-10-15'                        
        """).show()

```

&rarr; answer :

```
+--------+
|count(1)|
+--------+
|   62610|
+--------+
```

#### Question 4 - 