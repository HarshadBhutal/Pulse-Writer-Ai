// ---------- THEME ----------
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

// ---------- ARTICLE ----------
const titleEl = document.getElementById("articleTitle");
const textEl = document.getElementById("articleText");
const sourcesEl = document.getElementById("articleSources");
const dateEl = document.getElementById("articleDate");

const params = new URLSearchParams(window.location.search);
const idParam = params.get("id");

const articles = Array.isArray(window.PULSE_ARTICLES) ? window.PULSE_ARTICLES : [];

function renderArticle(article) {
  if (!article) {
    titleEl.textContent = "Article not found";
    textEl.textContent =
      "This link does not match any generated summary. Try going back and selecting a different card.";
    sourcesEl.innerHTML = "";
    dateEl.textContent = "";
    return;
  }

  titleEl.textContent = article.Title;
  textEl.textContent = article.Text;
  dateEl.textContent = article.Created_at || "Today";

  sourcesEl.innerHTML = "";
  const src = article.Sources_used;
  if (Array.isArray(src)) {
    src.forEach((s) => {
      const li = document.createElement("li");
      li.textContent = s;
      sourcesEl.appendChild(li);
    });
  } else if (src) {
    const li = document.createElement("li");
    li.textContent = src;
    sourcesEl.appendChild(li);
  }
}



function findArticleById(idParam) {
  const numericId = Number(idParam);
  return (
    window.PULSE_ARTICLES.find((a) => a.Id === numericId) ||
    window.PULSE_ARTICLES.find((a) => String(a.Id) === idParam)
  );
}

function initArticle() {
  const article = findArticleById(idParam);
  console.log("Article found:", article);
  renderArticle(article);
}

// if data already present (navigation from same session)
if (window.PULSE_ARTICLES && window.PULSE_ARTICLES.length > 0) {
  initArticle();
} else {
  document.addEventListener("pulse-articles-loaded", initArticle);
}


