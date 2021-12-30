output "instance_ips" {
    value = aws_instance.my-machine.*.public_ip
}