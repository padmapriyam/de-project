resource "aws_s3_bucket" "ingestion_bucket" {
  bucket = "${var.team_prefix}ingestion-bucket"
}


