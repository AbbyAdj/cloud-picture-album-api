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