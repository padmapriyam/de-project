resource "aws_cloudwatch_log_metric_filter" "processed_metric_filter" {
  name           = "Error-filter"
  pattern        = "ERROR"
  log_group_name = "/aws/lambda/${aws_lambda_function.processed_lambda.function_name}"

  metric_transformation {
    name      = "EventCount"
    namespace = "Processed-errors"
    value     = "1"
  }
}


resource "aws_cloudwatch_metric_alarm" "processed_metric_" {
  alarm_name          = "processed-error-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  metric_name         = aws_cloudwatch_log_metric_filter.processed_metric_filter.metric_transformation[0].name
  namespace           = aws_cloudwatch_log_metric_filter.processed_metric_filter.metric_transformation[0].namespace
  period              = 30
  statistic           = "Sum"
  threshold           = 0.5
  alarm_actions       = [aws_sns_topic.sns_error.arn]
  alarm_description   = "This metric monitors error messages"
}