# Utilisation d'Ubuntu avec Node.js, HAProxy et Python
FROM ubuntu:latest

# Mise à jour et installation des dépendances système
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    haproxy \
    curl \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Définition du répertoire de travail
WORKDIR /app

# Copie du backend (Node.js)
COPY backend/servers /app/backend/

# Installation des dépendances Node.js
WORKDIR /app/backend
RUN npm install

# Retour au dossier principal
WORKDIR /app

# Copie du frontend (HTML, CSS, JS)
COPY frontend /app/frontend/

# Copie de la configuration HAProxy
COPY config/haproxy.cfg /etc/haproxy/haproxy.cfg

# Copie des scripts Python et installation des dépendances
COPY src/request /app/src/request/
COPY requirements.txt /app/requirements.txt

# Création et activation d'un environnement virtuel Python
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r /app/requirements.txt

# Copie du script d'entrée et attribution des permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exposer les ports pour HAProxy et les stats
EXPOSE 8080 8404

# Lancer les services via le script d'entrée
CMD ["/entrypoint.sh"]
