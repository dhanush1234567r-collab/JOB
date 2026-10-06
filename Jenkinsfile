pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/dhanush1234567r-collab/JOB.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker rm -f job-portal-frontend job-portal-backend || true
                docker compose up -d --build
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                sleep 8
                curl -f http://localhost:5001/api/jobs
                '''
            }
        }
    }
}
