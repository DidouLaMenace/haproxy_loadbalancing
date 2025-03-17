const express = require("express");
const crypto = require("crypto");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;
let requestCount = 0;

// Middleware pour parser JSON
app.use(express.json());

// Chemin vers le frontend
const frontendPath = "/app/frontend";

// Servir les fichiers statiques
app.use(express.static(frontendPath));

// Route principale pour servir index.html
app.get("/", (req, res) => {
    res.sendFile(path.join(frontendPath, "index.html"));
});

app.post("/hash", (req, res) => {
    requestCount++;
    const { text, algorithm } = req.body;

    if (!text || !algorithm) {
        return res.status(400).json({ error: "Texte et algorithme requis" });
    }

    try {
        const hash = crypto.createHash(algorithm).update(text).digest("hex");
        res.json({ server: "server1", algorithm, hash });
    } catch (error) {
        res.status(400).json({ error: "Algorithme invalide" });
    }
});

// API de stats (utilisé pour le health check HAProxy)
app.get("/stats", (req, res) => {
    res.json({ server: "server1", status: "OK", requestCount });
});

// Lancer le serveur
app.listen(PORT, () => {
    console.log(`✅ Server1 running on port ${PORT}`);
});
