import os
import time
import subprocess
import requests
from multiprocessing import Pool

DOCKER_COMPOSE_FILE = "docker-compose.yml"
URL = "http://localhost"

def run_command(command):
    """Exécute une commande et affiche la sortie en temps réel."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()

def wait_for_haproxy():
    """Attend que HAProxy réponde en HTTP (port 80)."""
    print("🕒 Attente de la disponibilité de HAProxy...")

    while True:
        try:
            response = requests.get(URL, timeout=2)
            if response.status_code == 200:
                print("✅ HAProxy est prêt !")
                break
        except requests.RequestException:
            pass  # HAProxy pas encore prêt, on attend

        time.sleep(2)  # Attendre 2 secondes avant de re-tester

def send_request(_):
    """Envoie une requête à HAProxy et retourne le statut HTTP."""
    try:
        response = requests.get(URL, timeout=2)
        return response.status_code
    except requests.RequestException:
        return "Error"

def stress_test(num_requests=10, concurrent_workers=5):
    """Envoie plusieurs requêtes en parallèle."""
    print(f"🚀 Envoi de {num_requests} requêtes à {URL} avec {concurrent_workers} workers...")
    start_time = time.time()

    with Pool(concurrent_workers) as pool:
        results = pool.map(send_request, range(num_requests))

    print(f"✅ Test terminé en {time.time() - start_time:.2f} sec")
    print(f"📊 Résultats HTTP : {dict((x, results.count(x)) for x in set(results))}")

def main():
    print("🚀 Lancement de Docker Compose...")
    run_command("docker compose up --build -d")

    # Vérifier que HAProxy répond bien sur le port 80
    wait_for_haproxy()

    # Demander une interaction utilisateur avant d'envoyer les requêtes
    input("🔹 Appuyez sur Entrée pour envoyer 10 requêtes vers HAProxy...")

    # Lancer 10 requêtes
    stress_test(10)

if __name__ == "__main__":
    main()
