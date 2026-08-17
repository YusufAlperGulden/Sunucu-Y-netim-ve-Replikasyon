output "aws_apprunner_url" {
  value = aws_apprunner_service.usm_apprunner.service_url
}

output "gcp_cloudrun_url" {
  value = google_cloud_run_v2_service.usm_cloudrun.uri
}

output "global_domain" {
  value = aws_route53_record.primary_aws.name
}
