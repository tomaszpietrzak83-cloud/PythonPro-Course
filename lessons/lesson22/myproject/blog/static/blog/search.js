// SEARCH-SITE: Tom Select turns repeated GET fields into removable tokens.
function createRemoteSelect(selector) {
  const element = document.querySelector(selector);
  if (!element || typeof TomSelect === "undefined") return;

  new TomSelect(element, {
    plugins: ["remove_button"],
    create: (input) =>
      input.trim().length >= 1
        ? { value: input.trim(), text: input.trim() }
        : false,
    persist: false,
    valueField: "value",
    labelField: "text",
    searchField: "text",
    loadThrottle: 250,
    shouldLoad: (query) => query.length >= 1,
    load(query, callback) {
      fetch(`${element.dataset.url}?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then(callback)
        .catch(() => callback());
    },
  });
}

function createLocalSelect(selector, settings = {}) {
  const element = document.querySelector(selector);
  if (!element || typeof TomSelect === "undefined") return;
  new TomSelect(element, { plugins: ["remove_button"], ...settings });
}

function applyHighlights() {
  const dataNode = document.getElementById("highlight-data");
  if (!dataNode) return;
  const data = JSON.parse(dataNode.textContent);

  if (typeof Mark !== "undefined" && data.keywords.length) {
    document.querySelectorAll(".js-keyword-text").forEach((element) => {
      new Mark(element).mark(data.keywords, {
        className: "keyword-highlight",
        separateWordSearch: false,
      });
    });
  }

  const containsAny = (value, terms) =>
    terms.some((term) =>
      value.toLocaleLowerCase().includes(term.toLocaleLowerCase()),
    );
  document.querySelectorAll(".js-author").forEach((element) => {
    element.classList.toggle(
      "author-highlight",
      containsAny(element.dataset.value, data.authors),
    );
  });
  document.querySelectorAll(".js-tag").forEach((element) => {
    element.classList.toggle(
      "tag-highlight",
      containsAny(element.dataset.value, data.tags),
    );
  });
}

function clearHighlights() {
  if (typeof Mark !== "undefined") {
    document
      .querySelectorAll(".js-keyword-text")
      .forEach((element) => new Mark(element).unmark());
  }
  document
    .querySelectorAll(".author-highlight, .tag-highlight")
    .forEach((element) => {
      element.classList.remove("author-highlight", "tag-highlight");
    });
}

createRemoteSelect("#author-select");
createRemoteSelect("#tag-select");
createLocalSelect("#category-select", { create: false });
createLocalSelect("#keyword-select", {
  create: (input) =>
    input.trim() ? { value: input.trim(), text: input.trim() } : false,
  persist: false,
});

document
  .getElementById("article-search-form")
  ?.addEventListener("submit", (event) => {
    event.currentTarget.querySelectorAll("input[name]").forEach((input) => {
      input.disabled = !input.value.trim();
    });
  });
document
  .getElementById("clear-highlights")
  ?.addEventListener("click", clearHighlights);
applyHighlights();
