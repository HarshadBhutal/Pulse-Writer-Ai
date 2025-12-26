

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
    // expected: [{ id, title, text, sources_used, created_at }]
    window.PULSE_ARTICLES = data;
    // optional: notify other scripts that data is ready
    document.dispatchEvent(new CustomEvent("pulse-articles-loaded"));
  } catch (err) {
    console.error("Error loading news:", err);
  }
}

// start loading as soon as data.js is loaded
loadPulseArticles();

