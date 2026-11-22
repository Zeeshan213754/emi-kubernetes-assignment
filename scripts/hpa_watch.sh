#!/bin/bash
echo "timestamp,replicas,cpu_percent" > ~/emi-assignment/results/hpa_log.csv
for i in $(seq 1 42); do
  R=$(kubectl get hpa emi-web -n emi -o jsonpath='{.status.currentReplicas}')
  C=$(kubectl get hpa emi-web -n emi -o jsonpath='{.status.currentMetrics[0].resource.current.averageUtilization}')
  echo "$(date +%s),$R,$C" >> ~/emi-assignment/results/hpa_log.csv
  sleep 15
done
