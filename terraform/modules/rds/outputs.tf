output "rds_postgres_instance_identifier" {
    value = aws_db_instance.album_api_db.identifier
}

output "rds_postgres_instance_username" {
    value = aws_db_instance.album_api_db.username
}

output "rds_db_endpoint" {
    value = aws_db_instance.album_api_db.endpoint
}

output "rds_database_name" {
    value = aws_db_instance.album_api_db.db_name
}   