
# CREATE VPC

resource "aws_vpc" "cloud_api_vpc" {
    cidr_block = "10.0.0.0/16"
}

# CREATE PUBLIC SUBNETS

resource "aws_subnet" "cloud_api_vpc_public_subnets" {
    vpc_id = aws_vpc.cloud_api_vpc.id
    count = length(var.public_subnet_cidrs)
    cidr_block = element(var.public_subnet_cidrs, count.index)
    availability_zone = element(var.availability_zones, count.index)

    tags = {
      Name  = "Public Subnet ${count.index  + 1}"
    }
}

# CREATE PRIVATE SUBNETS

resource "aws_subnet" "cloud_api_vpc_private_subnets" {
    vpc_id = aws_vpc.cloud_api_vpc.id
    count = length(var.private_subnet_cidrs)
    cidr_block = element(var.private_subnet_cidrs, count.index)
    availability_zone = element(var.availability_zones, count.index)

    tags = {
      Name = "Private Subnet ${count.index + 1}"
    }
}

# CREATE INTERNET GATEWAY

resource "aws_internet_gateway" "cloud_api_vpc_internet_gateway" {
    vpc_id = aws_vpc.cloud_api_vpc.id
}

# CREATE ROUTE TABLE

resource "aws_route_table" "cloud_api_vpc_route_table" {
    vpc_id = aws_vpc.cloud_api_vpc.id

    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.cloud_api_vpc_internet_gateway.id
    }
}

# CREATE ROUTE TABLE ASSOCIATION

resource "aws_route_table_association" "cloud_api_public_subnet_association" {
    count = length(aws_subnet.cloud_api_vpc_public_subnets)
    subnet_id = aws_subnet.cloud_api_vpc_public_subnets[count.index].id
    route_table_id = aws_route_table.cloud_api_vpc_route_table.id
}  
