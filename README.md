# CloudOps Status Dashboard

A production-style cloud monitoring application deployed on AWS using containerized infrastructure, Infrastructure as Code, and automated CI/CD.

The application continuously checks external services, displays their operational status and response times, and runs as a highly available containerized workload on AWS ECS Fargate.

## Architecture

GitHub
↓
GitHub Actions CI/CD
↓
Docker Build
↓
Amazon ECR
↓
Amazon ECS Fargate
↓
Application Load Balancer
↓
CloudOps Status Dashboard

Infrastructure is provisioned and managed using Terraform.

## Features

- Real-time service health monitoring
- HTTP response-time tracking
- Containerized Python application
- Multi-task deployment using AWS ECS Fargate
- Application Load Balancer for traffic distribution
- Automated health checks
- Centralized logging with Amazon CloudWatch
- Infrastructure as Code using Terraform
- Automated CI/CD with GitHub Actions
- GitHub-to-AWS authentication using OIDC
- Versioned Docker images and ECS task definition revisions
- Automated deployments after changes are pushed to the main branch

## AWS Architecture

The application runs across the following AWS services:

- **Amazon ECS Fargate** — Runs the application without managing EC2 instances
- **Amazon ECR** — Stores versioned Docker container images
- **Application Load Balancer** — Routes incoming traffic to healthy ECS tasks
- **Amazon CloudWatch** — Collects application and container logs
- **AWS IAM** — Provides least-privilege permissions for application deployment
- **GitHub OIDC** — Allows GitHub Actions to authenticate to AWS without storing long-lived AWS credentials

Two ECS tasks run behind the Application Load Balancer to provide redundancy and demonstrate a highly available container architecture.

## Infrastructure as Code

The AWS infrastructure is defined using Terraform.

Terraform provisions and manages resources including:

- ECS cluster
- ECS service
- ECS task definition
- ECR repository
- Application Load Balancer
- Target group
- Networking and security groups
- IAM roles and policies
- CloudWatch logging
- GitHub Actions deployment permissions

This allows the environment to be recreated consistently rather than relying on manual AWS Console configuration.

## CI/CD Pipeline

Deployment is automated using GitHub Actions.

When code is pushed to the `main` branch, the pipeline:

1. Authenticates to AWS using GitHub OIDC
2. Builds the Docker image
3. Tags the image with a version associated with the commit
4. Pushes the image to Amazon ECR
5. Creates a new ECS task definition revision
6. Updates the ECS service
7. Deploys the new application version to the running Fargate environment

This provides a repeatable deployment workflow without manually rebuilding or deploying containers.

## Application Monitoring

The dashboard performs health checks against external services and reports:

- Operational status
- Response time
- Number of healthy services
- Last health-check timestamp

The current example configuration monitors services including Google, GitHub, and Amazon.

## Technology Stack

**Application**
- Python
- HTML/CSS
- HTTP health checks

**Containerization**
- Docker

**AWS**
- ECS
- Fargate
- ECR
- Application Load Balancer
- CloudWatch
- IAM

**Infrastructure**
- Terraform

**CI/CD**
- GitHub Actions
- GitHub OIDC

## Project Structure

```text
cloudops-status-dashboard/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── terraform/
│   └── main.tf
├── Dockerfile
├── health_check.py
├── main.py
├── requirements.txt
└── README.md
```
## Author

John Miller

AWS Certified Cloud Practitioner  
B.S. Computer Information Systems