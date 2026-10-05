const filterForm = document.querySelector("#catalog-filters");
const searchInput = filterForm.querySelector("[name=q]");
const suggestions = document.querySelector("#search-suggestions");
const searchStatus = document.querySelector("#search-status");
let timer;
let controller;
let requestVersion = 0;

function clearSuggestions() {
    suggestions.replaceChildren();
    suggestions.hidden = true;
    searchStatus.textContent = "";
}

function cancelPendingSearch() {
    clearTimeout(timer);
    controller?.abort();
    requestVersion += 1;
    clearSuggestions();
}

function suggestGames() {
    cancelPendingSearch();
    if (!searchInput.value.trim()) return;
    const version = requestVersion;
    const params = new URLSearchParams(new FormData(filterForm));

    timer = setTimeout(async () => {
        controller = new AbortController();
        try {
            const response = await fetch(`${filterForm.dataset.suggestionsUrl}?${params}`, {
                signal: controller.signal,
            });
            if (!response.ok) throw new Error("Search unavailable");
            const data = await response.json();
            if (version !== requestVersion) return;

            for (const game of data.results) {
                const item = document.createElement("li");
                const link = document.createElement("a");
                link.textContent = game.title;
                link.href = game.url;
                item.append(link);
                suggestions.append(item);
            }
            suggestions.hidden = data.results.length === 0;
            searchStatus.textContent = data.results.length
                ? `${data.results.length} suggestions. Use Tab to select a game.`
                : "No matching games.";
        } catch (error) {
            if (error.name !== "AbortError" && version === requestVersion) {
                searchStatus.textContent = "Suggestions unavailable. Press Enter to search.";
            }
        }
    }, 150);
}

searchInput.addEventListener("input", suggestGames);
filterForm.querySelectorAll("select").forEach((select) => {
    select.addEventListener("change", suggestGames);
});
filterForm.addEventListener("keydown", (event) => {
    if (event.key === "Escape") cancelPendingSearch();
});
filterForm.addEventListener("submit", cancelPendingSearch);
