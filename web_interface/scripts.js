//===================================
// Function to update favicon based on state
//===================================
function updateFavicon(state) {
  const favicon = document.getElementById("favicon");
  const states = {
    idle: "/static/favicon/idle.svg",
    processing: "/static/favicon/processing.svg",
    success: "/static/favicon/success.svg",
    error: "/static/favicon/error.svg",
  };

  if (states[state]) {
    favicon.href = states[state];
  }
}

//===================================
// State management to track image processing
//===================================
const imageState = {
  originalFilenames: [],
  currentFilenames: [],
  lastOperation: null,
};

//===================================
// Event listener for when the DOM content is loaded
//===================================
document.addEventListener("DOMContentLoaded", () => {
  //===================================
  // Variable declarations and element selection
  //===================================
  const themeToggle = document.getElementById("themeToggle");
  const modal = document.getElementById("notificationModal");
  const messageElement = document.getElementById("notificationMessage");
  const closeModal = document.getElementById("closeModal");
  const originalImagesPreview = document.getElementById(
    "originalImagesPreview"
  );
  const datasetInput = document.getElementById("dataset");
  const uploadBtn = document.getElementById("uploadBtn");
  const augmentBtn = document.getElementById("augmentBtn");
  const preprocessingButtons = document.querySelectorAll(
    "#preprocessing button"
  );
  const augmentationSelect = document.getElementById("augmentationSelect");
  const processedImagesPreview = document.getElementById(
    "processedImagesPreview"
  );
  const burgerMenu = document.querySelector(".burger-menu");
  const nav = document.querySelector(".nav");
  const uploadArea = document.getElementById("uploadArea");

  //===================================
  // Close modal event handler
  //===================================
  closeModal.onclick = () => {
    modal.style.display = "none";
  };

  //===================================
  // Initialize theme to dark
  //===================================
  setTheme("dark");

  //===================================
  // Event listener for theme toggle button
  //===================================
  themeToggle.addEventListener("click", toggleTheme);

  //===================================
  // Functions to handle theme setting and toggling
  //===================================
  function setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    updateThemeIcon(theme);
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    setTheme(newTheme);
  }

  function updateThemeIcon(theme) {
    if (!themeToggle) return;
    themeToggle.innerHTML = theme === "dark" ? getDarkIcon() : getLightIcon();
  }

  function getDarkIcon() {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
            </svg>`;
  }

  function getLightIcon() {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 A7 7 0 0 0 21 12.79z"/>
            </svg>`;
  }

  //===================================
  // Function to show notification modal
  //===================================
  function showNotification(message) {
    messageElement.textContent = message;
    modal.style.opacity = "0";
    modal.style.display = "flex";

    // Force reflow
    void modal.offsetWidth;

    modal.classList.add("show");
    modal.style.opacity = "1";

    // Auto-hide after 10 seconds
    setTimeout(() => {
      hideNotification();
    }, 10000);
  }

  function hideNotification() {
    modal.classList.remove("show");
    modal.style.opacity = "0";

    // Wait for transition to complete before hiding
    setTimeout(() => {
      modal.style.display = "none";
    }, 300); // Match this with your CSS transition time
  }

  // Update modal close handlers
  closeModal.addEventListener("click", hideNotification);
  window.addEventListener("click", (event) => {
    if (event.target === modal) hideNotification();
  });

  //===================================
  // Function to toggle buttons' disabled state
  //===================================
  function toggleButtons(disable) {
    document
      .querySelectorAll("#preprocessing button, #augmentBtn, #detectTumorBtn")
      .forEach((button) => {
        button.disabled = disable;
      });
  }

  //===================================
  // Function to apply processing or augmentation
  //===================================
  async function applyProcessingOrAugmentation(type, retries = 3) {
    updateFavicon("processing");
    let lastError = null;

    for (let attempt = 0; attempt < retries; attempt++) {
      try {
        if (imageState.originalFilenames.length === 0) {
          showNotification("Please upload images before applying processing!");
          return;
        }

        // Add delay between retries
        if (attempt > 0) {
          await new Promise((resolve) => setTimeout(resolve, 1000 * attempt));
        }

        // Reset current filenames when applying new processing or augmentation
        if (type !== "detect") {
          imageState.currentFilenames = [];
          imageState.lastOperation = type;
        }

        const filenamesToProcess = getFilenamesToProcess(type);

        const response = await fetch(
          type === "augmentation"
            ? "/augment"
            : type === "detect"
            ? "/detect"
            : "/process",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              type: type === "augmentation" ? augmentationSelect.value : type,
              filenames: filenamesToProcess,
            }),
          }
        );

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(errorText || "Network response was not ok");
        }

        const data = await response.json();
        if (data.error) {
          throw new Error(data.error);
        }

        // Success case
        updateFavicon("success");
        processedImagesPreview.innerHTML = "";

        if (type === "detect") {
          displayDetectionResults(data.detection_results);
        } else {
          displayProcessedImages(data.image_urls);
          imageState.currentFilenames = data.image_urls.map((url) =>
            url.split("/").pop()
          );
        }
        return;
      } catch (error) {
        lastError = error;
        console.error(`Error during ${type} (attempt ${attempt + 1}):`, error);

        if (attempt === retries - 1) {
          updateFavicon("error");
          showNotification(
            `Failed to perform ${type.replace("_", " ")}: ${error.message}`
          );
        }
      }
    }
  }

  function getFilenamesToProcess(type) {
    return type === "detect"
      ? imageState.currentFilenames.length > 0
        ? imageState.currentFilenames
        : imageState.originalFilenames
      : imageState.originalFilenames;
  }

  //===================================
  // Function to display detection results
  //===================================
  function displayDetectionResults(results) {
    processedImagesPreview.innerHTML = "";
    const statsContainer = document.getElementById("detectionStats");
    const statsText = document.getElementById("statsText");

    // Count tumors
    const totalImages = results.length;
    const tumorsFound = results.filter(
      (result) => result.tumor_detected
    ).length;
    const healthyImages = totalImages - tumorsFound;

    // Create statistics text
    let statsMessage = `Analysis Complete: `;
    if (totalImages === 1) {
      statsMessage +=
        tumorsFound === 1
          ? "Tumor detected in the image."
          : "No tumor detected in the image.";
    } else {
      statsMessage += `Out of ${totalImages} images analyzed, `;
      statsMessage += `<strong>${tumorsFound}</strong> ${
        tumorsFound === 1 ? "image has" : "images have"
      } tumors detected and `;
      statsMessage += `<strong>${healthyImages}</strong> ${
        healthyImages === 1 ? "image appears" : "images appear"
      } healthy.`;
    }

    // Show statistics
    statsText.innerHTML = statsMessage;
    statsContainer.style.display = "block";

    // Display images
    results.forEach((result) => {
      const imgWrapper = document.createElement("div");
      imgWrapper.classList.add("processed-image-container");

      // Create and append download button first
      const downloadBtn = document.createElement("button");
      downloadBtn.className = "download-button";
      downloadBtn.setAttribute("aria-label", "Download image");
      downloadBtn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
        `;

      // Add download functionality
      downloadBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        try {
          const response = await fetch(result.image_url);
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = downloadUrl;
          link.download = result.image_url.split("/").pop();
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
          console.error("Error downloading image:", error);
          showNotification("Failed to download image");
        }
      });

      // Create and append the image
      const img = document.createElement("img");
      img.src = result.image_url;

      // Create caption
      const caption = document.createElement("div");
      caption.classList.add("detection-caption");
      caption.classList.add(result.tumor_detected ? "error" : "success");
      caption.textContent = result.tumor_detected
        ? "Tumor detected."
        : "No tumor detected.";

      // Append elements in order
      imgWrapper.appendChild(downloadBtn);
      imgWrapper.appendChild(img);
      imgWrapper.appendChild(caption);

      // Add detection details if tumor is detected
      if (result.tumor_detected && result.details) {
        result.details.forEach((detail) => {
          const detailText = document.createElement("p");
          detailText.classList.add("detection-detail-text");
          detailText.textContent = `Type: ${detail.type}, Location: ${detail.location}, Confidence: ${detail.confidence}`;
          imgWrapper.appendChild(detailText);
        });
      }

      processedImagesPreview.appendChild(imgWrapper);
    });
  }

  //===================================
  // Function to display processed images
  //===================================
  function displayProcessedImages(imageUrls) {
    processedImagesPreview.innerHTML = "";
    imageUrls.forEach((url) => {
      const container = document.createElement("div");
      container.className = "processed-image-container";

      const downloadBtn = document.createElement("button");
      downloadBtn.className = "download-button";
      downloadBtn.setAttribute("aria-label", "Download image");
      downloadBtn.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
        `;

      downloadBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        try {
          const response = await fetch(url);
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = downloadUrl;
          link.download = url.split("/").pop();
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
          console.error("Error downloading image:", error);
          showNotification("Failed to download image");
        }
      });

      const img = document.createElement("img");
      img.src = url;

      container.appendChild(downloadBtn);
      container.appendChild(img);
      processedImagesPreview.appendChild(container);
    });
  }

  //===================================
  // Event listener for upload button click
  //===================================
  uploadBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    const files = datasetInput.files;
    if (files.length === 0) {
      updateFavicon("error");
      showNotification("Please select at least one image!");
      return;
    }

    updateFavicon("processing"); // Only set processing if files are selected
    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append("images", file));

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) {
        updateFavicon("error");
        throw new Error(
          (await response.text()) || "Network response was not ok"
        );
      }

      const data = await response.json();
      if (data.error) {
        updateFavicon("error");
        showNotification(data.error);
      } else {
        updateFavicon("success");
        originalImagesPreview.innerHTML = "";
        data.image_urls.forEach((url) => {
          const img = document.createElement("img");
          img.src = url;
          img.dataset.filename = url.split("/").pop();
          originalImagesPreview.appendChild(img);
        });
        toggleButtons(false);

        // Store original filenames and reset state
        imageState.originalFilenames = data.image_urls.map((url) =>
          url.split("/").pop()
        );
        imageState.currentFilenames = [];
        imageState.lastOperation = null;
      }
    } catch (error) {
      updateFavicon("error");
      console.error("Error uploading files:", error);
      showNotification("An error occurred while uploading the files.");
    }
  });

  //===================================
  // Event listeners for preprocessing buttons
  //===================================
  preprocessingButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      applyProcessingOrAugmentation(button.dataset.type);
    });
  });

  //===================================
  // Event listener for augment button click
  //===================================
  augmentBtn.addEventListener("click", (e) => {
    e.preventDefault();
    applyProcessingOrAugmentation("augmentation");
  });

  //===================================
  // Event listener for detect tumor button
  //===================================
  document
    .getElementById("detectTumorBtn")
    .addEventListener("click", async () => {
      const button = document.getElementById("detectTumorBtn");
      const originalText = button.textContent;

      // Add loading state
      button.classList.add("loading");
      button.disabled = true;

      try {
        await applyProcessingOrAugmentation("detect");

        // Show success state
        button.classList.remove("loading");
        button.classList.add("success");

        // Reset button after 1 second
        setTimeout(() => {
          button.classList.remove("success");
          button.disabled = false;
          button.textContent = originalText;
        }, 1000);
      } catch (error) {
        // Reset button immediately on error
        button.classList.remove("loading");
        button.disabled = false;
        button.textContent = originalText;
      }
    });

  //===================================
  // Initially disable buttons
  //===================================
  toggleButtons(true);

  //===================================
  // Event listener for burger menu toggle
  //===================================
  burgerMenu.addEventListener("click", () => {
    burgerMenu.classList.toggle("active");
    nav.classList.toggle("active");
  });

  //===================================
  // Close burger menu when clicking outside
  //===================================
  document.addEventListener("click", (event) => {
    if (!burgerMenu.contains(event.target) && !nav.contains(event.target)) {
      burgerMenu.classList.remove("active");
      nav.classList.remove("active");
    }
  });

  //===================================
  // Close burger menu when a nav link is clicked
  //===================================
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      burgerMenu.classList.remove("active");
      nav.classList.remove("active");
    });
  });

  //===================================
  // Event listeners for upload area drag and drop
  //===================================
  uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.add("dragover");
  });

  uploadArea.addEventListener("dragleave", (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove("dragover");
  });

  uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    e.stopPropagation();
    uploadArea.classList.remove("dragover");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      datasetInput.files = files;
      uploadBtn.click();
    }
  });
});
