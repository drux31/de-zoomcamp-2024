This first module is about seting up the environment. It is supposed to last two weeks.
The tools and language we are going to use are the followings :
* docker ;
* sql (using a postgres db since I am workng locally) ;
* Terraform. 

### Terraform & GCP
Terraform installation : all the instruction are available from [the official doc](https://developer.hashicorp.com/terraform/install#Linux). 
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
terraform --version<br>
The output should be something like :
Terraform v1.6.6
on linux_386 
``

4. Delete the zip file:<br>
``
rm terraform_1.6.6_linux_386.zip
``

I already had a GCP account from the previous cohort, so no particular config needed. We're all set for the course.
* [terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) ;
* [GCP](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md).

### Docker and SQL :
