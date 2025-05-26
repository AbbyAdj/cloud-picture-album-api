

resource "aws_s3_bucket" "user-data-storage" {
    bucket = var.s3_user_storage_bucket_name
}