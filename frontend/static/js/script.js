document.addEventListener("DOMContentLoaded", () => {
  const healthForm = document.getElementById("health-form");
  const imageUploadInput = document.getElementById("image-upload-input");
  const imageDropZone = document.getElementById("image-drop-zone");
  const imagePreviewContainer = document.getElementById(
    "image-preview-container"
  );
  const imagePreview = document.getElementById("image-preview");
  const textInput = document.getElementById("text-input");

  const resultsContainer = document.getElementById("results-container");
  const loader = document.getElementById("loader");
  const placeholder = document.getElementById("placeholder");
  const errorContainer = document.getElementById("error-container");
  const errorMessage = document.getElementById("error-message");

  healthForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    placeholder.classList.add("hidden");
    resultsContainer.classList.add("hidden");
    errorContainer.classList.add("hidden");
    loader.classList.remove("hidden");

    const formData = new FormData(healthForm);

    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "An unknown server error occurred.");
      }

      displayResults(data);
    } catch (err) {
      displayError(err.message);
    } finally {
      loader.classList.add("hidden");
    }
  });

  function displayResults(data) {
    document.getElementById("extracted-text").textContent =
      data.extracted_text || "No text was extracted.";

    const factorsContainer = document.getElementById("risk-factors-container");
    factorsContainer.innerHTML = "";
    (data.factors || []).forEach((factor) => {
      const factorEl = document.createElement("span");
      factorEl.className =
        "inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2";
      factorEl.textContent = `${factor.factor} (${(
        factor.confidence * 100
      ).toFixed(0)}%)`;
      factorsContainer.appendChild(factorEl);
    });

    const riskLevelContainer = document.getElementById("risk-level-container");
    const riskLevelClass = getRiskClass(data.risk_level);
    riskLevelContainer.innerHTML = `
            <span class="text-lg font-bold ${riskLevelClass.textColor}">${data.risk_level}</span>
            <span class="text-sm font-semibold text-gray-600">Score: ${data.score}</span>
        `;
    riskLevelContainer.className = `mt-2 p-4 rounded-lg flex items-center justify-between ${riskLevelClass.bgColor}`;

    // Recommendations
    const recsContainer = document.getElementById("recommendations-container");
    recsContainer.innerHTML = '';

    const recs = data.recommendations || [];

    recs.forEach((rec, index) => {
      const recEl = document.createElement("div");
      recEl.className =
        "bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-lg mb-3 shadow-sm";
      recEl.innerHTML = `
            <span class="font-semibold text-indigo-700 mr-2">Recommendation ${
              index + 1
            }:</span>
            <span class="text-gray-800">${rec}</span>
        `;
      recsContainer.appendChild(recEl);
    });
    console.log(recs);
    resultsContainer.classList.remove("hidden");
  }

  function displayError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove("hidden");
  }

  function getRiskClass(level) {
    switch (level.toLowerCase()) {
      case "high":
        return { bgColor: "bg-red-100", textColor: "text-red-800" };
      case "moderate":
        return { bgColor: "bg-yellow-100", textColor: "text-yellow-800" };
      case "low":
        return { bgColor: "bg-green-100", textColor: "text-green-800" };
      default:
        return { bgColor: "bg-gray-100", textColor: "text-gray-800" };
    }
  }

  function handleFile(file) {
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = (e) => {
        imagePreview.src = e.target.result;
        imagePreviewContainer.classList.remove("hidden");
      };
      reader.readAsDataURL(file);
    }
  }

  imageUploadInput.addEventListener("change", (e) =>
    handleFile(e.target.files[0])
  );

  imageDropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    imageDropZone.classList.add("border-indigo-600");
  });

  imageDropZone.addEventListener("dragleave", () => {
    imageDropZone.classList.remove("border-indigo-600");
  });

  imageDropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    imageDropZone.classList.remove("border-indigo-600");
    const file = e.dataTransfer.files[0];
    imageUploadInput.files = e.dataTransfer.files;
    handleFile(file);
  });
});
