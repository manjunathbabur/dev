pipeline {
    agent any

    environment {
        // Snowflake credentials
        SNOWFLAKE_ACCOUNT = "mg05545.eu-west-1"
        SNOWFLAKE_USER = "MRAJAMANI"
        SNOWFLAKE_STAGE = "@prod_notebook_stage"
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Installing Python dependencies...'
                bat 'pip install nbformat'
            }
        }

        stage('Clone Repository') {
            steps {
                echo 'Cloning the Git repository...'
                checkout scm
            }
        }

        stage('Convert Notebooks') {
            steps {
                echo 'Converting .ipynb files to .sql...'
                script {
                    // Get the list of .ipynb files
                    def ipynbFiles = bat(script: 'for %f in (notebooks\\*.ipynb) do echo %f', returnStdout: true).trim().split("\r\n")
                    
                    // Convert each .ipynb to .sql
                    for (file in ipynbFiles) {
                        def cleanFile = file.trim()
                        bat "python utils\\convert_ipynb_to_sql.py ${WORKSPACE}\\${cleanFile} ${WORKSPACE}\\${cleanFile.replace('.ipynb', '.sql')}"
                    }
                }
            }
        }

        stage('Deploy to Snowflake') {
            steps {
                echo 'Uploading SQL files to Snowflake stage...'
                script {
                    // Get the list of .sql files
                    def sqlFiles = bat(script: 'for %f in (notebooks\\*.sql) do echo %f', returnStdout: true).trim().split("\r\n")
                    
                    // Upload each .sql file
                    for (file in sqlFiles) {
                        def cleanFile = file.trim()
                        bat """
                        snowsql -a %SNOWFLAKE_ACCOUNT% -u %SNOWFLAKE_USER% -q ^
                        "USE DATABASE POC_CICD_PROD; USE SCHEMA SH_PROD; PUT file://${WORKSPACE}\\${cleanFile} %SNOWFLAKE_STAGE% AUTO_COMPRESS = TRUE;"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up workspace...'
            cleanWs()
        }
    }
}
