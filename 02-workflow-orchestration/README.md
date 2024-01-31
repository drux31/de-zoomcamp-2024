### Week 2 - Workflow orchestration (with Mage)
The purpose of the course is to learn about ETL architecture, working with Mage as an orchestrator, Postgres and BigQuery as databases, and GCS for storage.

#### What is workflow orchestration ?
Orchestration can be difined as a process of dependency management through automation, with the idea of minimizing manual work. This process is built upon the sequential stemps required by workflows.
Workflows can be also identified as DAGs (for Directed acyclic graphs), or the actual pipelines that are handled by the orchestrator. A good orchestrator will prioritize developper experience, based on three principles : 
* Flow state ;
* Feedback loos ;
* cognitive load.

#### What is Mage ?
Mage is an open source pipeline tool for orchestrating, transforming and integrating data. Mage has a three components hierarchical layer :
* Projects --> those are on the top of the layer ;
* Pipelines (or workflows) ;
* Blocks which are actual code executing tasks like Load, Transform or Export data.

##### Working with Mage

To install mage, we will use docker. 
* the folder used to work on mage can be downloaded from github :
	```
	git clone https://github.com/mage-ai/mage-zoomcamp mage-zoomcamp
	```

* make a local copy of the dev.env file :
```
cd mage-zoomcamp
cp dev.env .env #.env is already in the .gitignore
```

* then we can run our fist command : 
```
docker-compose build #this will build the images needed to work with Mage
```

* check we have the latest version :
```
docker pull mageai/mageai:latest
```
* Now we can start mage :
```
docker compose up
```

To acces the mage instance : 
```
locahost:6789 #don't forget to forward the port if working in a remote machine
```

#### Configuring postgres
in order to connect mage to postgres, we will create a dev config, in order to load env variables from docker : 
```
dev:
	# PostgresSQL
	POSTGRES_CONNECT_TIMEOUT: 10
	POSTGRES_DBNAME: "{{ env_var(POSTGRES_DBNAME) }}"
	POSTGRES_SCHEMA: "{{ env_var(POSTGRES_SCHEMA) }}"
	POSTGRES_USER: "{{ env_var(POSTGRES_USER) }}"
	POSTGRES_PASSWORD: "{{ env_var(POSTGRES_PASSWORD) }}"
	POSTGRES_HOST: "{{ env_var(POSTGRES_HOST) }}"
	POSTGRES_PORT: "{{ env_var(POSTGRES_PORT) }}"
```

Once the connection is configured, we can build our pipeline to load taxi data from internet to postgres. The code will not be detailed here, it can be found into the source files.

#### Troubleshooting
* You encounter an error about the port of postgres being already used, change the port into the .env file to 5431.
* If your block run in an infinite loop or you cannot load Mage terminal, just type **docker-compose down** in the terminal to kill everything properly and load Mage again (**docker-compose up**)