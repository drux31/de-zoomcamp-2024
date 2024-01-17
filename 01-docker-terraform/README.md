This first module is about seting up the environment. It is supposed to last two weeks.
The tools and language we are going to use are the followings :
* docker ;
* sql (using a postgres db since I am workng locally) ;
* Terraform. 

### Terraform & GCP

#### Terraform installation : 
all the instruction are available from [the official doc](https://developer.hashicorp.com/terraform/install#Linux). 
In my case, I decided to use the binary file :
1. downloaded the binary in my bin folder (~/bin/) :<br>
``
wget https://releases.hashicorp.com/terraform/1.6.6/terraform_1.6.6_linux_386.zip
`` 

2. unzip the downloaded file :<br>
``
unzip terraform_1.6.6_linux_386.zip
``

3. Test to see it's working :<br>
``
terraform --version
``
The output should be something like : <br>
terraform v1.6.6<br>
on linux_386 

4. Delete the zip file:<br>
``
rm terraform_1.6.6_linux_386.zip
``

I already had a GCP account from the previous cohort, so no particular config needed. We're all set for the course.

#### Terraform (little) presentation :
Terraform is an open source software for infrastructure as a code (IaaS).
&rarr; IaaS : Terraform, why ?
* simplicity in keeping track of infra ;
* easier collabolation ;
* reproductibility.

&rarr; why not :
* does not manage and update code on configuration ;
* does enable changes to immutable resources ;
* not used to manage resources not definfed in terraform.

terraform will run a provider on your local machine that will help you manage resources for a given provider (GCP in our case).

&rarr;  Key terraform command : 
* init - get me the provider I need ;
* plan - what am I about to do (once I define the resource I need) ;
* appy - execute and build the infrastructure as stated in the code ;
* destroy - will destroy everything in the terraform file.

For our lesson : 
1. create a service account on GCP (with Storage admin and BigQuery admin role);
2. create a terraform file (main.tf) with this [example](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build) and this [one for the bucket](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket)
3. instead of adding the path to the credentials in the file, create a local env variable setting the google credentials (terraform wil automatically fetch the credentials from the env path variable) : 
	```
	export GOOGLE_CREDENTIALS='absolute path to the service account's json credential file'
	```
	once the main.tf is created, run the following commands : 
	
	```
	1. terraform init
	2. terraform plan
	3. terraform apply
	```
####  Troubleshooting :
if you encouter the following error : 
Error: googleapi: Error 409: The requested bucket name is not available. The bucket namespace is shared by all users of the system. Please select a different name and try again., conflict

Just change the name of the bucket.

Terraform can also be used with [variables](https://developer.hashicorp.com/terraform/language/values/variables). You just create a variables.tf file, and call the variable name ine the main.tf with ```var.variable_name```

#### Official resources.
* [terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) ;
* [GCP](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md).

### Docker and SQL :

#### Docker
Docker is a container. Those are sets of platform as a service, that use OS-level virtualization to deliver a packaged software. They are great for isolation, configuration and fast deployment.
You can have several container running in a host machine, and communicating with each others via configured channels.

&rarr; Why use docker for a data enginner ?
* reproductibility ;
* fast setup for local experiment ;
* integration test (CI/CD) ;
* running pipelines on the cloud ;
* experimenting specific tools (Spark, serverless - AWS Lambda).

&rarr; For our lesson :
inside the working directory :
1. create a docker file called Dockefile (```touch Dockerfile```);

2. add some information ; for example, we would a docker container running python 3.9 with pandas installed :
	```
	FROM Python:3.9 # will use python 3.9 or greater
	
	RUN pip install pandas # install the additional pandas library
	
	ENTRYPOINT [ "bash" ] # use bash as an executable environment
	```
3. build the docker image :
	```
	docker build -t test:pandas .
	```
	we basically ask docker to build and image with the tag test:pandas in the current repository (the dot at the end), using the existing Dockerfile.
	
4. Once you've built the image, you can run the container :
	```
	docker run -it test:pandas
	```
	This will launch a new bash terminal with python3.9 and pandas installed, and you're all set.

5. Now we can change our Dockerfile slightly :
	```
	FROM python3:.9

	RUN pip install pandas 

	WORKDIR /app # new line added #1

	COPY pipeline.py pipeline.py # this will copy our local pipeline file to container.

	ENTRYPOINT ["python", "pipeline.py"] # this new version tells docker to execute the pipeline python file.

	```

6. Create a pipeline.py python file (you can copy the one in 2_docker_sql/basic folder) ;

7. execute steps 3 and 4 again to see the result.

That's it for the basics.

#### sql
##### Installing postgres in Docker

in order to postgres with docker, run the following command :
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5431:5432 \
postgres:14.3 
```
When this code is executed, it launches a container with a running postgres database, waiting for a connection. Since I already have a postgres db running on my local machine, I'll use the port 5431 and forward it to the 5432 port that my local machine is listening to.
In order to connect, to newly create db  (you should be prompted to type your password -- root in our case):
```
pgcli -h localhost -p 5431 -U root -d ny_taxi
```
when connected, you should see this :
```
Server: PostgreSQL 14.3 (Debian 14.3-1.pgdg110+1)
Version: 3.5.0
Home: http://pgcli.com
root@localhost:ny_taxi>
```
pgcli is client that allos to connect to a pg database, with a prettier interface than the native client (pgsql).

###### Ingestion script
We will build a script that will download a CSV file from the internet and load it into our postgres db running into docker.
1. create the ingestion file :
```
touch upload-data.py
```
this file wil contain the script for downloading CSV file about the NYC yellow trip data and  and inserting it into postgres. Look into the file in the repo.
Some tips : 
to dowload the yellow taxi data we will use : 
```
get https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```
Once downloaded, we cannot load it immediately into panda because the file is too big. So in order to analyze it, we will create a small chunk that we will use to study the data : 
```
gzip -d yellow_tripdata_2021-01.csv.gz # this will unzip the file
head -n 100 yellow_tripdata_2021-01.csv > yellow_head_100.csv # This will copy the first 100 lines into a new file called yeallow_head_100.csv
```

We can now proceed to the analysis of our data.