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

globally, What we have done is the following : 
* Load data from the internet to postgres ;
* configure GCP and set a service account for Mage ;
* Load parquet data from the internet to a GCS Bucket ;
* Partitioning a large parquet file, in order to speed up the loading to GCS ;
* Create a pipeline to load data from GCS to BigQuery, enabling a trigger to run the pipeline on schduled time (triggers are actualy what allow schduling in Mage).

We did also dig into some advanced practices like parameterizing pipelines, backfilling or deployment.
We mainly worked with batch pipelines, but Mage also offers streming or data integration pipelines.

  

#### Troubleshooting
* You encounter an error about the port of postgres being already used, change the port into the .env file to 5431.
* If your block run in an infinite loop or you cannot load Mage terminal, just type **docker-compose down** in the terminal to kill everything properly and load Mage again (**docker-compose up**)
* If the **select 1;** does not work, set the service account role to **owner**, it should solve the issue.