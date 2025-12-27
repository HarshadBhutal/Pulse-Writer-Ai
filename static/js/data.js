

// data.js

// global placeholder so other scripts can read it
window.PULSE_ARTICLES = [];

// small helper to fetch from FastAPI and fill the global
async function loadPulseArticles() {
  try {

    const res = await fetch("http://127.0.0.1:8000/article/trending");

    if (!res.ok) {
      console.error("Failed to load news:", res.status);
      return;
    }

    const data = await res.json();
    window.PULSE_ARTICLES = data;
    localStorage.setItem("pulse-articles", JSON.stringify(articles));
    document.dispatchEvent(new CustomEvent("pulse-articles-loaded"));

  } catch (err) {
    console.error("Error loading news:", err);
  }
}

loadPulseArticles();

