pipeline {
    agent any
    environment {
        SNOWFLAKE_ACCOUNT = 'mg05545.eu-west-1'
        SNOWFLAKE_USER = credentials('SNOWFLAKE_USER')  // Jenkins credential for Snowflake username
        SNOWFLAKE_PASSWORD = credentials('SNOWFLAKE_PASSWORD')  // Jenkins credential for Snowflake password
        SNOWFLAKE_ROLE = 'ACCOUNTADMIN'
        SNOWFLAKE_WAREHOUSE = 'POC_ITIM_PERIASAMY'
        SNOWSQL_CONFIG_FILE = 'C:\\mala1\\<YourUsername>\\.snowsql\\config'
        
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
                bat '"C:\\Program Files\\Python313\\python.exe" utils\\convert_ipynb_to_sql.py'
            }
        }
        stage('Debug Environment') {
    steps {
        bat '''
        dir notebooks\\
        echo SNOWSQL_CONFIG_FILE=%SNOWSQL_CONFIG_FILE%
        echo PATH=%PATH%
        '''
    }
}

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/your-repo.git'
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
