const http = require('http');
const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Réponse du serveur 2\n');
});
server.listen(3002, () => console.log('Serveur 1 en écoute sur le port 3002'));
