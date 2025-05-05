# CHANGE ENVIRONMENT TO PROD AFTER PROJECT COMPLETION

# export TF_VAR_my_ip_address=$(curl -s https://api.ipify.org)/32


# Backend

terraform {
  backend "s3" {
    bucket = "abbys-tf-store-bucket"
    key = "terraform/terraform.tfstate"
    region = "eu-west-2"
  }
}

# Provider

provider "aws" {
    region = "eu-west-2"
    default_tags {
        tags = {
          Environment = var.environment
          Project = "Cloud Album API Project"
          Management = "Terraform Managed"
          Repo = "https://github.com/AbbyAdj/cloud-picture-album-api"
        }
    }
}

module "ec2_instance" {
    source = "./modules/ec2"
    iam_instance_profile = module.iam_roles.iam_ec2_instance_profile

    ec2_security_groups = [
        module.security_group.ec2_security_group, 
        ]
}

module "iam_roles" {
    source = "./modules/iam"
}

module "rds_instance" {
    source = "./modules/rds"
    db_username = module.secrets.db_username
    db_password = module.secrets.db_password

    rds_security_groups = [
        module.security_group.rds_security_group
    ]
}

module "s3_buckets" {
    source = "./modules/s3"
}

module "secrets" {
    source = "./modules/secrets-manager"
    github_arn = "arn:aws:secretsmanager:eu-west-2:924932512997:secret:github_token_new-dH4FVb"
    db_credentials_arn = "arn:aws:secretsmanager:eu-west-2:924932512997:secret:merch_api_db_credentials-wacLpr"
}

module "security_group" {
    source = "./modules/security_groups"
    vpc_id = module.vpc.cloud_api_vpc_id
    my_ip_address = var.my_ip_address
}

module "vpc" {
    source = "./modules/vpc"
}
