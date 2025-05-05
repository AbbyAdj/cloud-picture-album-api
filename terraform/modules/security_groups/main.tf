# export TF_VAR_my_ip_address=$(curl -s https://api.ipify.org)/32

# EC2 SECURITY GROUP

resource "aws_security_group" "ec2_security_group" {
    name = "ec2_security_group"
    description = "ec2 security group"
    vpc_id = var.vpc_id 
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
    security_group_id = aws_security_group.ec2_security_group.id
    cidr_ipv4 = var.my_ip_address
    from_port = 22
    to_port = 22
    ip_protocol = "tcp"
}

resource "aws_vpc_security_group_ingress_rule" "http" {
    security_group_id = aws_security_group.ec2_security_group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 80
    to_port = 80
    ip_protocol = "tcp"
}

resource "aws_vpc_security_group_egress_rule" "internet" {
    security_group_id = aws_security_group.ec2_security_group.id
    cidr_ipv4 = "0.0.0.0/0"
    ip_protocol = "-1"
}

# RDS SECURITY GROUP

resource "aws_security_group" "rds_security_group" {
    name = "rds_security_group"
    description = "allow rds access from ec2 only"
    vpc_id = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "rds_from_ec2" {
    security_group_id = aws_security_group.rds_security_group.id
    referenced_security_group_id = aws_security_group.ec2_security_group.id
    from_port = 5432
    to_port = 5432
    ip_protocol = "tcp"
}

# not exactly needed
resource "aws_vpc_security_group_egress_rule" "rds_outbound" {
    security_group_id = aws_security_group.rds_security_group.id
    cidr_ipv4 = "0.0.0.0/0"
    ip_protocol = "tcp"
}