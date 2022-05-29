terraform {
  backend "gcs" {
    bucket = "<project_id>"
    prefix = "playground-state/"
  }
}