output "github_token" {
    value = jsondecode(data.aws_secretsmanager_secret_version.github_token.secret_string)["github_token_new"]
}   

output "db_username" {
    value = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)["db_username"]
}

output "db_password" {
    value = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)["db_password"]
}