let selectedFile = null;
let chart = null;

// ---------------- FILE SELECT ----------------
document.getElementById("fileInput").addEventListener("change", function () {

  selectedFile = this.files[0];

  console.log("FILE SELECTED:", selectedFile);

  if (!selectedFile) return;

  const reader = new FileReader();

  reader.onload = function (e) {
    const img = document.getElementById("preview");
    img.src = e.target.result;
    img.style.display = "block";
  };

  reader.readAsDataURL(selectedFile);
});


// ---------------- UPLOAD FUNCTION ----------------
async function upload() {

  console.log("UPLOAD CLICKED");

  if (!selectedFile) {
    alert("Please select an image first");
    return;
  }

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {

    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData
    });

    console.log("STATUS:", res.status);

    const data = await res.json();

    console.log("API RESPONSE:", data);

    // ---------------- SAFE VALUES ----------------
    const status = data.status || "NO STATUS";
    const confidence = data.confidence ?? 0;
    const defects = data.defects || [];
    const stats = data.stats || { total: 0, pass: 0, fail: 0 };

    // ---------------- UPDATE UI ----------------
    if (data.annotated_image_url) {
      document.getElementById("preview").src = data.annotated_image_url;
    }

    const statusEl = document.getElementById("statusText");
    statusEl.innerText = status;

    // color change
    statusEl.classList.remove("status-pass", "status-fail");
    if (status === "PASS") {
      statusEl.classList.add("status-pass");
    } else {
      statusEl.classList.add("status-fail");
    }

    document.getElementById("confidence").innerText =
      Number(confidence).toFixed(2);

    // ---------------- DEFECT LIST ----------------
    const list = document.getElementById("defectList");
    list.innerHTML = "";

    if (Array.isArray(defects) && defects.length > 0) {
      defects.forEach(d => {
        const li = document.createElement("li");
        li.innerText = d;
        list.appendChild(li);
      });
    } else {
      list.innerHTML = "<li>✅ No defects detected</li>";
    }

    // ---------------- STATS ----------------
    document.getElementById("stats").innerText =
      `Total: ${stats.total} | PASS: ${stats.pass} | FAIL: ${stats.fail}`;

    // ---------------- CHART ----------------
    const ctx = document.getElementById("chart");

    if (chart) chart.destroy();

    chart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["PASS", "FAIL"],
        datasets: [{
          data: [stats.pass || 0, stats.fail || 0],
          backgroundColor: ["#00ff7b", "#ff4d4d"]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: {
              color: "white"
            }
          }
        }
      }
    });

  } catch (error) {
    console.error("UPLOAD ERROR:", error);
    alert("Backend not responding or API error");
  }
}