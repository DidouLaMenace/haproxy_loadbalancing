#!/bin/bash

echo "🚀 Activation de l'environnement virtuel Python..."
source /app/venv/bin/activate

echo "🚀 Démarrage des serveurs Node.js..."
nohup node /app/backend/server1.js > /dev/null 2>&1 &
nohup node /app/backend/server2.js > /dev/null 2>&1 &

echo "🚀 Démarrage de HAProxy..."
haproxy -f /etc/haproxy/haproxy.cfg &

echo "✅ Serveur prêt à recevoir des requêtes !"

# Maintenir le conteneur actif
tail -f /dev/null
