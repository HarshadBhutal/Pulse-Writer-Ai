const root = document.documentElement;
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.getElementById("themeIcon");

function setTheme(mode) {
  root.setAttribute("data-theme", mode);
  localStorage.setItem("pulse-theme", mode);
  themeIcon.textContent = mode === "light" ? "☀️" : "🌙";
}

function getPreferredTheme() {
  const stored = localStorage.getItem("pulse-theme");
  if (stored === "light" || stored === "dark") return stored;
  const prefersDark =
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;
  return prefersDark ? "dark" : "light";
}

setTheme(getPreferredTheme());

themeToggle.addEventListener("click", () => {
  const current = root.getAttribute("data-theme") === "light" ? "light" : "dark";
  setTheme(current === "light" ? "dark" : "light");
});

let articles = [];

function initArticles() {
  articles = Array.isArray(window.PULSE_ARTICLES)
    ? window.PULSE_ARTICLES
    : [];
  renderCards(articles);
}

document.addEventListener("pulse-articles-loaded", initArticles);

const cardsContainer = document.getElementById("cardsContainer");
const searchInput = document.getElementById("searchInput");

function makePreview(text, maxWords = 26) {
  if (text == null) return "";
  const str = String(text);
  const words = str.split(/\s+/);
  if (words.length <= maxWords) return str;
  return words.slice(0, maxWords).join(" ") + "…";
}

function formatDate(isoString) {
  if (!isoString) return "Today";
  
  const date = new Date(isoString);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const articleDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  
  if (articleDate.getTime() === today.getTime()) {
    return "Today";
  }
  
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  if (articleDate.getTime() === yesterday.getTime()) {
    return "Yesterday";
  }
  
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  });
}

function createCard(article) {
  const card = document.createElement("article");
  card.className = "card";

  const sources = Array.isArray(article.Sources_used)
    ? article.Sources_used.join(", ")
    : article.Sources_used || "Multiple sources";

  const preview = makePreview(article.Text, 26);
  const split=makePreview(article.Title,4)
  card.innerHTML = `
    <div class="card-header">
      <span class="card-chip">
        <span>↗</span>
        <span>${split}</span>
      </span>
      <span class="card-date">${formatDate(article.Created_at)}</span>
    </div>
      <h2 class="card-title">${article.Title}</h2>
      <p class="card-ai-label">AI summary from multiple sources</p>
      <p class="card-preview">${preview}</p>

    `;

  card.addEventListener("click", () => {
    window.location.href = `article.html?id=${(article.Id)}`;
  });

  return card;
}


function renderCards(list) {
  cardsContainer.innerHTML = "";
  list.forEach((a) => cardsContainer.appendChild(createCard(a)));
}

renderCards(articles);

function handleSearch() {
  const q = searchInput.value.toLowerCase().trim();
  articles = Array.isArray(window.PULSE_ARTICLES)
    ? window.PULSE_ARTICLES
    : [];
  const filtered = articles.filter(
    (a) =>
    (String(a.Title) || "").toLowerCase().includes(q) ||
    (String(a.Text) || "").toLowerCase().includes(q)
    );

  renderCards(filtered);
}

searchInput.addEventListener("input", handleSearch);
