### Module 6 - Homework
This homework will extend Module 5 homework, alowing to learn about streming with PySpark.

Instead of Kafka, we will use Red Panda, which is a drop-in replacement for Kafka.
   > Dataset used : 2019-10 data - https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz

#### Start Red Panda 
First we need to get the docker container from redpanda [github repo](https://github.com/redpanda-data-blog/2023-python-gsg/blob/main/docker-compose.yml). 
Once the ```dock-compose.yml``` file is downloaded, we can run the following command :
```
docker-compose up -d # The -d is for detached mode
```

#### Question 1 - Red Panda version
&rarr; first, exec the container : ```docker exec -it redpanda-1 bash```
&rarr; then execute the help command : ```rpk help```
&rarr; finaly, check the version : ```rpk version```

* Another alternative can be done in two commands : 
1. first command: ```docker exec -it redpanda-1 bash -c "rpk help"```
2. second command: ```docker exec -it redpanda-1 bash -c "rpk version"```

result: **v22.3.5 (rev 28b2443)**

#### Question 2 - Creating a topic
Using the command rpk, create a topic:
1. command: ```docker exec -it redpanda-1 bash -c "rpk topic create test-topic"```

result: 

```
TOPIC       STATUS
test-topic  OK
```

#### Question 3 - Connect to Kafka server
working wwith python 3.12, I had to install kafka-python-ng :

```
pip install kafka-python-ng
```

Provided that you can connect to the server, what's the output of the last command?
result: ```True``` 

#### Question 4 - Sending data to the stream
Let's send some data from the producer.
1. How much time did it take? &rarr; **0.51 seconds**
2. Where did it spend most of the time? &rarr; **Sending the messages**

3. Sending taxi data
```
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
        FROM read_csv('data/{filename}') \
        limit 10;"

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
    topic_name = 'test-topic'

    for row in df_green.itertuples(index=False):
        row_dict = {col: getattr(row, col) for col in row._fields}
        producer.send(topic_name, value=row_dict)
        print(f"Sent: {row_dict}")
        time.sleep(0.05)

        time.sleep(0.05)
    t1bis = time.time()
    t0ter = time.time()
    producer.flush()
    t1ter = time.time()
    t1 = time.time()

    print(f'sending the message took {(t1bis - t0bis):.2f} seconds')
    print(f'flushing took {(t1ter - t0ter):.2f} seconds')
    print(f'took {(t1 - t0):.2f} seconds')

    k = input("\nType 'q' to quit: ")
    if k == 'q':
        break
```

#### Question 5 - Sending the Trip Data
1. Create a topic green-trips and send the data there: 

* create a topic:
``` 
docker exec -it redpanda-1 bash -c "rpk topic create green-trips"
## Result:
TOPIC        STATUS
green-topic  OK
```

* send the data:
``` 
docker exec -it redpanda-1 bash -c "rpk topic consume green-trips"
```

2. How much time in seconds did it take? (You can round it to a whole number)
&rarr; took 134 seconds

#### Question 6 - Parsing the data

When applying the schema, wow does the record look after parsing? Copy the output :
```
Row(lpep_pickup_datetime='2019-10-01 00:26:02', lpep_dropoff_datetime='2019-10-01 00:39:58', PULocationID=112, DOLocationID=196, passenger_count=1.0, trip_distance=5.88, tip_amount=0.0)
```

#### Question 7 - Most popular destination
