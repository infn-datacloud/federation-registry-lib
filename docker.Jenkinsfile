def tagImage(image_name) {
    // Add tags to a docker image
    script {
        if ("${BRANCH_NAME}" == "main") {
            sh("docker tag ${PROJECT_NAME} ${image_name}")
        }
        sh("docker tag ${PROJECT_NAME} ${image_name}:${BRANCH_NAME}")
        sh("docker tag ${PROJECT_NAME} ${image_name}:${COMMIT_SHA}")
    }    
}

def pushImage(image_name, registry_url, registry_credentials) {
    // Login to target registry, retrieve docker image and push it to the registry
    script {
        docker.withRegistry("${registry_url}", "${registry_credentials}") {
            if ("${BRANCH_NAME}" == "main") {           
                docker.image("${image_name}").push()
            }
            docker.image("${image_name}:${BRANCH_NAME}").push()
            docker.image("${image_name}:${COMMIT_SHA}").push()
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
        COMMIT_SHA = sh(returnStdout: true, script: "git rev-parse --short=10 HEAD").trim()
    }

    stages {
        stage('Build docker image') {
            steps {
                script {
                    docker.build("${PROJECT_NAME}", "./dockerfiles/tiangolo.dockerfile")
                    docker.build("${PROJECT_NAME}-k8s", "./dockerfiles/k8s.dockerfile")
                }
            }
        }
        
        stage('Tag and push to registries') {
            parallel {
                stage("Harbor") {
                    stages {
                        stage("Tag") {
                            steps {
                                tagImage("${HARBOR_ORGANIZATION}/${PROJECT_NAME}")
                                tagImage("${HARBOR_ORGANIZATION}/${PROJECT_NAME}-k8s")
                            }
                        }
                        stage('Push') {
                            steps {
                                pushImage("${HARBOR_ORGANIZATION}/${PROJECT_NAME}", "${HARBOR_URL}", "${HARBOR_CREDENTIALS}")
                                pushImage("${HARBOR_ORGANIZATION}/${PROJECT_NAME}-k8s", "${HARBOR_URL}", "${HARBOR_CREDENTIALS}")
                            }
                        }
                    }
                }
                stage("DockerHub") {
                    stages {
                        stage("Tag") {
                            steps {
                                tagImage("${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}")
                                tagImage("${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}-k8s")
                            }
                        }
                        stage('Push') {
                            steps {
                                pushImage("${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}", "${DOCKER_HUB_URL}", "${DOCKER_HUB_CREDENTIALS}")
                                pushImage("${DOCKER_HUB_ORGANIZATION}/${PROJECT_NAME}-k8s", "${DOCKER_HUB_URL}", "${DOCKER_HUB_CREDENTIALS}")
                            }
                        }
                    }
                }
            }
        }

        stage('Remove docker image') {
            steps{
                script {
                    sh("docker rmi ${PROJECT_NAME}")
                }
            }
        }
        
    }
}
