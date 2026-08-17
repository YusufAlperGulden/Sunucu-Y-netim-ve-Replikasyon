# ---------------------------------------------------------
# Global Load Balancer (AWS Route 53 with Failover Routing)
# ---------------------------------------------------------

data "aws_route53_zone" "main" {
  name = var.domain_name
}

# Health Check for AWS App Runner
resource "aws_route53_health_check" "aws_primary" {
  fqdn              = aws_apprunner_service.usm_apprunner.service_url
  port              = 443
  type              = "HTTPS"
  resource_path     = "/"
  failure_threshold = "3"
  request_interval  = "10"

  tags = {
    Name = "usm-aws-health-check"
  }
}

# Primary Record pointing to AWS App Runner
resource "aws_route53_record" "primary_aws" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.subdomain_name
  type    = "CNAME"
  ttl     = "60"

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier  = "Primary-AWS"
  records         = [aws_apprunner_service.usm_apprunner.service_url]
  health_check_id = aws_route53_health_check.aws_primary.id
}

# Secondary Record pointing to Google Cloud Run
resource "aws_route53_record" "secondary_gcp" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.subdomain_name
  type    = "CNAME"
  ttl     = "60"

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier = "Secondary-GCP"
  # Clean up "https://" from cloud run URL for CNAME
  records        = [replace(google_cloud_run_v2_service.usm_cloudrun.uri, "https://", "")]
}
