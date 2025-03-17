FROM node:18

WORKDIR /app

# Copier package.json et installer les dépendances
COPY package.json ./
RUN npm install

# Copier les fichiers serveurs
COPY server1.js .
COPY server2.js .

# Définir le point d'entrée pour exécuter le bon serveur
CMD ["node"]
