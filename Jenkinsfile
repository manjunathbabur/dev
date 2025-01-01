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
                bat '''
                for %%f in (notebooks\\*.ipynb) do (
                    python utils\\convert_ipynb_to_sql.py %%f notebooks\\%%~nf.sql
                )
                '''
            }
        }

  stage('Deploy to Snowflake') {
            steps {
                withCredentials([string(credentialsId: 'SNOWFLAKE_PASSWORD', variable: 'SNOWFLAKE_PASSWORD')]) {
                    echo 'Uploading SQL files to Snowflake stage...'
                    bat '''
                    for %%f in (notebooks\\*.sql) do (
                        "C:\\Program Files\\SnowSQL\\snowsql.exe" -a %SNOWFLAKE_ACCOUNT% -u %SNOWFLAKE_USER% -p %SNOWFLAKE_PASSWORD% -q ^
                        "USE DATABASE POC_CICD_PROD; USE SCHEMA SH_PROD; PUT file://%WORKSPACE%\\%%f %SNOWFLAKE_STAGE% AUTO_COMPRESS = TRUE;"
                    )
                    '''
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
