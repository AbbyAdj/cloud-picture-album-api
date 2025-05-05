# ROLE

resource "aws_iam_role" "ec2_combined_role" {
    name = "ec2_combined_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Action = "sts:AssumeRole",
                Effect = "Allow",
                Principal = {
                    Service = "ec2.amazonaws.com"
                    }           
            }
        ]
    })
}

# COMBINED POLICY

resource "aws_iam_policy" "ec2_combined_policy" {
  name = "ec2_combined_policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [

      # Secrets Manager permissions
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Resource = "*"
      },

      # S3 permissions
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:ListBuckets",
          "s3:CreateBucket",
          "s3:DeleteBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
        ],
        Resource = [
          "arn:aws:s3:::user_album_*",
          "arn:aws:s3:::user_album_*/*"
        ]
      },

      # RDS IAM auth (optional — only if using IAM DB auth)
      {
        Effect = "Allow",
        Action = [
          "rds-db:connect"
        ],
        Resource = "arn:aws:rds-db:${data.aws_region.curent_region.name}:a${data.aws_caller_identity.my_caller_id.account_id}:dbuser:${module.db_instance.rds_postgres_instance_identifier}/${module.db_instance.rds_postgres_instance_username}"
      }
    ]
  })
}


# ROLE -> POLICY

resource "aws_iam_role_policy_attachment" "ec2_combined_policy_attachment" {
    role = aws_iam_role.ec2_combined_role.name
    policy_arn = aws_iam_policy.ec2_combined_policy.arn
}

# INSTANCE PROFILE

resource "aws_iam_instance_profile" "ec2_combined_profile" {
    name = "ec2_combined_profile"
    role = aws_iam_role.ec2_combined_role.name
}

# DATA NEEDED

data "aws_region" "curent_region" {}

data "aws_caller_identity" "my_caller_id" {}
