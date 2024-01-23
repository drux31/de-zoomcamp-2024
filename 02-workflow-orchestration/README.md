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

