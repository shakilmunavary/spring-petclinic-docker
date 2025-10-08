pipeline {
    agent any

    environment {
        IMAGE_NAME = "shakilahamed/spring-petclinic"
        IMAGE_TAG = "latest"
        KUBE_NAMESPACE = "petclinic"
        DEPLOYMENT_NAME = "petclinic"
        KUBE_MANIFEST = "k8/petclinic-deployment.yaml"
        AWS_REGION = "us-west-2"
        EKS_CLUSTER_NAME = "your-cluster-name"
    }

    stages {
        stage('Checkout Source') {
            steps {
                git url: 'https://github.com/shakilmunavary/spring-petclinic-docker.git', branch: 'main'
            }
        }

        stage('Check Docker Version') {
            steps {
                sh "docker version"
            }
        }

        stage('Build Java App') {
            steps {
                sh "./mvnw package"
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh """
                        echo $PASSWORD | docker login -u $USERNAME --password-stdin
                        docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Authenticate to EKS') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-eks-creds']]) {
                    sh """
                        aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER_NAME}
                    """
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh "kubectl apply -f ${KUBE_MANIFEST}"
            }
        }

        stage('Trigger AI Dashboard') {
            steps {
                sh "curl http://<your-dashboard-host>:5001/eks_dashboard/data?namespace=${KUBE_NAMESPACE}"
            }
        }
    }

    post {
        success {
            echo "✅ PetClinic deployed successfully. Check AI dashboard for diagnostics."
        }
        failure {
            echo "❌ Pipeline failed. Investigate logs and AI feedback."
        }
    }
}
