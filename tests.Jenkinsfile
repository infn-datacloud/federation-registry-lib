pipeline {
    agent none
    stages {
        stage('Intall dependencies') {
            agent {
                docker {
                    label 'jenkinsworker00'
                    image 'ghcr.io/withlogicco/poetry:1.8.3-python-3.10-slim'
                    reuseNode true
                }
            }
            steps {
                sh "poetry install"
            }
        }        
    }
}
