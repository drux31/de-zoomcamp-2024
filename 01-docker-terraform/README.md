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
2. create a terraform file (main.tf) with this [example](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/google-cloud-platform-build) and this [one for the bucket] (https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket)
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


### Official resources.
* [terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) ;
* [GCP](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md).

### Docker and SQL :
