pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "113.205.79.188"
        APP_DIR  = "/home/ubuntu/pipeline/Query-model"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Deploy on EC2') {
            steps {
                sshagent(credentials: ['gpu-ec2']) {
                    sh """
ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} << 'EOF'
set -e

echo "🚀 Moving to app directory"
cd ${APP_DIR}

echo "🔄 Pulling latest code"
git pull origin main

echo "🛑 Stopping old container"
docker compose down

echo "🔨 Building image"
docker compose build

echo "▶️ Starting container"
docker compose up -d

echo "✅ Deployment completed successfully"
EOF
"""
                }
            }
        }
    }

    post {
        success {
            echo "🎉 Jenkins pipeline completed successfully!"
        }
        failure {
            echo "❌ Jenkins pipeline failed!"
        }
    }
}
