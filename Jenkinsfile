pipeline {
    agent any

    environment {
        IMAGE_NAME = "shakilahamed/ai-eks-petclinic-app"
        IMAGE_TAG = "latest"
        KUBE_NAMESPACE = "petclinic"
        DEPLOYMENT_NAME = "petclinic"
        KUBE_MANIFEST = "k8/petclinic-deployment.yaml"
        AWS_REGION = "us-west-2"
        EKS_CLUSTER_NAME = "ai-eks-cluster"
        KUBECONFIG_PATH = "/var/lib/jenkins/.kube/config"
    }

    stages {
        stage('Checkout Source') {
            steps {
                git url: 'https://github.com/shakilmunavary/ai-eks-petclinic-app.git', branch: 'main'
            }
        }

        stage('Check Docker Version') {
            steps {
                sh 'docker version'
            }
        }

        stage('Build Java App') {
            steps {
                sh './mvnw package'
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
                    sh '''
                        echo $PASSWORD | docker login -u $USERNAME --password-stdin
                        docker push shakilahamed/ai-eks-petclinic-app:latest
                    '''
                }
            }
        }


        stage('Deploy to EKS') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key-id', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-access-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        echo "🔐 Updating kubeconfig for EKS cluster..."
                        export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
                        export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
                        aws eks update-kubeconfig --region ${AWS_REGION} --name ${EKS_CLUSTER_NAME} --kubeconfig ${KUBECONFIG_PATH}
                        kubectl apply -f ${KUBE_MANIFEST} --validate=false
                        echo "✅ Kubeconfig updated"
                    '''
                }
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
