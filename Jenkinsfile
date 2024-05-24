pipeline {
    agent any

    environment {
        KUBECONFIG = '/home/vivek-maltare/.kube/config'
    }

    stages {
        // stage('Checkout SCM') {
        //     steps {
        //         // Checkout the source code from the Git repository with credentials
        //         checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/VivekMaltare/Skin-Cancer-Prediction-Django.git']])
        //     }
        // }
         stage('Debug User') {
            steps {
                script {
                    sh 'whoami'
                }
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
        stage('Start docker-compose services') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }
        stage('Delay before down') {
            steps {
                script {
                    sleep 30 // Wait for 1 minute
                }
            }
        }
        stage('Stop docker-compose services') {
            steps {
                script {
                    sh 'docker-compose -f docker-compose.yml down'
                }
            }
        }
        stage('Start Minikube') {
            steps {
                script {
                    sh 'minikube start'
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
        // stage('Delay before stopping Minikube') {
        //     steps {
        //         script {
        //             sleep 1800 // Wait for 30 minutes (1800 seconds)
        //         }
        //     }
        // }
        // stage('Stop Minikube') {
        //     steps {
        //         script {
        //             sh 'minikube stop'
        //         }
        //     }
        // }
    }
}
