
// =========================
// DOM ELEMENTS
// =========================

const cardsContainer = document.getElementById("cardsContainer");
const searchInput = document.getElementById("searchInput");

let articles = [];

// =========================
// DATE FORMATTING
// =========================

function formatDate(isoString) {
  if (!isoString) return "Today";

  const date = new Date(isoString);

  if (Number.isNaN(date.getTime())) return "Unknown date";

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const articleDate = new Date(date);
  articleDate.setHours(0, 0, 0, 0);

  const difference = Math.round(
    (today - articleDate) / (1000 * 60 * 60 * 24)
  );

  if (difference === 0) return "Today";
  if (difference === 1) return "Yesterday";

  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

// =========================
// TEXT PREVIEW
// =========================

function makePreview(text, maxWords = 26) {
  if (text == null) return "";

  const words = String(text).trim().split(/\s+/);

  if (words.length <= maxWords) return String(text);

  return words.slice(0, maxWords).join(" ") + "…";
}

// =========================
// CREATE NEWS CARD
// =========================

function createCard(article) {
  const card = document.createElement("article");
  card.className = "card";

  const header = document.createElement("div");
  header.className = "card-header";

  const chip = document.createElement("span");
  chip.className = "card-chip";

  const chipIcon = document.createElement("span");
  chipIcon.textContent = "↗";

  const chipText = document.createElement("span");
  chipText.textContent = makePreview(article.Title, 4);

  chip.append(chipIcon, chipText);

  const date = document.createElement("span");
  date.className = "card-date";
  date.textContent = formatDate(article.Created_at);

  header.append(chip, date);

  const title = document.createElement("h2");
  title.className = "card-title";
  title.textContent = article.Title || "Untitled article";

  const aiLabel = document.createElement("p");
  aiLabel.className = "card-ai-label";
  aiLabel.textContent = "AI summary from multiple sources";

  const preview = document.createElement("p");
  preview.className = "card-preview";
  preview.textContent = makePreview(article.Text, 26);

  card.append(header, title, aiLabel, preview);

  card.addEventListener("click", () => {
    window.location.href = `article.html?id=${encodeURIComponent(article.Id)}`;
  });

  return card;
}

// =========================
// RENDER ARTICLES
// =========================

function renderCards(list) {
  const fragment = document.createDocumentFragment();

  list.forEach((article) => {
    fragment.appendChild(createCard(article));
  });

  cardsContainer.replaceChildren(fragment);
}

// =========================
// INITIALIZE ARTICLES
// =========================

function initArticles() {
  articles = Array.isArray(window.PULSE_ARTICLES)
    ? window.PULSE_ARTICLES
    : [];

  handleSearch();
}

// =========================
// SEARCH
// =========================

function handleSearch() {
  const query = searchInput.value.toLowerCase().trim();

  const filtered = articles.filter((article) => {
    const title = String(article.Title || "").toLowerCase();
    const text = String(article.Text || "").toLowerCase();

    return title.includes(query) || text.includes(query);
  });

  renderCards(filtered);
}

// =========================
// EVENT LISTENERS
// =========================

searchInput.addEventListener("input", handleSearch);

document.addEventListener("pulse-articles-loaded", initArticles);

// Initial rendering
initArticles();