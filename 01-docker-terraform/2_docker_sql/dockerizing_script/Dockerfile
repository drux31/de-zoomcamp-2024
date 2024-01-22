FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas psycopg2-binary

WORKDIR /app
COPY ingest_data.py ingest_data.py
COPY pipeline.conf pipeline.conf
RUN mkdir /app/data

ENTRYPOINT [ "python", "ingest_data.py" ]
