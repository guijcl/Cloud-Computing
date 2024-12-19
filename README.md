
# Spotify Music Charts

This is a complete dataset of all the "Top 200" and "Viral 50" charts published globally by Spotify. Spotify publishes a new chart every 2-3 days. This is its entire collection since January 1, 2017.

---

### Running the application Locally

- Install the requirements
    pip install -r requirements.txt
        
- Create the protobuf files

    In the folder /CN-Spotify/app/protobufs/account run a terminal with the following command
        python3 -m grpc_tools.protoc -I ../../protobufs --python_out=. --grpc_python_out=. ../../protobufs/account.proto

    In the folder /CN-Spotify/app/protobufs/music run a terminal with the following command
        python3 -m grpc_tools.protoc -I ../../protobufs --python_out=. --grpc_python_out=. ../../protobufs/music.proto

- Move the .csv file into the folder "/CN-Spotify/app/database/"

- Run the .sh file contained in the folder "/CN-Spotify/scripts"
    inside this folder you will find a file with the following command "docker-compose up" , which will build and run all the docker containers, and create a network "cn-spotify_local" for them to communicate 

### Deploy in GCP

Run the deploy.sh file contained in the folder "/CN-Spotify"

then in the GCP terminal run the following commands:
    kubectl apply -f deployment.yaml
    kubectl apply -f gateway_deployment.yaml
     # the following commands about prometheus are not currently working
     # kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml
     # kubectl apply -f prometheus.yaml
    kubectl apply -f mongodb-secrets.yaml
    kubectl create -f mongodb-pvc.yaml
    kubectl apply -f mongodb-deployment.yaml
    kubectl create -f mongodb-nodeport-svc.yaml
    kubectl create -f mongodb-client.yaml
 
### Notes

- The .csv file should be called "charts_0.csv" for the container to work properly
- The database is not populated, so in order to insert data into it, the script contained in the file "/CN-Spotify/app/database" called "scriptPopulateDB.py" should be run first and, to verify if the data was successfully inserted, run the script "script2.py"

## Authors

- [@António Pedro - fc52795](https://github.com/Darth-tope)
- [@Eduardo Madeira - fc51720](https://github.com/eduardomadeira98)
- [@Gonçalo Rocha - fc57410](https://github.com/gonzaleZMMR)
- [@Guilherme Lopes - fc52761](https://github.com/guijcl)
- [@Henrique Céu - fc57584](https://github.com/HenriqueCeu)
