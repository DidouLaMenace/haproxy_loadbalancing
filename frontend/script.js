async function generateHash() {
    const text = document.getElementById("text").value;
    const algorithm = document.getElementById("algorithm").value;
    const hashTitle = document.getElementById("hashTitle");
    const resultField = document.getElementById("result");

    if (!text) {
        alert("Veuillez entrer un texte.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8080/hash", { // Envoi vers HAProxy
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, algorithm })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erreur serveur");
        }

        // Mettre à jour le titre et le champ du hash
        hashTitle.innerText = `Hash (${data.algorithm.toUpperCase()})`;
        resultField.value = data.hash;
    } catch (error) {
        console.error("Erreur API :", error);
        hashTitle.innerText = "Erreur";
        resultField.value = "Erreur : Impossible de contacter le serveur.";
    }
}

// Fonction pour copier le hash
function copyHash() {
    const resultField = document.getElementById("result");
    resultField.select();
    document.execCommand("copy");
    alert("Hash copié !");
}
