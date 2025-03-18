const ctx = document.getElementById("statsChart").getContext("2d");

// Graphique pour suivre l'évolution des requêtes
const statsChart = new Chart(ctx, {
    type: "line",
    data: {
        labels: [],
        datasets: [
            { label: "Requêtes", data: [], borderColor: "blue", fill: false },
            { label: "Latence moyenne (ms)", data: [], borderColor: "red", fill: false }
        ]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Met à jour les statistiques toutes les 2 secondes
async function updateStats() {
    const response = await fetch("http://localhost:8080/stats");
    const data = await response.json();

    document.getElementById("requestCount").innerText = data.requestCount;
    document.getElementById("avgLatency").innerText = data.avgLatency;

    // Ajoute des données au graphique
    statsChart.data.labels.push(new Date().toLocaleTimeString());
    statsChart.data.datasets[0].data.push(data.requestCount);
    statsChart.data.datasets[1].data.push(data.avgLatency);

    statsChart.update();
}

// Simule une charge
async function simulateLoad() {
    const requests = document.getElementById("requests").value;
    const duration = document.getElementById("duration").value;

    await fetch("http://localhost:8080/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ requests, duration })
    });

    alert(`Simulation lancée: ${requests} requêtes sur ${duration} ms.`);
}

// Rafraîchir les stats automatiquement
setInterval(updateStats, 2000);