variable "project" {
  type    = string
  default = "<project_id>"
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "vpc_cidr_block" {
  type    = string
  default = "10.128.0.0/9"
}

variable "source-ip" {
  type    = string
  default = "<your_ip>"
}

variable "user" {
  type    = string
  default = "<key_username>"
}

variable "public_key_path" {
  type    = string
  default = "<path_to_key>"
}

variable "private_key_path" {
  type    = string
  default = "<path_to_private_key>"
}