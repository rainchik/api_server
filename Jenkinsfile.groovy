#!groovy
import hudson.model.*
pipeline {
  options {
      timeout(time: 60, unit: 'MINUTES')
  }

  parameters {
      string (name: 'git_branch',defaultValue: 'master',  description: 'Git branch to build')
      string {name: 'docker_repo',defaultValue: 'rainchik/api',  description: 'Git commit to build'}

  }

  agent { node { label 'master' } }

  stages {

    stage('Prepare: Git clone and setup') {
      steps {
        script {
          git branch: git_branch, url: 'https://github.com/rainchik/api_server.git'
          env.commit_hash = sh ( script: 'git rev-parse --short HEAD', returnStdout: true).trim()
          sh "kubectl cluster-info"
        }
      }
    }

    stage('Build: Build and local tests') {
      steps {
        script{
          echo "Building Docker image"
          sh "docker build -t ${docker_repo}:${commit_hash} -f Dockerfile_api ./"

          echo "Running tests"
          echo "Stopping and remove old container"
          sh "docker stop api_server 2>/dev/null && docker rm api_server 2>/dev/null"
          echo "Starting container"
          sh "docker run -d --name api_server -p 127.0.0.1:80:5000 ${docker_repo}:${commit_hash}"
          sh '''
            status=`curl  -I 127.0.0.1:80/hello/Jon 2>/dev/null | head -1 | awk '{print $2}'`
            if [ $status = "200" ];
            then echo "200 is ok";
            else
            echo "something goes wrong";
            exit 1
            fi
            '''
        }

      }
    }

    stage('Deploy: push docker image') {
      steps {
        script{
          echo "Push Docker image to repo"
          sh "docker push ${docker_repo}:${commit_hash}"
        }
      }
    }


    stage('Deploy: run/update service') {
      steps {
        script{
          sh '''
          aws_hostname=`kubectl get services/api-app -o json 2>/dev/null | jq -r '.status|.loadBalancer|.ingress|.[]|.hostname'`
          if [ -z "$aws_hostname" ]
          then
              kubectl apply -f kubernetes/deployment.yaml
              kubectl apply -f kubernetes/service.yaml
          else
              kubectl set image deployment/api-app api-app=${docker_repo}:${commit_hash}
          fi
          '''
          env.aws_hostname = sh ( script: "kubectl get services/api-app -o json 2>/dev/null | jq -r '.status|.loadBalancer|.ingress|.[]|.hostname'", returnStdout: true).trim()

        }
      }
    }

    stage('Test: Testing AWS service') {
      steps {
        script {
          sh '''
            status=`curl  -I ${aws_hostname}:80/hello/Jon 2>/dev/null | head -1 | awk '{print $2}'`
            if [ $status = "200" ];
            then echo "200 is ok";
            else
            echo "something goes wrong";
            exit 1
            fi
            '''
        }
      }
    }
  }
}
