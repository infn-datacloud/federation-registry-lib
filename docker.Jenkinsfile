def pushImage(String imageName, String registryUrl, String registryCredentials) {
    // Login to target registry, retrieve docker image and push it to the registry
    sh "docker tag ${PROJECT_NAME} ${imageName}"
    script {
        docker.withRegistry("${registryUrl}", "${registryCredentials}") {
            if ("${BRANCH_NAME}" == 'main') {
                docker.image("${imageName}").push('main')
                docker.image("${imageName}").push('latest')
            }
            docker.image("${imageName}").push("${BRANCH_NAME}")
            docker.image("${imageName}").push("${COMMIT_SHA}")
        }
    }
}

pipeline {
    agent {
        node { label 'jenkinsworker00' }
    }

    environment {
        PROJECT_NAME = 'federation-registry'

        DOCKER_HUB_CREDENTIALS = 'docker-hub-credentials'
        DOCKER_HUB_ORGANIZATION = 'indigopaas'
        DOCKER_HUB_URL = 'https://index.docker.io/v1/'

        HARBOR_CREDENTIALS = 'harbor-paas-credentials'
        HARBOR_ORGANIZATION = 'datacloud-middleware'
        HARBOR_URL = 'https://harbor.cloud.infn.it'

        BRANCH_NAME = "${env.BRANCH_NAME != null ? env.BRANCH_NAME : 'main'}"
        COMMIT_SHA = sh(returnStdout: true, script: 'git rev-parse --short=10 HEAD').trim()
    }

    stages {
        stage('Build docker images') {
            parallel {
                stage('Image for single instance deployment') {
                    steps {
                        script {
                            docker.build("${PROJECT_NAME}", '-f ./dockerfiles/Dockerfile.prod .')
                        }
                    }
                }
                stage('Image for kubernetes deployment') {
                    steps {
                        script {
                            docker.build("${PROJECT_NAME}-k8s", '-f ./dockerfiles/Dockerfile.k8s .')
                        }
                    }
                }
            }
        }

        stage('Push to registries') {
            parallel {
                stage('Harbor - single instance version') {
                    steps {
                        pushImage(
                            "${HARBOR_ORGANIZATION}/${PROJECT_NAME}", "${HARBOR_URL}", "${HARBOR_CREDENTIALS}"
                        )
                    }
                }
                stage('Harbor - k8s version') {
                    steps {
                        pushImage(
                            "${HARBOR_ORGANIZATION}/${PROJECT_NAME}-k8s", "${HARBOR_URL}", "${HARBOR_CREDENTIALS}"
                        )
                    }
                }
                stage('DockerHub - single instance version') {
                    steps {
                        pushImage(
                            "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}",
                            "${DOCKER_HUB_URL}",
                            "${DOCKER_HUB_CREDENTIALS}"
                        )
                    }
                }
                stage('DockerHub - k8s version') {
                    steps {
                        pushImage(
                            "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}-k8s",
                            "${DOCKER_HUB_URL}",
                            "${DOCKER_HUB_CREDENTIALS}"
                        )
                    }
                }
            }
        }

        stage('Remove docker images') {
            steps {
                sh "docker rmi ${PROJECT_NAME}"
                sh "docker rmi ${PROJECT_NAME}-k8s"
            }
        }
    }
}
