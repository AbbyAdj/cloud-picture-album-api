# RETRIEVING GITHUB TOKEN

data "aws_secretsmanager_secret" "github_token_secret" {
    name = var.github_secret_name
}

data "aws_secretsmanager_secret_version" "github_token" {
    secret_id = data.aws_secretsmanager_secret.github_token_secret.id
}

# RETRIEVING DB USERNAME AND PASSWORD

data "aws_secretsmanager_secret" "db_credentials_secret" {
    name = var.db_credentials_secret_name
}

data "aws_secretsmanager_secret_version" "db_credentials" {
    secret_id = data.aws_secretsmanager_secret.db_credentials_secret.id
}
