module "syntactical_analysis_repository" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "chesscog"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [
    data.aws_caller_identity.current.arn,
  ]

  repository_lifecycle_policy = local.repository_lifecycle_policy
}

locals {
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep 1 images",
        selection = {
          tagStatus   = "any",
          countType   = "imageCountMoreThan",
          countNumber = 1
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}
