provider "aws" {
  region = "eu-west-2"

  default_tags {
    tags = {
      Project = "totesys-project"
      Team    = "de-watershed"
    }
  }
}


terraform {
  backend "s3" {
    bucket = "de-watershed-terraform-config"
    key    = "tfstate.tfstate"
    region = "eu-west-2"
  }
}

