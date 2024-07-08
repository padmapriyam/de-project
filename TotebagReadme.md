# Northcoders Data Engineering Project

We are the Watershed Team, welcome to our Data Engineering Project! We will be demonstrating our skills and understanding of Python, AWS, Terraform, and data engineering in general. Our aim is to create a data-pipeline for managing sales and inventory data of a tote bag company.

# Objective

The objective of this project is to develop an application to Extract, Transform, and Load (ETL) data from the company's operational database into a data lake and data warehouse hosted on AWS. The application should be reliable, secure, and deployed using code automation.

# Components

**S3 Buckets**: Two S3 buckets to store ingested and processed data.
**Lambda Functions**: AWS Lambda functions for data ingestion, processing, and loading tasks.
**CloudWatch**: CloudWatch for logging and monitoring the Lambda functions.
**SSM Parameter Store**: The SSM Parameter Store for storing the timestamp of the last successful data ingestion.
**Terraform**: Terraform for deploying the project resources and implementing Infrastructure-as-Code (IaC)

# Minimum Viable Product

Must:

- Ingest data from the database into the S3 ingestion bucket.
- Transform and process data into a predefined schema stored in the S3 processing bucket.
- Load processed data into the data warehouse.
- Monitore and log all events using CloudWatch.
- Automate deployment using Terraform and Github actions.

# Project Structure:

1. .github/workflows/:
   Contains GitHub Actions workflow files for CI/CD processes.
   Key file:
   - deploy.yml: GitHub Actions workflow for deployment.
2. src/:
   Root directory for the project's source code.  
   Subdirectories:
   - Ingestion_lambda/: Lambda functions for data ingestion.
   - utils/: Utility modules for common functions.
   - packages/python/: Python packages and modules.
3. src/ingestion_lambda/:
   Contains Lambda functions related to data ingestion.
   Key files:
   - lambda_handler.py: Main Lambda handler functions.
   - custom_exceptions.py: Custom exception classes.
   - get_db_creds.py: Module for retrieving database credentials.
   - write_object_to_s3_bucket.py: Module for writing objects to S3 bucket.
4. src/utils/:
   Houses utility modules used across the project.
   Key files:
   - connect.py: Module for database connection.
   - convert_results_to_json_lines.py: Module for converting results to JSON lines format.
   - ssm.py: Module for AWS Systems Manager parameter management.
   - get_table.py: Module for retrieving tables from databases.
5. terraform/:
   Contains Terraform configuration files for deploying infrastructure on AWS.
   Key files:
   - main.tf: Main Terraform configuration file.
   - data.tf, ingestioniam.tf, ingestionlambda.tf, etc.: Additional Terraform configuration file for specific resources.
6. test/:
   Directory for unit tests and integration tests.
   Key files:
   - test_custom_exceptions.py: Unit tests for custom exception classes.
   - test_get_db_creds.py: Unit tests for database credentials module.
7. .gitignore:
   Specifies which files and directories to ignore in version control.
8. python-version:
   File specifying the Python version used in the project.
9. Makefile:
   Includes common tasks and commands for automation.
   Key commands:
   - make setup: Sets up the project environment.
   - make test: Runs unit tests.
   - make deploy: Deploys the project to AWS using Terraform.

# Setup

1. Clone this repository to your local machine:
   https://github.com/yourusername/de-project-watershed.git
2. Install Python, install dependencies and run unittests via Make commands (Make all)
3. Configure AWS's iam credentials using the AWS CLI: aws configure.
4. Deploy infrastructure by going into terraform directory and running the commands init, plan and apply commands.
