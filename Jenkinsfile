def prepareEnvironment() {
    script {
        sh """
            pip install poetry
            poetry install --no-interaction --no-root
        """
    }
}

pipeline {
    environment {
        POETRY_VIRTUALENVS_IN_PROJECT = true
    }
    agent {
        docker {
            label 'jenkinsworker00'
            image 'python:3.9-slim'
            reuseNode 'true'
        }
    }
    stages {
        stage('Test') {
            steps {
                prepareEnvironment()
            }
        }
    }
}
