pipeline {
    agent any

    environment {
        // Snowflake credentials
        SNOWFLAKE_ACCOUNT = "mg05545.eu-west-1"
        SNOWFLAKE_USER = "MRAJAMANI"
        SNOWFLAKE_STAGE = "@prod_notebook_stage"
    }

    stages {
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
                    def ipynbFiles = bat(script: 'dir /B notebooks\\*.ipynb', returnStdout: true).trim().split("\r\n")
                    for (file in ipynbFiles) {
                        bat "python utils\\convert_ipynb_to_sql.py notebooks\\${file} notebooks\\${file.replace('.ipynb', '.sql')}"
                    }
                }
            }
        }

        stage('Deploy to Snowflake') {
            steps {
                echo 'Uploading SQL files to Snowflake stage...'
                script {
                    def sqlFiles = bat(script: 'dir /B notebooks\\*.sql', returnStdout: true).trim().split("\r\n")
                    for (file in sqlFiles) {
                        bat """
                        snowsql -a %SNOWFLAKE_ACCOUNT% -u %SNOWFLAKE_USER% -q ^
                        "USE DATABASE POC_CICD_PROD; USE SCHEMA SH_PROD; PUT file://${WORKSPACE}\\notebooks\\${file} %SNOWFLAKE_STAGE% AUTO_COMPRESS = TRUE;"
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
