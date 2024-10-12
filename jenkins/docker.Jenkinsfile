#!groovy
@Library('jenkins-libraries') _

pipeline {
    agent {
        node { label 'jenkinsworker00' }
    }

    environment {
        PROJECT_NAME = 'federation-registry'

        DOCKER_HUB_CREDENTIALS_NAME = 'docker-hub-credentials'
        DOCKER_HUB_CREDENTIALS = credentials("${DOCKER_HUB_CREDENTIALS_NAME}")
        DOCKER_HUB_ORGANIZATION = 'indigopaas'
        DOCKER_HUB_URL = 'https://index.docker.io/v1/'

        HARBOR_CREDENTIALS_NAME = 'harbor-paas-credentials'
        HARBOR_CREDENTIALS = credentials("${HARBOR_CREDENTIALS_NAME}")
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
                        script {
                            dockerRepository.pushImage(
                                "${PROJECT_NAME}",
                                "${HARBOR_ORGANIZATION}/${PROJECT_NAME}",
                                "${HARBOR_URL}",
                                "${HARBOR_CREDENTIALS_NAME}",
                            )
                            dockerRepository.updateReadMe(
                                'harbor2',
                                "${HARBOR_ORGANIZATION}/${PROJECT_NAME}",
                                '${HARBOR_CREDENTIALS_USR}',
                                '${HARBOR_CREDENTIALS_PSW}',
                                'harbor.cloud.infn.it',
                            )
                        }
                    }
                }
                stage('Harbor - k8s version') {
                    steps {
                        script {
                            dockerRepository.pushImage(
                                "${PROJECT_NAME}-k8s",
                                "${HARBOR_ORGANIZATION}/${PROJECT_NAME}-k8s",
                                "${HARBOR_URL}",
                                "${HARBOR_CREDENTIALS_NAME}",
                            )
                            dockerRepository.updateReadMe(
                                'harbor2',
                                "${HARBOR_ORGANIZATION}/${PROJECT_NAME}-k8s",
                                '${HARBOR_CREDENTIALS_USR}',
                                '${HARBOR_CREDENTIALS_PSW}',
                                'harbor.cloud.infn.it',
                            )
                        }
                    }
                }
                stage('DockerHub - single instance version') {
                    steps {
                        script {
                            dockerRepository.pushImage(
                                "${PROJECT_NAME}",
                                "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}",
                                "${DOCKER_HUB_URL}",
                                "${DOCKER_HUB_CREDENTIALS_NAME}",
                            )
                            dockerRepository.updateReadMe(
                                'dockerhub',
                                "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}",
                                '${DOCKER_HUB_CREDENTIALS_USR}',
                                '${DOCKER_HUB_CREDENTIALS_PSW}',
                                'docker.io',
                            )
                        }
                    }
                }
                stage('DockerHub - k8s version') {
                    steps {
                        script {
                            dockerRepository.pushImage(
                                "${PROJECT_NAME}-k8s",
                                "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}-k8s",
                                "${DOCKER_HUB_URL}",
                                "${DOCKER_HUB_CREDENTIALS_NAME}",
                            )
                            dockerRepository.updateReadMe(
                                'dockerhub',
                                "${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}-k8s",
                                '${DOCKER_HUB_CREDENTIALS_USR}',
                                '${DOCKER_HUB_CREDENTIALS_PSW}',
                                'docker.io',
                            )
                        }
                    }
                }
            }
        }
    }
}
