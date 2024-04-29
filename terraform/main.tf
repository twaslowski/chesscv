terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "chesscv-tfstate"
    key    = "terraform.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"

  default_tags {
    tags = {
      project = "chesscv"
    }
  }
}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "dataset" {
  bucket = "chesscv-dataset"
}
