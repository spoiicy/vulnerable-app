pipeline {
    agent any

    environment {
        // Set Python environment for deployment
        PYTHON_ENV = 'python3.10'
        SEMGREP_APP_TOKEN = credentials('SEMGREP_APP_TOKEN') // Add your Semgrep token in Jenkins credentials
    }

    stages {
        stage('Setup Environment') {
            steps {
                echo 'Setting up the environment...'
                // Install Python and pip dependencies
                sh 'python3 -m venv venv'  // Create virtual environment
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running tests...'
                // Execute pytest tests
                sh './venv/bin/pytest || true'  // Allow pipeline to continue even if tests fail (optional)
            }
        }

        // stage('Semgrep Security Scan') {
        //     steps {
        //         echo 'Running Semgrep security scan...'
        //         // Install Semgrep in the virtual environment
        //         sh './venv/bin/pip install semgrep'
        //         // Run Semgrep scan with the configured token
        //         sh './venv/bin/semgrep ci --code'
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                // Build the Docker image for deployment
                sh 'docker build -t vulnerable-app .'
            }
        }

        stage('Deploy App') {
            steps {
                echo 'Deploying the application...'
                // Run the Docker container
                sh 'docker run -d -p 5000:5000 vulnerable-app'
            }
        }
        
        stage('Clean Up') {
            steps {
                echo 'Cleaning up...'
                // Clean up virtual environment
                sh 'rm -rf venv'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Jenkins workspace...'
            // Clean Jenkins workspace
            cleanWs()
        }
    }
}
