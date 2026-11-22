import csv, subprocess, sys, threading, time
import psutil

prefix, duration = sys.argv[1], int(sys.argv[2])
end = time.time() + duration

def host():
    with open(prefix + "_host.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "host_cpu_percent"])
        while time.time() < end:
            w.writerow([round(time.time(), 1), psutil.cpu_percent(interval=1)])
            f.flush()

def pods():
    with open(prefix + "_pods.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["timestamp", "pod", "cpu_millicores", "mem_mi"])
        while time.time() < end:
            t0 = time.time()
            out = subprocess.run(["kubectl", "top", "pods", "-n", "emi", "--no-headers"],
                                 capture_output=True, text=True).stdout
            for line in out.splitlines():
                p = line.split()
                if len(p) >= 3:
                    w.writerow([round(t0, 1), p[0], p[1].rstrip("m"), p[2].rstrip("Mi")])
            f.flush()
            time.sleep(max(0, 15 - (time.time() - t0)))

ts = [threading.Thread(target=host), threading.Thread(target=pods)]
for t in ts:
    t.start()
for t in ts:
    t.join()
