# CHANGE ENVIRONMENT TO PROD AFTER PROJECT COMPLETION

# export TF_VAR_my_ip_address=$(curl -s https://api.ipify.org)/32


# Backend

terraform {
  backend "s3" {
    bucket = "cloud-album-api-project-backend"
    key    = "terraform/terraform.tfstate"
    region = "eu-west-2"
  }
}

# Provider

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      Environment = var.environment
      Project     = "Cloud Album API Project"
      Management  = "Terraform Managed"
      Repo        = "https://github.com/AbbyAdj/cloud-picture-album-api"
    }
  }
}


module "vpc" {
  source = "./modules/vpc"
}


module "iam_roles" {
  source         = "./modules/iam"
  rds_identifier = module.rds_instance.rds_postgres_instance_identifier
  rds_username   = module.rds_instance.rds_postgres_instance_username
}

module "security_group" {
  source        = "./modules/security_groups"
  vpc_id        = module.vpc.cloud_api_vpc_id
  my_ip_address = var.my_ip_address
}

module "secrets" {
  source                     = "./modules/secrets-manager"
  github_secret_name         = var.github_secret_name
  db_credentials_secret_name = var.db_credentials_secret_name
}

module "ec2_instance" {
  source               = "./modules/ec2"
  iam_instance_profile = module.iam_roles.iam_ec2_instance_profile
  github_token = module.secrets.github_token
  db_database = module.rds_instance.rds_database_name
  db_username = module.secrets.db_username
  db_password = module.secrets.db_password
  db_endpoint = module.rds_instance.rds_db_endpoint
  subnet_id            = module.vpc.cloud_api_vpc_public_subnet[0]
  ec2_security_groups = [
    module.security_group.ec2_security_group,
  ]
}

module "rds_instance" {
  source           = "./modules/rds"
  db_username      = module.secrets.db_username
  db_password      = module.secrets.db_password
  rds_subnet_group = module.vpc.cloud_api_vpc_private_subnet
  rds_security_groups = [
    module.security_group.rds_security_group,
  ]
}

module "s3_buckets" {
  source = "./modules/s3"
}


