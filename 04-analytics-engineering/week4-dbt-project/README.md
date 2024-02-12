## DBT Project 
for this section, we're working from dbt cloud. We ill need to first create and configure the project with the following:
* define a name for our project ;
* configure the connection with a datawarehouse (BigQuery in this case) ;
* configure the connection with a code supervision repo (github in our case).

Once it is done, not that dbt do not allow to work on the main branch, so we will need to create another branch dedicated to our project. 
Also, the repo is synced automaticaly with the github.

### Initialise the project
Once we created our branch, we can **initialize the project**. This will create a folder dedicated to the project into the github repo provided.
A lot of files a created during the initialisation, but we will put our focus on **dbt_project.yml** first. 
