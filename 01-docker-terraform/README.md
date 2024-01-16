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

### Official resources.
* [terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) ;
* [GCP](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md).

### Docker and SQL :
