variable "project_id" {
  description = "alert-palace-425411-d9"
  type        = string
}

variable "region" {
  description = "europe-west1"
  type        = string
}

variable "zone" {
  description = "europe-west1-b"
  type        = string
}

variable "cloud_sql_instance_name" {
  description = "grasp_api"
  type        = string
}

variable "db_name" {
  description = "grasp_api"
  type        = string
}

variable "db_user" {
  description = "postgres"
  type        = string
}

variable "db_pass" {
  description = "qwerty123"
  type        = string
  sensitive   = true
}

variable "home_ip" {
  description = "46.244.5.202"
  type        = string
}
