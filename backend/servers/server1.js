const express = require("express");
const crypto = require("crypto");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = process.env.PORT || 3000;
let requestCount = 0;
let latencies = [];

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

// Route pour afficher le dashboard
app.get("/dashboard", (req, res) => {
    res.sendFile(path.join(frontendPath, "dashboard.html"));
});

app.post("/hash", (req, res) => {
    requestCount++;
    const { text, algorithm } = req.body;

    if (!text || !algorithm) {
        return res.status(400).json({ error: "Texte et algorithme requis" });
    }

    const start = Date.now();
    try {
        const hash = crypto.createHash(algorithm).update(text).digest("hex");
        const latency = Date.now() - start;
        latencies.push(latency);
        res.json({ server: "server1", algorithm, hash });
    } catch (error) {
        res.status(400).json({ error: "Algorithme invalide" });
    }
});

// API des statistiques
app.get("/stats", (req, res) => {
    const avgLatency = latencies.length ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 0;
    res.json({ server: "server1", requestCount, avgLatency: avgLatency.toFixed(2) });
});

// API pour simuler une charge
app.post("/simulate", async (req, res) => {
    const { requests, duration } = req.body;
    if (!requests || !duration) {
        return res.status(400).json({ error: "Nombre de requêtes et durée requis" });
    }

    const interval = duration / requests;
    for (let i = 0; i < requests; i++) {
        setTimeout(async () => {
            await fetch(`http://localhost:${PORT}/hash`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: "test", algorithm: "sha256" }),
            });
        }, i * interval);
    }

    res.json({ message: `Simulation de ${requests} requêtes sur ${duration}ms en cours.` });
});

// Lancer le serveur
app.listen(PORT, () => {
    console.log(`✅ Server1 running on port ${PORT}`);
});
