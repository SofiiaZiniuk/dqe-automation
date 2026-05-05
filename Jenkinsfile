pipeline {
    agent any

    environment {
        POSTGRES_SECRET = credentials('jenkins-postgres-credentials')
    }

    stages {
        stage('Check Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    venv/bin/python -m pip install --upgrade pip
                    cat requirements.txt
                    venv/bin/python -m pip install -r requirements.txt -v
                    venv/bin/python -m pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                withCredentials([
                usernamePassword(
                credentialsId: 'postgres-creds',
                usernameVariable: 'DB_USER',
                passwordVariable: 'DB_PASSWORD'
            )
        ]) {
            sh '''
                . venv/bin/activate

                export DB_HOST=postgres
                export DB_PORT=5432
                export DB_NAME=mydatabase

                venv/bin/python -m pytest tests -m parquet_data \
                    --html=html_report/report.html
            '''
        }
    }
}

        stage('Archive Test Report') {
            steps {
                archiveArtifacts artifacts: 'html_report/**', allowEmptyArchive: true

                publishHTML(target: [
                    allowMissing: false,
                    keepAll: true,
                    reportDir: 'html_report',
                    reportFiles: 'report.html',
                    reportName: 'HTML Test Report'
                ])
            }
        }
    }
}