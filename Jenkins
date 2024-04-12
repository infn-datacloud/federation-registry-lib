def prepareEnvironment() {
    script {
        sh '''
            pip install poetry
            poetry install --no-interaction --no-root
        '''
    }
}

pipeline {
    stages {
        stage('Test') {
            environment {
                POETRY_VIRTUALENVS_IN_PROJECT = true
            }
            agent {
                docker {
                    image 'python:3.9-slim'
                    reuseNoe 'true'
                }
            }
            steps {
                prepareEnvironment()
            }
        }
    }
}
