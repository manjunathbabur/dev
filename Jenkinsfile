pipeline {
    agent any
    environment {
        SNOWFLAKE_ACCOUNT = 'mg05545.eu-west-1.snowflakecomputing.com'
        SNOWFLAKE_USER = credentials('SNOWFLAKE_USER')  // Jenkins credential for Snowflake username
        SNOWFLAKE_PASSWORD = credentials('SNOWFLAKE_PASSWORD')  // Jenkins credential for Snowflake password
        SNOWFLAKE_ROLE = 'ACCOUNTADMIN'
        SNOWFLAKE_WAREHOUSE = 'POC_ITIM_PERIASAMY'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/manjunathbabur/dev.git'
            }
        }
        stage('Convert Notebooks') {
            steps {
                // Convert .ipynb files to .sql
                sh 'python utils/convert_ipynb_to_sql.py'
            }
        }
        stage('Deploy SQL Files to Snowflake') {
            steps {
                // Upload all SQL files to Snowflake stage
                bat '''
                for %f in (notebooks\\*.sql) do (
                    snowsql -a %SNOWFLAKE_ACCOUNT% -u %SNOWFLAKE_USER% -p %SNOWFLAKE_PASSWORD% -r %SNOWFLAKE_ROLE% -w %SNOWFLAKE_WAREHOUSE% -q "PUT file://%cd%\\%f @prod_notebook_stage AUTO_COMPRESS = TRUE;"
                )
                '''
            }
        }
    }
    post {
        success {
            echo 'Deployment Successful: SQL files uploaded to Snowflake stage!'
        }
        failure {
            echo 'Deployment Failed: Check the logs for details.'
        }
    }
}
