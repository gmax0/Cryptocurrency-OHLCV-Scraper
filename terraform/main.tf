provider "aws" {}

resource "aws_iam_instance_profile" "s3_profile" {
    name = "s3_profile"
    role = "${aws_iam_role.s3_role.name}"
}

resource "aws_s3_bucket" "data_bucket" {
    force_destroy = true
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "s3_policy"
  role = "${aws_iam_role.s3_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}

resource "aws_security_group" "main" {
  egress = [
    {
      cidr_blocks      = [ "0.0.0.0/0", ]
      description      = ""
      from_port        = 0
      ipv6_cidr_blocks = []
      prefix_list_ids  = []
      protocol         = "-1"
      security_groups  = []
      self             = false
      to_port          = 0
    }
  ]
 ingress                = [
   {
     cidr_blocks      = [ "0.0.0.0/0", ]
     description      = ""
     from_port        = 22
     ipv6_cidr_blocks = []
     prefix_list_ids  = []
     protocol         = "tcp"
     security_groups  = []
     self             = false
     to_port          = 22
  }
  ]
}

resource "aws_instance" "my-machine" {
  count = var.ec2_count 

  key_name = var.key_name 
  ami = lookup(var.ec2_ami,var.region) 
  instance_type = var.instance_type
  iam_instance_profile = "${aws_iam_instance_profile.s3_profile.name}"
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.main.id]

  user_data = <<-EOL
  #!/bin/bash

  sudo apt update
  sudo apt install awscli

  echo export DISCORD_WEBHOOK_URL="${var.discord_webhook_url}" | sudo tee -a /etc/profile
  echo export S3_BUCKET_NAME="${aws_s3_bucket.data_bucket.id}" | sudo tee -a /etc/profile
  EOL


  tags = {
    Name = "${count.index}"
  }

  provisioner "file" {
      source = "../coinbasepro/coinbasepro-scraper.py"
      destination = "~/coinbasepro-scraper.py"

      connection {
        type        = "ssh"
        user        = "ubuntu"
        private_key = "${file(var.key_location)}"
        host        = "${self.public_dns}"
      }
  } 

  provisioner "file" {
      source = "../ftx/ftx-scraper.py"
      destination = "~/ftx-scraper.py"

      connection {
        type        = "ssh"
        user        = "ubuntu"
        private_key = "${file(var.key_location)}"
        host        = "${self.public_dns}"
      }
  }

  provisioner "file" {
      source = "../binance/binance-scraper.py"
      destination = "~/binance-scraper.py"

      connection {
        type        = "ssh"
        user        = "ubuntu"
        private_key = "${file(var.key_location)}"
        host        = "${self.public_dns}"
      }
  } 
}