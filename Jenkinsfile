pipeline {
  
  environment {
    PROJECT = "jenkinstest-351122"
    APP_NAME = "CN-Spotify"
    FE_SVC_NAME = "${APP_NAME}-api-gateway"
    CLUSTER = "jenkins-cd"
    CLUSTER_ZONE = "europe-central2-a"
    IMAGE_TAG = "gcr.io/${PROJECT}/api-gateway:${env.BRANCH_NAME}.${env.BUILD_NUMBER}"
    JENKINS_CRED = "JenkinsTest"
  }

  agent {
    kubernetes {
      yaml """
      apiVersion: v1
      kind: Pod
      spec:
        serviceAccountName: jenkins-sa
        containers:
        #Services
        - name: gcloud
          image: gcr.io/cloud-builders/gcloud
          command:
          - cat
          tty: true
        - name: kubectl
          image: gcr.io/cloud-builders/kubectl
          command:
          - cat
          tty: true
        - name: testenv
          image: gcr.io/jenkinstest-351122/musics
          command:
          - cat
          tty: true
      """
    }
  }


  stages {

    stage('UnitTest') {
    steps {  
        container("gcloud"){
          echo 'Strat Testing ...'          
        
          sh("gcloud builds submit deploymentDocker.yaml")
        }    
      }
    }
    

    stage('Build') { //Builds images and push them to cloud build            
      steps {
        container('gcloud') { 
          echo 'Starting Image Builds'
          
          dir("app/protobufs/account") {
                sh "PYTHONUNBUFFERED=1 gcloud builds submit -t gcr.io/${PROJECT}/account ."
          } 
                   
          dir("app/protobufs/artist"){
                sh "PYTHONUNBUFFERED=1 gcloud builds submit -t gcr.io/${PROJECT}/artist ."
          }

          dir("app/protobufs/api_gateway") { 
                sh "PYTHONUNBUFFERED=1 gcloud builds submit -t gcr.io/${PROJECT}/api-gateway ."
          } 
           
          dir("app/protobufs/musics") {
                sh "PYTHONUNBUFFERED=1 gcloud builds submit -t gcr.io/${PROJECT}/musics ."
          }
          
          echo 'Ended Image Builds'
        }
      }
    }
    
    stage('Deploy Images to GKE with canary') {   
      when { branch 'canary' }        
      steps {
        container('kubectl') { //Deploy images to GKE 
          echo "DEPLOY STARTS"

            echo "VOU FAZER DEPLOY para o canario"
            sh("sed -i.bak 's#gcr.io/gcr.io/api-gateway:1.0.0#${IMAGE_TAG}#' deploymentCanary")
            step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'deploymentCanary.yaml', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
            echo "DEPLOY ENDS" 
            
          } 
      }    
    }
  

    stage('Deploy Images to GKE with master') {   
      when { branch 'master' }        
      steps {
        container('kubectl') { //Deploy images to GKE 
          echo "DEPLOY STARTS in Production"

          script {
            if(sh(script:"kubectl get deploy --namespace production | grep api-gateway", returnStatus: true) == 0) {
              echo "Rolling out api.gateway"
              sh("kubectl set image deployment api-gateway api-gateway=gcr.io/${PROJECT}/api-gateway:latest --namespace=production ")
              sh("kubectl rollout restart deployment api-gateway --namespace=production ")
            }                    

            if(sh(script:"kubectl get deploy --namespace production | grep music", returnStatus: true) == 0) {              
              echo "Rolling out music"
              sh("kubectl set image deployment music musics=gcr.io/${PROJECT}/musics:latest --namespace=production ")
              sh("kubectl rollout restart deployment music --namespace=production ")
            } 

            if(sh(script:"kubectl get deploy --namespace production | grep artist", returnStatus: true) == 0) {              
              echo "Rolling out artist"
              sh("kubectl set image deployment artist artist=gcr.io/${PROJECT}/artist:latest --namespace=production ")
              sh("kubectl rollout restart deployment artist --namespace=production ")
            } 

            if(sh(script:"kubectl get deploy --namespace production | grep account", returnStatus: true) == 0) {             
              echo "Rolling out account"
              sh("kubectl set image deployment account account=gcr.io/${PROJECT}/account:latest --namespace=production ")
              sh("kubectl rollout restart deployment account --namespace=production ")
            } 
            
            if((sh(script:"kubectl get deploy --namespace production | grep api-gateway", returnStatus: true) == 1)
              && (sh(script:"kubectl get deploy --namespace production | grep music", returnStatus: true) == 1)
              && (sh(script:"kubectl get deploy --namespace production | grep artist", returnStatus: true) == 1)
              && (sh(script:"kubectl get deploy --namespace production | grep account", returnStatus: true) == 1)) {
              echo "TUDO NOVO"
              echo "Deploying into production"
              step([$class: 'KubernetesEngineBuilder', namespace:'production', projectId: env.PROJECT, clusterName: env.CLUSTER, zone: env.CLUSTER_ZONE, manifestPattern: 'deploymentProduction.yaml', credentialsId: env.JENKINS_CRED, verifyDeployments: true])
              echo "DEPLOY ENDS production"
            }
          }
        }
      }
    }

    stage('Testing Deployments') {
      steps { 
       
        container('testenv') {
          
          echo 'Strat Testing ...'   
                 
          dir("app/protobufs/musics") {
              sh 'python musicsTest.py'
          }
          
          dir("app/protobufs/account") {
              sh 'python unitTestAccount.py'
          } 
          dir("app/protobufs/artist") {
              sh 'python unitTestArtist.py'
          }
          
        }
      }
    }
  }
}






  

