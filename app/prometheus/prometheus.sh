kubectl create configmap prometheus-cm --from-file prometheus-cm.yaml

kubectl apply -f prometheus.yaml
