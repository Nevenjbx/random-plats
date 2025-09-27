const result = document.getElementById("result");
const feedback = document.getElementById("feedback");

// Proposer un plat
document.getElementById("btn-random").addEventListener("click", async () => {
  const res = await fetch("/api/random-plat");
  const data = await res.json();
  result.textContent = "👉 " + data.plat;
});

// Ajouter un plat
document.getElementById("btn-add").addEventListener("click", async () => {
  const plat = document.getElementById("new-plat").value;
  if (!plat) return;

  const res = await fetch("/api/add-plat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ plat })
  });

  const data = await res.json();
  if (res.ok) {
    feedback.textContent = data.message;
    document.getElementById("new-plat").value = "";
  } else {
    feedback.textContent = "⚠️ " + data.error;
  }
});