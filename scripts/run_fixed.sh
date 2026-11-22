#!/bin/bash
cd ~/emi-assignment
kubectl delete hpa emi-web -n emi --ignore-not-found
echo "replicas,phases,total,ok,errors,avg_ms" > results/summary.csv
for R in 1 2 3; do
  kubectl scale deployment emi-web --replicas=$R -n emi
  kubectl rollout status deployment/emi-web -n emi
  sleep 20
  for RATE in 10 25 50 100 200; do
    echo "== replicas=$R rate=$RATE =="
    P=results/r${R}_rate${RATE}
    python3 scripts/profile.py $P 65 &
    PID=$!
    python3 scripts/loadgen.py $P ${RATE}:60 $R >> results/summary.csv
    wait $PID
    sleep 20
  done
done
echo DONE
