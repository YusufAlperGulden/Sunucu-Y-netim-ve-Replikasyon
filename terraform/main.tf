terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# ---------------------------------------------------------
# AWS App Runner Service
# ---------------------------------------------------------
resource "aws_apprunner_service" "usm_apprunner" {
  service_name = "universal-server-manager"

  source_configuration {
    image_repository {
      image_configuration {
        port = "8000"
      }
      image_identifier      = var.aws_ecr_image_url
      image_repository_type = "ECR"
    }
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_access_role.arn
    }
    auto_deployments_enabled = true
  }

  instance_configuration {
    cpu    = "1024"
    memory = "2048"
  }
}

# IAM Role for App Runner to pull from ECR
resource "aws_iam_role" "apprunner_access_role" {
  name = "apprunner-access-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
        Effect = "Allow"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_policy" {
  role       = aws_iam_role.apprunner_access_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# ---------------------------------------------------------
# Google Cloud Run Service
# ---------------------------------------------------------
resource "google_cloud_run_v2_service" "usm_cloudrun" {
  name     = "universal-server-manager"
  location = var.gcp_region

  template {
    containers {
      image = var.gcp_artifact_image_url
      ports {
        container_port = 8000
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "2048Mi"
        }
      }
    }
  }
}

# Make Cloud Run public
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  name     = google_cloud_run_v2_service.usm_cloudrun.name
  location = google_cloud_run_v2_service.usm_cloudrun.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
