kubectl apply -f deployment.yaml

cd app/prometheus/

kubectl delete cm prometheus-cm
kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml

kubectl apply -f prometheus.yaml
kubectl apply -f grafana.yaml

