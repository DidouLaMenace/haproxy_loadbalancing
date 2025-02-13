const http = require('http');
const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Réponse du serveur 1\n');
});
server.listen(3001, () => console.log('Serveur 1 en écoute sur le port 3001'));
