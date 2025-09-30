document.getElementById("predictForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const payload = {
    Size_sqft: parseFloat(document.getElementById("Size_sqft").value),
    Bedrooms: parseInt(document.getElementById("Bedrooms").value),
    Bathrooms: parseInt(document.getElementById("Bathrooms").value),
    YearBuilt: parseInt(document.getElementById("YearBuilt").value),
    Location: document.getElementById("Location").value
  };

  const model = document.getElementById("modelChoice").value;

  try {
    const res = await fetch(`http://localhost:8000/predict?model=${model}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    const resultDiv = document.getElementById("result");
    resultDiv.classList.remove("hidden");

    if (data.error) {
      resultDiv.style.color = "red";
      resultDiv.innerText = "❌ " + data.error;
    } else {
    resultDiv.innerHTML = `
      <img width="40" height="40" 
           src="https://img.icons8.com/3d-fluency/94/ok.png" 
           alt="ok" style="vertical-align: middle; margin-right: 8px;">
      Predicted Price (${data.model}): <b>$${data.prediction}</b>
    `;
  }
  } catch (err) {
    alert("⚠️ Failed to connect to server. Make sure Flask API is running.");
  }
});
