variable "ec2_ami" {
  type = map

  default = {
    us-east-1 = "ami-0e472ba40eb589f49"
    us-west-1 = "ami-042b432b930cdde04"
  }
}

variable "region" {
  type = string
  default = "us-east-1"
}

variable "instance_type" {    
  type = string
  default = "t2.small"
}

variable "key_name" {
    type = string
    default = ""
}

variable "key_location" {
    type = string
    default = ""
}

variable "discord_webhook_url" {
    type = string
    default = ""
}

variable "ec2_count" {
    type = number
    default = 1
}