import asyncio, aiohttp, csv, random, sys, time

URL = "http://emi.local/api/emi"
prefix = sys.argv[1]
phases = [tuple(int(x) for x in p.split(":")) for p in sys.argv[2].split(",")]
label = sys.argv[3] if len(sys.argv) > 3 else ""
rows = []

async def one(session):
    body = {"P": random.randint(10000, 5000000),
            "rate": round(random.uniform(5, 25), 2),
            "n": random.randint(6, 120)}
    t0 = time.time()
    try:
        async with session.post(URL, json=body) as r:
            await r.read()
            status = r.status
    except Exception:
        status = 0
    rows.append((round(t0, 3), round((time.time() - t0) * 1000, 2), status))

async def main():
    timeout = aiohttp.ClientTimeout(total=10)
    conn = aiohttp.TCPConnector(limit=0)
    tasks = []
    start = time.time()
    offset = 0
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as s:
        for rate, secs in phases:
            for i in range(rate * secs):
                delay = start + offset + i / rate - time.time()
                if delay > 0:
                    await asyncio.sleep(delay)
                tasks.append(asyncio.create_task(one(s)))
            offset += secs
        await asyncio.gather(*tasks)

asyncio.run(main())
rows.sort()
with open(prefix + "_requests.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["timestamp", "latency_ms", "status"])
    w.writerows(rows)
ok = [r[1] for r in rows if r[2] == 200]
avg = round(sum(ok) / len(ok), 2) if ok else 0
print(f"{label},{sys.argv[2]},{len(rows)},{len(ok)},{len(rows) - len(ok)},{avg}")
