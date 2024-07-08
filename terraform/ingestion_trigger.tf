resource "aws_cloudwatch_event_rule" "ingestion_scheduler" {
  name                = "ingestion-five-minute-scheduler"
  schedule_expression = "rate(5 minutes)"
}


resource "aws_cloudwatch_event_target" "invoke_ingestion_lambda" {
  rule = aws_cloudwatch_event_rule.ingestion_scheduler.name
  arn  = aws_lambda_function.ingestion_lambda.arn
}
