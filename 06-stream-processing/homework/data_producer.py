import json
import time
from kafka import KafkaProducer
import duckdb
import pandas as pd


filename = 'green_tripdata_2019-10.csv'
query = f"SELECT lpep_pickup_datetime, \
                 lpep_dropoff_datetime, \
                 PULocationID, \
                 DOLocationID, \
                 passenger_count, \
                 trip_distance, \
                 tip_amount \
        FROM read_csv('data/{filename}') limit 10;"

duckdb.sql(query).write_csv("data/head_green_data.csv")
print("Done")


def json_serializer(data):
    return json.dumps(data).encode('utf-8')

server = 'localhost:9092'

producer = KafkaProducer(

    bootstrap_servers=[server],
    value_serializer=json_serializer
)

df_green = pd.read_csv('data/head_green_data.csv')

while True:
    print(producer.bootstrap_connected())

    t0 = time.time()

    t0bis = time.time()
    topic_name = 'green-trips'

    for row in df_green.itertuples(index=False):
        row_dict = {col: getattr(row, col) for col in row._fields}
        producer.send(topic_name, value=row_dict)
        print(f"Sent: {row_dict}")
    t1bis = time.time()
    t0ter = time.time()
    producer.flush()
    producer.close()
    t1ter = time.time()
    t1 = time.time()

    print(f'sending the message took {(t1bis - t0bis):.2f} seconds')
    print(f'flushing took {(t1ter - t0ter):.2f} seconds')
    print(f'took {(t1 - t0):.2f} seconds')

    k = input("\nType 'q' to quit: ")
    if k == 'q':
        break