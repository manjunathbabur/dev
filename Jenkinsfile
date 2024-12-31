pipeline {
    agent any
    environment {
        SNOWFLAKE_ACCOUNT = 'mg05545.eu-west-1'
        SNOWFLAKE_USER = credentials('SNOWFLAKE_USER')  // Snowflake username
        SNOWFLAKE_PASSWORD = credentials('SNOWFLAKE_PASSWORD')  // Snowflake password
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/manjunathbabur/dev.git'
            }
        }
        stage('Deploy SQL Files to Snowflake') {
            steps {
                bat '''
                for %%f in (notebooks\\*.sql) do (
                    echo %SNOWFLAKE_PASSWORD% | "C:\\Program Files\\SnowSQL\\snowsql.exe" -a %SNOWFLAKE_ACCOUNT% -u %SNOWFLAKE_USER% -q "PUT file://%%~dpnxf @prod_notebook_stage AUTO_COMPRESS = TRUE;"
                )
                '''
            }
        }
    }
    post {
        success {
            echo 'Deployment Successful: All SQL files uploaded to Snowflake stage!'
        }
        failure {
            echo 'Deployment Failed: Check the logs for details.'
        }
    }
}
