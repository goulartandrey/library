variable "aws_region" {
  description = "aws region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "ec2 type"
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "ssh key"
  type        = string
}

variable "bucket_name" {
  description = "static_library"
  type        = string
}

variable "project_name" {
  description = "Library v2"
  type        = string
  default     = "library-api"
}
