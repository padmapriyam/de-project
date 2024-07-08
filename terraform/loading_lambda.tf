resource "aws_lambda_function" "loading_lambda" {
  function_name    = "${var.team_prefix}loading-lambda"
  filename         = data.archive_file.lambda_loading_source.output_path
  source_code_hash = data.archive_file.lambda_loading_source.output_base64sha256
  role             = aws_iam_role.loading_lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  layers           = [aws_lambda_layer_version.lambda_layer.arn,
                      aws_lambda_layer_version.pandas_lambda_layer.arn,
                      aws_lambda_layer_version.pyarrow_lambda_layer.arn,
                      aws_lambda_layer_version.sqlalchemy_layer.arn]
  runtime          = "python3.11"
  timeout          = 900
  memory_size      = 1024
}

data "archive_file" "lambda_loading_source" {
  type        = "zip"
  output_path = "${path.module}/../zip/loading.zip"
  source_dir  = "${path.module}/../src/loading_lambda/"
}


data "archive_file" "sqlalchemy_zip" {
  type        = "zip"
  output_path = "${path.module}/../zip/sqlalchemy.zip"
  source_dir  = "${path.module}/../src/sqlalchemy_layer/"
}

resource "aws_lambda_layer_version" "sqlalchemy_layer" {
  filename            = "${path.module}/../zip/sqlalchemy.zip"
  layer_name          = "sqlalchemy_layer"
  source_code_hash    = data.archive_file.sqlalchemy_zip.output_base64sha256
  compatible_runtimes = ["python3.11"]
}

