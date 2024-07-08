resource "aws_s3_bucket_notification" "processed_lambda_trigger" {
  bucket = "${var.team_prefix}ingestion-bucket"

  lambda_function {
    lambda_function_arn = aws_lambda_function.processed_lambda.arn
    events = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_ingestion_s3_to_call_lambda]

}


resource "aws_lambda_permission" "allow_ingestion_s3_to_call_lambda" {
    statement_id = "AllowS3Invoke"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.processed_lambda.function_name
    principal = "s3.amazonaws.com"
    source_arn = aws_s3_bucket.ingestion_bucket.arn
}