import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("results/r3_rate100_pods.csv")
d = d[d["pod"].str.startswith("emi-web")]
d["t"] = d["timestamp"] - d["timestamp"].min()
d["cpu_pct"] = d["cpu_millicores"]  # request = 100m, so 1m = 1%
for pod, g in d.groupby("pod"):
    plt.plot(g["t"], g["cpu_pct"], marker="o", label=pod.split("-")[-1])
plt.xlabel("Time (seconds)")
plt.ylabel("CPU utilization (% of 100m request)")
plt.title("Per-pod CPU, 100 req/s, 3 replicas")
plt.grid(True, alpha=0.3)
plt.legend(title="web pod")
plt.savefig("results/graph2.png", dpi=150, bbox_inches="tight")
print("saved graph2")
