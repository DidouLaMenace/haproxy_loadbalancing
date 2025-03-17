FROM node:18

WORKDIR /app

# Copier le dossier frontend dans l'image Docker
COPY ./frontend /app/frontend

# Copier les fichiers de configuration Node.js
COPY ./backend/servers/package.json ./
RUN npm install

# Copier les serveurs Node.js
COPY ./backend/servers/server1.js .
COPY ./backend/servers/server2.js .

# Définir le point d'entrée (remplacé par docker-compose)
CMD ["node"]
