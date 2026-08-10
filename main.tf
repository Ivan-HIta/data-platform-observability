terraform {
  required_version = ">= 1.6.0"
}

# Reference only: keep provider credentials and state outside this repository.
variable "project_id" { type = string }
variable "bucket_name" { type = string }

resource "google_storage_bucket" "raw_landing" {
  name          = var.bucket_name
  project       = var.project_id
  location      = "NORTHAMERICA-NORTHEAST1"
  uniform_bucket_level_access = true
  versioning { enabled = true }
}

