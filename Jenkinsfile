pipeline {
    agent any
    
    environment {
        KUBECONFIG = '/home/vivek-maltare/.kube/config'
    }

    stages {
        stage('Debug') {
            steps {
                sh 'whoami'
                sh 'ls -l /home/vivek-maltare/.kube/config'
            }
        }
        stage('Checkout') {
            steps {
                // Checkout the source code from the Git repository with credentials
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/VivekMaltare/Skin-Cancer-Prediction-Django.git']])
            }
        }
        stage('Build docker image'){
            steps{
                script{
                    sh 'docker build -t vivekmaltare/spe_major_project .'
                }
            }
        }
        stage('Push Docker image') {
            steps {
                script {
                    withCredentials([string(credentialsId: 'DockerHubCreds', variable: 'Binding')]) {
                        sh 'docker login -u vivekmaltare -p ${Binding}'
                    }
                    sh 'docker push vivekmaltare/spe_major_project'
                }
            }
        }
        stage('Start Services') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
        stage('Delay') {
            steps {
                script {
                    sleep 30 // Wait for 1 minute
                }
            }
        }
        stage('Stop Containers') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml down'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl --kubeconfig=$KUBECONFIG apply -f k8s_resources/'
                }
            }
        }
    }
}
