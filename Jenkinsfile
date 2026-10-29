pipeline {
    agent any

    environment {
        APP_IMAGE = 'prathibha9949/registration-app:latest'
        CONTAINER_NAME = 'registration-app-test'
        APP_URL = 'http://127.0.0.1:5000'
        PYTHON = 'C:\\Users\\samap\\AppData\\Local\\Programs\\Python\\Python310\\python.exe'
    }

    stages {

        stage('Install Dependencies') {
            steps {
                bat '''
                    "%PYTHON%" --version
                    "%PYTHON%" -m pip install Flask pytest selenium
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %APP_IMAGE% .'
            }
        }

        stage('Start Application') {
            steps {
                bat '''
                    docker rm -f %CONTAINER_NAME% 2>NUL
                    docker run -d --name %CONTAINER_NAME% -p 5000:5000 %APP_IMAGE%
                '''

                powershell '''
                    $ready = $false
                    for ($i = 0; $i -lt 30; $i++) {
                        try {
                            Invoke-WebRequest -Uri "$env:APP_URL/register" -UseBasicParsing -TimeoutSec 3 | Out-Null
                            $ready = $true
                            break
                        } catch {
                            Start-Sleep -Seconds 2
                        }
                    }

                    if (-not $ready) {
                        docker logs $env:CONTAINER_NAME
                        exit 1
                    }

                    Write-Output "Application is ready"
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v tests/test_registrationapp.py --junitxml=test-results.xml'
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '''
                    docker tag %APP_IMAGE% prathibha9949/registration-app:%BUILD_NUMBER%
                    docker push %APP_IMAGE%
                    docker push prathibha9949/registration-app:%BUILD_NUMBER%
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout status deployment/kubedemoapp --timeout=120s
                '''
            }
        }
    }

    post {
        always {
            bat 'docker rm -f %CONTAINER_NAME% 2>NUL'
            junit testResults: 'test-results.xml',
                  allowEmptyResults: true
        }
    }
}