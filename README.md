# Loan EMI Calculator on Kubernetes (Minikube)

DS-584 Cloud Computing, Assignment 4. Node.js/Express app, MongoDB replica set
(StatefulSet), NGINX Ingress and a Horizontal Pod Autoscaler.

## Layout
    app/      Express app, public/index.html, Dockerfile
    k8s/      all Kubernetes manifests
    scripts/  load generator, profiler, experiment scripts, graph scripts
    results/  raw CSV outputs and graphs

## 1. Start Minikube
    minikube start --driver=docker --cpus=2 --memory=3072
    minikube addons enable ingress
    minikube addons enable metrics-server
    kubectl create namespace emi

## 2. Build the image
    docker build -t emi-web:1.0 app/
    minikube image load emi-web:1.0

## 3. Deploy everything
    kubectl apply -f k8s/
    kubectl get pods -n emi -w

The mongo-init Job retries until the three mongo pods are ready. If it ends
as Failed, run:
    kubectl delete job mongo-init -n emi
    kubectl apply -f k8s/mongo-init-job.yaml

Check the replica set (1 PRIMARY, 2 SECONDARY):
    kubectl exec -n emi mongo-0 -- mongosh --quiet --eval 'rs.status().members.forEach(m => print(m.name, m.stateStr))'

Note: k8s/hpa.yaml is applied too. Delete it before fixed-replica runs:
    kubectl delete hpa emi-web -n emi

## 4. Open the app
    echo "$(minikube ip) emi.local" | sudo tee -a /etc/hosts
Then open http://emi.local (with the Docker driver on Windows/macOS use
minikube tunnel and 127.0.0.1 emi.local).

## 5. Experiments
    python3 scripts/loadgen.py <prefix> <rate:seconds,...> <label>
    ./scripts/run_fixed.sh     # 15 runs: 1,2,3 replicas x 10,25,50,100,200 req/s
    ./scripts/run_hpa.sh       # 10 minute autoscaling test
    python3 scripts/graph1.py; python3 scripts/graph2.py; python3 scripts/graph3.py
Raw outputs and graphs are saved in results/.
