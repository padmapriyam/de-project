data "archive_file" "lambda_layer_zip" {
  type        = "zip"
  output_path = "${path.module}/../zip/layer.zip"
  source_dir  = "${path.module}/../src/packages/"
}

resource "aws_lambda_layer_version" "lambda_layer" {
  filename            = "${path.module}/../zip/layer.zip"
  layer_name          = "pg8000_layer"
  source_code_hash    = data.archive_file.lambda_layer_zip.output_base64sha256
  compatible_runtimes = ["python3.11"]
}
