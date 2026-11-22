import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = pd.read_csv("results/summary.csv")
d["rate"] = d["phases"].str.split(":").str[0].astype(int)
for r, g in d.groupby("replicas"):
    g = g.sort_values("rate")
    plt.plot(g["rate"], g["avg_ms"], marker="o", label=f"{r} replica(s)")
plt.xlabel("Request rate (req/s)")
plt.ylabel("Average response time (ms, log scale)")
plt.title("Average response time vs request rate")
plt.yscale("log")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.savefig("results/graph1.png", dpi=150, bbox_inches="tight")
print("saved graph1")
