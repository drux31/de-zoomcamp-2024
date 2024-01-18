terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }

}

provider "google" {
  credentials = file(var.google_creds)
  project = "drux-de-zoomcamp"
  region  = var.region
  zone    = var.zone
}

resource "google_storage_bucket" "auto-expire" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 10
    }
    action {
      type = "Delete"
    }
  }

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}


resource "google_bigquery_dataset" "terrademo_dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}
