import os
import time
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()

def main():
    print("🚀 Lancement de Docker Compose...")
    run_command("docker compose up --build -d")
    print("✅ HAProxy est prêt !")
    # Arréter HAProxy après interaction avec l'utilisateur
    input("Appuyez sur Entrée pour arrêter HAProxy...")
    run_command("docker compose down")
    print("✅ HAProxy a été arrêté")

if __name__ == "__main__":
    main()
