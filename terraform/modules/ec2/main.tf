# NEED ENV VARIABLES TO EXPORT


# CREATE AMI (ubuntu)

# might consider Amazon linux, but I am sticking to ubuntu for now,
data "aws_ami" "ubuntu_24_04" {
  most_recent = true
  owners      = ["099720109477"]

  # Ubuntu AMI ID search
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# CREATE EC2 INSTANCE

resource "aws_instance" "album_api" {
    ami = data.aws_ami.ubuntu_24_04.id
    instance_type = var.instance_type
    key_name = var.key_name
    iam_instance_profile = var.iam_instance_profile
    user_data = templatefile("../run.sh", {"INSERT ENV VARIABLES TO EXPORT TO .SH"="Hey"})
    user_data_replace_on_change = var.user_data_replace_on_change
    vpc_security_group_ids = var.ec2_security_groups
}