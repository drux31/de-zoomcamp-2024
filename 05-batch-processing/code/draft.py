types.StructType([
    types.StructField('dispatching_base_num', types.StringType(), True),
    types.StructField('pickup_datetime', types.TimestampType(), True), 
    types.StructField('dropoff_datetime', types.TimestampType(), True),
    types.StructField('PULocationID', types.IntegerType(), True), 
    types.StructField('DOLocationID', types.IntegerType(), True), 
    types.StructField('SR_Flag', types.IntegerType(), True), 
    types.StructField('Affiliated_base_number',types.StringType(), True)
])


# --------------------------------------------------
def get_schema(service):
    """generate the schema for the given service"""
    match service:
        case 'green':
            green_schema = types.StructType([
                types.StructField("VendorID", types.IntegerType(), True),
                types.StructField("lpep_pickup_datetime", types.TimestampType(), True),
                types.StructField("lpep_dropoff_datetime", types.TimestampType(), True),
                types.StructField("store_and_fwd_flag", types.StringType(), True),
                types.StructField("RatecodeID", types.IntegerType(), True),
                types.StructField("PULocationID", types.IntegerType(), True),
                types.StructField("DOLocationID", types.IntegerType(), True),
                types.StructField("passenger_count", types.IntegerType(), True),
                types.StructField("trip_distance", types.FloatType(), True),
                types.StructField("fare_amount", types.FloatType(), True),
                types.StructField("extra", types.FloatType(), True),
                types.StructField("mta_tax", types.FloatType(), True),
                types.StructField("tip_amount", types.FloatType(), True),
                types.StructField("tolls_amount", types.FloatType(), True),
                types.StructField("ehail_fee", types.FloatType(), True),
                types.StructField("improvement_surcharge", types.FloatType(), True),
                types.StructField("total_amount", types.FloatType(), True),
                types.StructField("payment_type", types.IntegerType(), True),
                types.StructField("trip_type", types.IntegerType(), True),
                types.StructField("congestion_surcharge", types.FloatType(), True)
            ])
            yield green_schema
        case 'yellow':
            yellow_schema = types.StructType([
                types.StructField("VendorID", types.IntegerType(), True),
                types.StructField("tpep_pickup_datetime", types.TimestampType(), True),
                types.StructField("tpep_dropoff_datetime", types.TimestampType(), True),
                types.StructField("passenger_count", types.IntegerType(), True),
                types.StructField("trip_distance", types.FloatType(), True),
                types.StructField("RatecodeID", types.IntegerType(), True),
                types.StructField("store_and_fwd_flag", types.StringType(), True),
                types.StructField("PULocationID", types.IntegerType(), True),
                types.StructField("DOLocationID", types.IntegerType(), True),
                types.StructField("payment_type", types.IntegerType(), True),
                types.StructField("fare_amount", types.FloatType(), True),
                types.StructField("extra", types.FloatType(), True),
                types.StructField("mta_tax", types.FloatType(), True),
                types.StructField("tip_amount", types.FloatType(), True),
                types.StructField("tolls_amount", types.FloatType(), True),
                types.StructField("improvement_surcharge", types.FloatType(), True),
                types.StructField("total_amount", types.FloatType(), True),
                types.StructField("congestion_surcharge", types.FloatType(), True)
            ])
            yield yellow_schema



# --------------------------------------------------
def create_parquet_files(service, filename, year, service_schema):
    """
    Create and store parquet file from CSV
    with SPark
    """
    #ignite a Spark session
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName('test') \
        .getOrCreate()
    

    print('Create Spark dataframe with persisted schema')
    df = spark.read \
        .option("header", "true") \
        .schema(service_schema) \
        .csv(f'../data/fhvhv_tripdata_2021-06.csv')


