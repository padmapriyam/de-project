# Create role for loading lambda 
resource "aws_iam_role" "loading_lambda_role" {
  name = "${var.team_prefix}loading-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

# Define IAM policy loading lambda to read loading s3
resource "aws_iam_policy" "loading_lambda_read_processed_s3_policy" {
  name        = "${var.team_prefix}loading-lambda-read-processed-s3-policy"
  description = "Policy for lambda to read from loading s3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.processed_bucket.arn}/*"
      },
      {
        Action = [
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = "${aws_s3_bucket.processed_bucket.arn}"
      }
    ]
  })
}

# Define IAM policy attachment to attach read_loading_lambda_s3_policy
resource "aws_iam_role_policy_attachment" "loading_lambda_read_loading_s3_policy_attachment" {
  role       = aws_iam_role.loading_lambda_role.name
  policy_arn = aws_iam_policy.loading_lambda_read_processed_s3_policy.arn
}




# Define IAM policy for processing lambda to write logs
resource "aws_iam_policy" "loading_lambda_logs_policy" {
  name        = "${var.team_prefix}loading-lambda-logs-policy"
  description = "Policy for logging warehouse entries"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
      },
      {
        Action = [
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${aws_lambda_function.loading_lambda.function_name}:*"
      }
    ]
  })
}

# Attach logs policy to processing lambda role
resource "aws_iam_role_policy_attachment" "loading_lambda_logs_attachment" {
  role       = aws_iam_role.loading_lambda_role.name
  policy_arn = aws_iam_policy.loading_lambda_logs_policy.arn
}


resource "aws_iam_policy" "loading_lambda_secrets_policy" {
  name        = "${var.team_prefix}loading-lambda-secrets-policy"
  description = "Policy for lambda to read/write to secrets"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:data_warehouse_credentials*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "loading_secrets_policy_attachment" {
  role       = aws_iam_role.loading_lambda_role.name
  policy_arn = aws_iam_policy.loading_lambda_secrets_policy.arn
}

