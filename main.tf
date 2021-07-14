terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "eu-central-1"
}

resource "aws_security_group" "sg_allow_ssh" {
  name = "sg_allow_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outgoing traffic to anywhere.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "sg_allow_rest_8080" {
  name = "sg_allow_rest_8080"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outgoing traffic to anywhere.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "sg_allow_http" {
  name = "sg_allow_http"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outgoing traffic to anywhere.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "postgres-data" {
#  id = "vol-05732eeba51435043"
   availability_zone = "eu-central-1a"
   size              = 8
}


resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/xvdf"
  volume_id   = aws_ebs_volume.postgres-data.id
  instance_id = aws_instance.app_server.id
}

resource "aws_instance" "app_server" {
  ami             = "ami-05f7491af5eef733a"
  instance_type   = "t2.micro"
  vpc_security_group_ids = [
      "sg_allow_http",
      "sg_allow_ssh",
      "sg_allow_rest_8080",
  ]
  key_name        = "maslovss" 
  availability_zone = "eu-central-1a"


  connection {
    type = "ssh"
    host = self.public_ip
    user = "ubuntu"
    private_key = file("${path.module}/maslovss.pem")
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get remove docker docker-engine docker.io containerd runc",
      "sudo apt-get update",
      "sudo apt-get  --yes install apt-transport-https ca-certificates curl gnupg lsb-release",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
      "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list /dev/null",
      "sudo apt-get update",
      "sudo apt-get  --yes install docker-ce docker-ce-cli containerd.io docker-compose"
    ]
  }

  provisioner "file" {
    source      = "docker"
    destination = "/home/ubuntu/docker"
  }
  

  tags = {
    Name = "Check goods price development"
  }
}
