# CI/CD to Kubernetes using Jenkins
This repo contains codebase for test deploy to Kubernetes service.
In this case we use AWS EKS, but we can use any Kubernetes realisation.

## Preinstalled environment:
- Kubernetes
- Jenkins with Kubenetes credetials, installed git and docker services
- PostgreSQL database with deployed SQL-dump (api_db.sql)
- builded docker image with flask components (from Dockerfile_api)


## Kubernetes development

For test deployment we can use eksctl tool, for example:
```bash
eksctl create cluster --name api-app --nodes 2 --node-type=t2.micro --region us-east-1 --zones=us-east-1a,us-east-1b
```

## Common pipeline
- Developer push changes to the github repo.
- Webhook starts Jenkins pipeline job
- Jenkins builds new docker-image and runs some tests
- Jenkins deploy new docker-image to Kubernetes service.
- Run some tests


## Files description
- api_service.py - main python service
- db_settings.ini - settings file with database credentials (should be stored in private repo)
- Jenkinsfile.groovy - Jenkins pipeline (declarative Jenkins pipeline language)
- Dockerfile_flask - main Dockerfile to create docker image with all software,  what we need for application
- Dockerfile_api - Dockerfile for our application
