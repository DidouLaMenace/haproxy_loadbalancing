import time
import requests
from multiprocessing import Pool

URL = "http://localhost"

def send_request(_):
    """Envoie une requête HTTP et affiche les erreurs."""
    try:
        response = requests.get(URL, timeout=5)
        return response.status_code
    except requests.Timeout:
        print("⏳ Timeout: le serveur a mis trop de temps à répondre.")
        return "Timeout"
    except requests.ConnectionError:
        print("🚫 Connexion refusée: Le serveur est peut-être surchargé.")
        return "Connexion refusée"
    except requests.RequestException as e:
        print(f"❌ Autre erreur: {e}")
        return "Error"


def ddos_attack(start_requests=100, step=50, max_workers=500):
    """
    Simule une attaque DDoS en augmentant progressivement le nombre de requêtes
    jusqu'à ce que le serveur plante.
    - `start_requests`: nombre initial de requêtes simultanées.
    - `step`: nombre de requêtes supplémentaires à chaque itération.
    - `max_workers`: nombre maximum de workers.
    """
    current_requests = start_requests

    while True:
        print(f"🚀 Envoi de {current_requests} requêtes simultanées...")
        start_time = time.time()

        with Pool(min(current_requests, max_workers)) as pool:
            results = pool.map(send_request, range(current_requests))

        print(f"✅ Test terminé en {time.time() - start_time:.2f} sec")
        status_counts = {x: results.count(x) for x in set(results)}
        print(f"📊 Résultats HTTP : {status_counts}")

        # Vérifier si HAProxy ou les serveurs commencent à échouer
        # if "Error" in status_counts:
        #     print("💥 Le serveur commence à échouer ! Arrêt du test.")
        #     break

        if current_requests >= 1000:
            print("Arrêt du test.")
            break

        # Augmenter la charge progressivement
        current_requests += step
        time.sleep(1)  # Pause courte avant le prochain test

if __name__ == "__main__":
    ddos_attack()
