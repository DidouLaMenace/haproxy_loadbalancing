import requests
import time
import statistics
import matplotlib.pyplot as plt

HAPROXY_URL = "http://localhost:8080/hash"
STEP = 100       
MAX_LATENCY_THRESHOLD = 1000

latencies = []
failures = 0
total_sent = 0
server_down = False
steps = []

current_batch_size = STEP

while not server_down:
    print(f"\n Envoi d'un lot de {current_batch_size} requêtes...")
    batch_latencies = []

    for _ in range(current_batch_size):
        total_sent += 1  # ← toujours compter la requête envoyée
        try:
            start = time.time()
            res = requests.post(HAPROXY_URL, json={"text": "stress", "algorithm": "sha256"}, timeout=5)
            latency = (time.time() - start) * 1000
            if res.status_code == 200:
                latencies.append(latency)
                batch_latencies.append(latency)
            else:
                failures += 1
                server_down = True
                print("Réponse non valide du serveur.")
                break
        except Exception as e:
            print("Erreur de connexion :", e)
            failures += 1
            server_down = True
            break


    total_sent += len(batch_latencies)
    if batch_latencies:
        avg = statistics.mean(batch_latencies)
        print(f"Latence : ")
        steps.append((total_sent, avg))
        min_latency = int(min(batch_latencies))
        max_latency = int(max(batch_latencies))
        print(f"    Min : {min_latency} ms | Max : {max_latency} ms | Moyenne : {int(avg)} ms")
        print(f"Total cumulé : {current_batch_size} | Échecs cumulés : {failures}")

    current_batch_size += STEP

# === Résultats ===
# print("\n=== BILAN FINAL ===")
# print(f"Total envoyé : {total_sent}")
# print(f"Requêtes réussies : {len(latencies)}")
# print(f"Échecs : {failures}")
# if latencies:
#     print(f"Latence moyenne totale : {int(statistics.mean(latencies))} ms")

# # === Graphique de latence individuelle ===
# plt.figure(figsize=(10, 5))
# plt.plot(latencies, label="Latence par requête (ms)", marker=".")
# plt.title("Latence des requêtes")
# plt.xlabel("Requête #")
# plt.ylabel("Latence (ms)")
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.savefig("/app/src/request/latences.png")
# print("📸 Graphique latence individuelle : latences.png")

# # === Graphique latence moyenne par vague ===
# if steps:
#     lots, moyennes = zip(*steps)
#     plt.figure(figsize=(10, 5))
#     plt.plot(lots, moyennes, label="Latence moyenne par lot", marker="o")
#     plt.title("Évolution de la latence moyenne par vague")
#     plt.xlabel("Nombre total de requêtes")
#     plt.ylabel("Latence moyenne (ms)")
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig("/app/src/request/lots.png")
#     print("📸 Graphique par vague : lots.png")
