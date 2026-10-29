
pipeline {
    agent any

    environment {
        IMAGE = 'prathibha9949/selenium-testing-demo-app:latest'
        CONTAINER_NAME = 'selenium-testing-demo-ci'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE% .'
            }
        }

        stage('Start Container') {
            steps {
                bat '''
                docker rm -f %CONTAINER_NAME% 2>NUL
                docker run -d --name %CONTAINER_NAME% -p 5001:5000 %IMAGE%
                timeout /t 5 /nobreak >NUL
                '''
            }
        }

        stage('Install Test Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'set APP_URL=http://localhost:5001&& python -m pytest -v tests'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )
                ]) {
                    bat '''
                    echo %DOCKERHUB_PASSWORD% | docker login -u %DOCKERHUB_USERNAME% --password-stdin
                    docker push %IMAGE%
                    docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                kubectl rollout restart deployment/selenium-testing-demo-app
                kubectl rollout status deployment/selenium-testing-demo-app --timeout=120s
                '''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f %CONTAINER_NAME% 2>NUL'
        }
    }
}
