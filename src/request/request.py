import requests
import time
import sys
from multiprocessing import Pool

URL = "http://haproxy:80"
NUM_REQUESTS = int(sys.argv[1]) if len(sys.argv) > 1 else 100  # Nombre de requêtes configurable
CONCURRENT_WORKERS = 10  # Nombre de requêtes en parallèle

def send_request(_):
    try:
        response = requests.get(URL)
        return response.status_code
    except requests.exceptions.RequestException:
        return "Error"

if __name__ == "__main__":
    print(f"🚀 Envoi de {NUM_REQUESTS} requêtes à {URL} avec {CONCURRENT_WORKERS} workers...")
    start_time = time.time()
    
    with Pool(CONCURRENT_WORKERS) as pool:
        results = pool.map(send_request, range(NUM_REQUESTS))

    print(f"✅ Test terminé en {time.time() - start_time:.2f} sec")
    print(f"📊 Réponses HTTP : {dict((x, results.count(x)) for x in set(results))}")
