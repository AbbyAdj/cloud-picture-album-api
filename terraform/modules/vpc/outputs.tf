output "cloud_api_vpc_id" {
    value = aws_vpc.cloud_api_vpc.id
}

output "cloud_api_vpc_public_subnet" {
    value = aws_subnet.cloud_api_vpc_public_subnets[*].id
}

output "cloud_api_vpc_private_subnet" {
    value = aws_subnet.cloud_api_vpc_private_subnets[*].id
}


