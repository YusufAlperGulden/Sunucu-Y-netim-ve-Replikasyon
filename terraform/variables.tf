variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "gcp_region" {
  type    = string
  default = "europe-west3"
}

variable "gcp_project_id" {
  type        = string
  description = "Your Google Cloud Project ID"
}

variable "aws_ecr_image_url" {
  type        = string
  description = "ECR URL of your Docker image"
}

variable "gcp_artifact_image_url" {
  type        = string
  description = "Google Artifact Registry URL of your Docker image"
}

variable "domain_name" {
  type        = string
  description = "Your root domain name hosted in Route 53 (e.g. example.com)"
}

variable "subdomain_name" {
  type        = string
  description = "The subdomain to deploy to (e.g. manager.example.com)"
}
