
# Glynac Auth Service — CI/CD

CI/CD configuration and deployment infrastructure for the Glynac Authentication Service.

## Project Objectives

- Automate continuous integration and deployment.
- Separate development, staging, and production environments.
- Deploy workloads to HashiCorp Nomad.
- Manage application secrets using HashiCorp Vault.
- Use Docker Hub for container image distribution.
- Maintain separate databases for each environment.
- Protect staging and production deployments with approval requirements.

## Environments

| Environment | Nomad Namespace | Vault Secret Prefix |
|---|---|---|
| Development | ai-service-dev | secret/ai-service/dev |
| Staging | ai-service-staging | secret/ai-service/staging |
| Production | ai-service-prod | secret/ai-service/prod |

## Backend Service Namespaces

| Environment | Nomad Namespace |
|---|---|
| Development | be-service-dev |
| Staging | be-service-staging |
| Production | be-service-prod |

## Infrastructure

- GitHub Actions — CI/CD automation
- Docker — application containerization
- Docker Hub — container image registry
- HashiCorp Nomad — workload scheduling
- HashiCorp Vault — secrets management
- Database — isolated Auth Service databases per environment

## Deployment Workflow

1. Validate and test application changes.
2. Build the Docker image.
3. Publish the image to Docker Hub.
4. Select the target GitHub Environment.
5. Retrieve environment-specific configuration and credentials.
6. Deploy to the corresponding Nomad namespace.
7. Verify deployment health.

## Security

- Keep credentials out of source code.
- Use GitHub Environment secrets for deployment tokens.
- Require approval before staging and production deployments.
- Restrict Nomad and Vault permissions according to environment.
- Do not store production credentials in this repository.

## Status

Initial repository setup.

Deployment configuration, application details, database configuration, and infrastructure endpoints will be documented as they are verified.