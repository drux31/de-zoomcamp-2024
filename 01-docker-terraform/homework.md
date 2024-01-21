### Homework for week 1

1. --rm
2. 0.42.0
3. 
* query :
```
select count(1) from green_taxi_data where lpep_pickup_datetime >= '2019-09-18 00:00:00' and lpep_dropoff_datetime <= '2019-09-18 23:59:59' ;
```

* result: 15612.
4. 
 * query : 
 ```
 select lpep_pickup_datetime::DATE, sum(trip_distance) from green_taxi_data group by lpep_pickup_datetime::date order by 2 desc limit 1 ;
    
```
    
 * result : 2019-09-26

5. 
```
 select g.lpep_pickup_datetime::date, 
        z."Borough",
        sum(g.total_amount) 
 from green_taxi_data g 
 join zones z on z."LocationID" = g."PULocationID" 
 where g.lpep_pickup_datetime::date = '2019-09-18'
 group by 1, 2
 having sum(g.total_amount) > 50000;
 
 -- Result : 
+----------------------+-------------+----------+
| lpep_pickup_datetime | Borough     | sum      |
|----------------------+-------------+----------|
| 2019-09-18           | "Brooklyn"  | 96333.53 |
| 2019-09-18           | "Manhattan" | 92272.04 |
| 2019-09-18           | "Queens"    | 78672.27 |
+----------------------+-------------+----------+

```

6. 
* query : 
```
 select g."DOLocationID", z."Zone", g.tip_amount
 from green_taxi_data g
 join zones z on z."LocationID" = g."DOLocationID"
 where TO_CHAR(lpep_pickup_datetime, 'YYYY-MM') = '2019-09'
 and TO_CHAR(lpep_dropoff_datetime, 'YYYY-MM') = '2019-09'
 and g."PULocationID" = 7
 order by 3 desc;

-- Result 
+--------------+---------------------------------------+------------+
| DOLocationID | Zone                                  | tip_amount |
|--------------+---------------------------------------+------------|
| 132          | "JFK Airport"                         | 62.31      |
| 260          | "Woodside"                            | 30.0       |
| 137          | "Kips Bay"                            | 28.0       |
| 264          | "NV"                                  | 25.0       |


```


7. terraform :
```
terraform apply
```

Result :
```
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "drux-de-zoomcamp"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.terraform-demo-drux31-bucket will be created
  + resource "google_storage_bucket" "terraform-demo-drux31-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo-drux31-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.terraform-demo-drux31-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 0s [id=projects/drux-de-zoomcamp/datasets/demo_dataset]
google_storage_bucket.terraform-demo-drux31-bucket: Creation complete after 1s [id=terraform-demo-drux31-bucket]
```
