variable "db_username" {
    description = "rds db username"
    type = string
    sensitive = true
}

variable "db_password" {
    description = "rds db password"
    type = string
    sensitive = true
}

variable "rds_security_groups" {
    type = list(string)
}
