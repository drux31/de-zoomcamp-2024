variable "google_creds" {
  default     = "[path to the google credentials file]"
  description = "Project google creds"
}

variable "region" {
  default     = "us-central1"
  description = "Project region"
}

variable "zone" {
  default     = "us-central1-c"
  description = "Project zone"
}

variable "location" {
  default     = "US"
  description = "Project location"
}

variable "bq_dataset_name" {
  default     = "terrademo_dataset"
  description = "My BigQuery dataset Name"
}

variable "gcs_bucket_name" {
  default     = "auto-expiring-demo-bucket"
  description = "My GCS bucket name"
}

variable "gcs_storage_class" {
  default     = "STANDARD"
  description = "Bucket Storage Class"
}