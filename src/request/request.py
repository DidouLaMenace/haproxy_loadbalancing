import time
import requests
from multiprocessing import Pool
import sys

URL = "http://localhost"

def send_single_request(_):
    try:
        response = requests.get(URL, timeout=2)
        return response.status_code
    except requests.RequestException:
        return "Error"

def send_requests(num_requests, concurrent_workers):
    print(f"🚀 Envoi de {num_requests} requêtes à {URL} avec {concurrent_workers} workers...")
    start_time = time.time()

    with Pool(concurrent_workers) as pool:
        results = pool.map(send_single_request, range(num_requests))

    print(f"✅ Test terminé en {time.time() - start_time:.2f} sec")
    print(f"📊 Résultats HTTP : {dict((x, results.count(x)) for x in set(results))}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python request.py <num_requests> <concurrent_workers>")
        sys.exit(1)
    num_requests = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    concurrent_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    send_requests(num_requests, concurrent_workers)
