ZONE=europe-central2-a
PROJECT=$(gcloud config get-value project)
CLUSTER=jenkins-cd
TARGET="34.110.234.141"
SCOPE="https://www.googleapis.com/auth/cloud-platform"

gcloud config set compute/zone ${ZONE}
gcloud config set project ${PROJECT}

cd distributed-load-testing-using-kubernetes-master/

gcloud container clusters get-credentials $CLUSTER --zone $ZONE --project $PROJECT

gcloud builds submit --tag gcr.io/$PROJECT/locust-tasks:latest docker-image
gcloud container images list | grep locust-tasks

sed -i -e "s/\[TARGET_HOST\]/$TARGET/g" kubernetes-config/locust-master-controller.yaml
sed -i -e "s/\[TARGET_HOST\]/$TARGET/g" kubernetes-config/locust-worker-controller.yaml
sed -i -e "s/\[PROJECT_ID\]/$PROJECT/g" kubernetes-config/locust-master-controller.yaml
sed -i -e "s/\[PROJECT_ID\]/$PROJECT/g" kubernetes-config/locust-worker-controller.yaml

kubectl apply -f kubernetes-config/locust-master-controller.yaml
kubectl apply -f kubernetes-config/locust-master-service.yaml
kubectl apply -f kubernetes-config/locust-worker-controller.yaml