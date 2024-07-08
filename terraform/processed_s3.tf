resource "aws_s3_bucket" "processed_bucket" {
    bucket = "${var.team_prefix}processed-bucket"
}