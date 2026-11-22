import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

req = pd.read_csv("results/hpa_requests.csv")
log = pd.read_csv("results/hpa_log.csv")
log["replicas"] = log["replicas"].ffill().bfill()
t0 = min(req["timestamp"].min(), log["timestamp"].min())
req["t"] = ((req["timestamp"] - t0) // 5) * 5
rate = req.groupby("t").size() / 5
log["t"] = log["timestamp"] - t0

fig, ax = plt.subplots(3, 1, sharex=True, figsize=(9, 8))
ax[0].plot(rate.index, rate.values)
ax[0].set_ylabel("Request rate (req/s)")
ax[1].plot(log["t"], log["cpu_percent"], color="tab:red")
ax[1].axhline(50, ls="--", color="gray")
ax[1].set_ylabel("Avg CPU (%), target 50%")
ax[2].step(log["t"], log["replicas"], where="post", color="tab:green")
ax[2].set_yticks(range(1, 6))
ax[2].set_ylabel("Web replicas")
ax[2].set_xlabel("Time (seconds)")
for a in ax:
    a.grid(True, alpha=0.3)
fig.suptitle("Autoscaling test (10 minutes)")
fig.savefig("results/graph3.png", dpi=150, bbox_inches="tight")
print("saved graph3")
