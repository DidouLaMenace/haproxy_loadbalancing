import asyncio
import httpx
import time
import statistics
import matplotlib.pyplot as plt

HAPROXY_URL = "http://localhost:8080/hash"
TOTAL_REQUESTS = 10000
CONCURRENCY = 1000  # Nombre de requêtes simultanées
TIMEOUT = 5

latencies = []
failures = 0

sem = asyncio.Semaphore(CONCURRENCY)
lock = asyncio.Lock()

async def send_request(session, i):
    global failures
    async with sem:
        start = time.time()
        try:
            response = await session.post(HAPROXY_URL, json={"text": f"req{i}", "algorithm": "sha256"}, timeout=TIMEOUT)
            latency = (time.time() - start) * 1000
            async with lock:
                if response.status_code == 200:
                    latencies.append(latency)
                else:
                    failures += 1
        except Exception as e:
            async with lock:
                failures += 1
                print(f"❌ Erreur requête {i} : {e}")


async def main():
    print(f"🚀 Lancement de {TOTAL_REQUESTS} requêtes avec {CONCURRENCY} en parallèle")
    async with httpx.AsyncClient() as client:
        tasks = [send_request(client, i) for i in range(TOTAL_REQUESTS)]
        start_time = time.time()
        await asyncio.gather(*tasks)
        total_time = time.time() - start_time

    # === Résultats
    print("\n=== BILAN ===")
    print(f"📤 Total envoyé      : {TOTAL_REQUESTS}")
    print(f"✅ Réussites         : {len(latencies)}")
    print(f"❌ Échecs            : {failures}")
    print(f"⏱️ Durée totale      : {round(total_time, 2)}s")
    if latencies:
        print(f"📊 Latence moyenne   : {int(statistics.mean(latencies))} ms")

    # === Graphique
    plt.figure(figsize=(10, 5))
    plt.plot(latencies, label="Latence (ms)", marker=".")
    plt.title(f"Rafale async de {TOTAL_REQUESTS} requêtes")
    plt.xlabel("Requête #")
    plt.ylabel("Latence (ms)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("/app/src/request/dashboard_async_burst.png")
    print("📸 Graphique : dashboard_async_burst.png")

if __name__ == "__main__":
    asyncio.run(main())
