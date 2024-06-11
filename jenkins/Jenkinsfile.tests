def runTests(pythonVersion) {
    // Run in backgound a dockerized neo4j DB instance.
    // Install dependencies for the specified python version.
    // Run tests.
    script {
        docker.image("neo4j:5.18").withRun("-e NEO4J_AUTH=none -e NEO4J_PLUGINS=apoc") { c ->
            docker.image("neo4j:5.18").inside("--link ${c.id}:db") {
                sh "while ! wget http://db:7474; do sleep 1; done"
            }
            docker.image("ghcr.io/withlogicco/poetry:1.8.3-python-$pythonVersion-slim").inside("-e POETRY_VIRTUALENVS_IN_PROJECT=true -e NEO4J_TEST_URL=bolt://neo4j:password@db:7687 -u root:root --link ${c.id}:db") {
                sh "poetry install"
                configFileProvider([configFile(fileId: ".coveragerc-$pythonVersion", variable: "COVERAGERC")]) {
                    sh "poetry run pytest --resetdb --cov --cov-config=$COVERAGERC --cov-report=xml --cov-report=html"
                }
            }
        }
    }
}

pipeline {
    agent { label "jenkinsworker00" }
    stages {
        stage("Run tests") {
            parallel {
                stage("Python 3.10") {
                    steps {
                        runTests("3.10")   
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: "htmlcov-3.10/**/*, coverage-3.10.xml", fingerprint: true
                        }
                    }
                }
                stage("Python 3.11") {
                    steps {
                        runTests("3.11")   
                    }
                    post {
                        always {
                            archiveArtifacts artifacts: "htmlcov-3.11/**/*, coverage-3.11.xml", fingerprint: true
                        }
                    }
                }
            }
        }
    }
}
