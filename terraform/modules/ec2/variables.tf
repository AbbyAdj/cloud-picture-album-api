variable "instance_type" {
    type = string
    default = "t2.micro"
}

variable "key_name" {
    type = string
    # for deployment, switch to a different key name
    default = "NewServer"
}

variable "user_data_replace_on_change" {
    type = bool
    default = true
}

variable "iam_instance_profile" {
    type = string
}

variable "ec2_security_groups" {
    type = list(string)
}

variable "subnet_id" {
    type = string
}

variable "github_token" {
    type = string
}

variable "db_port" {
    type = number
    default = 5432
}

variable "db_username" {
    type = string
}

variable "db_password" {
    type = string
}

variable "db_endpoint" {
    type = string
}

variable "db_database" {
    type = string
}

variable "s3_user_storage_bucket" {
    type = string
}
