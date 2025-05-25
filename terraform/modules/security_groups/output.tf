output "ec2_security_group" {
    value = aws_security_group.ec2_security_group.id
}

output "rds_security_group" {
    value = aws_security_group.rds_security_group.id
}

output "vpc_id_ec2" {
  value = aws_security_group.ec2_security_group.vpc_id
}

output "vpc_id_rds" {
  value = aws_security_group.rds_security_group.vpc_id
}