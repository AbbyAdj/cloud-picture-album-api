output "token" {
  value = nonsensitive(module.secrets.github_token)

}

output "rds_db_name_confirm" {
    value = module.rds_instance.rds_database_name
}

output "rds_db_endpoint_confirm" {
    value = module.rds_instance.rds_db_endpoint
}