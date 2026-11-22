#!/bin/bash
cd ~/emi-assignment
kubectl scale deployment emi-web --replicas=1 -n emi
kubectl rollout status deployment/emi-web -n emi
sleep 30
kubectl apply -f k8s/hpa.yaml
python3 scripts/profile.py results/hpa 620 &
bash scripts/hpa_watch.sh &
python3 scripts/loadgen.py results/hpa 10:120,100:300,10:180 hpa > results/hpa_summary.csv
wait
echo DONE
