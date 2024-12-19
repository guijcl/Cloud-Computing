export PROJECT_ID=$(gcloud info --format='value(config.project)')
sh ./scripts/requirements.sh
sh ./scripts/protoCreate.sh
cd app/
cd protobufs/
cd account/
docker build -t gcr.io/${PROJECT_ID}/account .
cd ..
cd musics/
docker build -t gcr.io/${PROJECT_ID}/musics .
cd ..
cd artist/
docker build -t gcr.io/${PROJECT_ID}/artist .
cd ..
cd api_gateway/
docker build -t gcr.io/${PROJECT_ID}/api-gateway .
cd .. 


docker images

gcloud services enable containerregistry.googleapis.com
gcloud auth configure-docker
docker push gcr.io/${PROJECT_ID}/account
docker push gcr.io/${PROJECT_ID}/musics
docker push gcr.io/${PROJECT_ID}/artist
docker push gcr.io/${PROJECT_ID}/api-gateway

docker images
gcloud container images list


