resource "aws_lambda_function" "processed_lambda" {
  function_name    = "${var.team_prefix}processed-lambda"
  filename         = data.archive_file.lambda_processed_source.output_path
  source_code_hash = data.archive_file.lambda_processed_source.output_base64sha256
  role             = aws_iam_role.processed_lambda_role.arn
  handler          = "lambda_handler.lambda_handler"
  layers           = [aws_lambda_layer_version.pandas_lambda_layer.arn, 
                      aws_lambda_layer_version.pyarrow_lambda_layer.arn]
  runtime          = "python3.11"
  timeout          = 60
}

data "archive_file" "lambda_processed_source" {
  type        = "zip"
  output_path = "${path.module}/../zip/processing.zip"
  source_dir  = "${path.module}/../src/processing_lambda/"
}

data "archive_file" "pandas_layer_zip" {
  type        = "zip"
  output_path = "${path.module}/../zip/pandas_layer.zip"
  source_dir  = "${path.module}/../src/pandas_layer/"
}

resource "aws_lambda_layer_version" "pandas_lambda_layer" {
  filename            = "${path.module}/../zip/pandas_layer.zip"
  layer_name          = "pandas_layer"
  source_code_hash    = data.archive_file.pandas_layer_zip.output_base64sha256
  compatible_runtimes = ["python3.11"]
}


data "archive_file" "pyarrow_layer_zip" {
  type        = "zip"
  output_path = "${path.module}/../zip/pyarrow_layer.zip"
  source_dir  = "${path.module}/../src/pyarrow_layer/"
}

resource "aws_lambda_layer_version" "pyarrow_lambda_layer" {
  filename            = "${path.module}/../zip/pyarrow_layer.zip"
  layer_name          = "pyarrow_layer"
  source_code_hash    = data.archive_file.pyarrow_layer_zip.output_base64sha256
  compatible_runtimes = ["python3.11"]
}