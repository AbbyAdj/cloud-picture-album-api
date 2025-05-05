# RDS INSTANCE

resource "aws_db_instance" "album_api_db" {
    allocated_storage = 20
    db_name = "albumapidb"
    engine = "postgres"
    engine_version = "14.12"
    instance_class = "db.t4g.micro"
    username = var.db_username
    password = var.db_password
    skip_final_snapshot = false
    vpc_security_group_ids = var.rds_security_groups
}
