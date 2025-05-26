# VARS FOR ROOT TF 

variable "environment" {
    type = string
    default = "dev"
}

variable "my_ip_address" {
    type = string
}


variable "github_secret_name" {
    type = string
}

variable "db_credentials_secret_name" {
    type = string
}

variable "s3_user_storage_bucket_name" {
    type = string
}

