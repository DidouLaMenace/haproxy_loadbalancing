const express = require("express");
const crypto = require("crypto");

const app = express();
const PORT = process.env.PORT || 3000;
let requestCount = 0;

app.get("/hash", (req, res) => {
    requestCount++;
    const algorithms = ["sha256", "sha512", "md5"];
    const algorithm = algorithms[Math.floor(Math.random() * algorithms.length)];
    const hash = crypto.createHash(algorithm).update(Date.now().toString()).digest("hex");
    res.json({ server: "server1", algorithm, hash });
});

app.get("/stats", (req, res) => {
    res.json({ server: "server1", requestCount });
});

app.listen(PORT, () => {
    console.log(`Server1 running on port ${PORT}`);
});
