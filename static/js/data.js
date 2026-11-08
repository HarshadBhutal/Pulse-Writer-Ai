window.PULSE_ARTICLES = [];

async function loadPulseArticles() {
  try {
    const res = await fetch("/article/trending");

    if (!res.ok) {
      throw new Error(`HTTP error: ${res.status}`);
    }

    const data = await res.json();

    window.PULSE_ARTICLES = data;
    localStorage.setItem("pulse-articles", JSON.stringify(data));

    document.dispatchEvent(new CustomEvent("pulse-articles-loaded"));
  } catch (err) {
    console.error("Error loading news:", err);
  }
}

loadPulseArticles();