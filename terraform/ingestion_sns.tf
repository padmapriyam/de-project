resource "aws_sns_topic" "sns_error" {
  name = "watershed-sns-notifier"
}

resource "aws_sns_topic_subscription" "sns_error_sub" {
  for_each  = toset(["padmapriya.mariappan@gmail.com", "ahmed.mansurul-karim.de-202404@northcoders.net", "yayuezhou2020@gmail.com", "14doan@gmail.com", "aaron98uk@gmail.com", "khadar7@hotmail.co.uk"])
  topic_arn = aws_sns_topic.sns_error.arn
  protocol  = "email"
  endpoint  = each.value

}