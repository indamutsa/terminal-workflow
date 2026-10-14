/* Site behaviour shared by every page: copy buttons, the cheat sheet drawer and site-wide search. */
"use strict";
(function () {
  const MAX_RESULTS = 40;
  const COPY_RESET_MS = 1500;
  const KIND_LABEL = { p: "Page", h: "Section", c: "Command", k: "Key", t: "Text" };
  const KIND_WEIGHT = { c: 30, k: 30, h: 20, p: 15, t: 0 };
  const PHRASE_BONUS = 100, START_BONUS = 50, SAME_FILE_BONUS = 5;
  const TEXT_LEN_CAP = 200, TEXT_LEN_DIVISOR = 50;
  const root = document.body.dataset.root || "";
  const here = document.body.dataset.file || "index.html";
  // A module lives at <folder>/index.html but is linked as <folder>/.
  const MODULE_FILE_RE = /(^|\/)index\.html$/;
  const TYPING_TARGET = 'input,textarea,select,[contenteditable=""],[contenteditable="true"]';

  // Vim and tmux spellings of the same key must meet: "<C-w>v" and "Ctrl-w v" both become "ctrl-w v".
  function norm(s) {
    return String(s).toLowerCase()
      .replace(/<c-([^>]+)>/g, " ctrl-$1 ")
      .replace(/<leader>/g, "<space>")
      .replace(/\bctrl\+/g, "ctrl-")
      .replace(/\s+/g, " ").trim();
  }

  // ---- copy
  function legacyCopy(text) {
    const area = document.createElement("textarea");
    area.value = text;
    area.setAttribute("readonly", "");
    area.style.position = "fixed";
    area.style.opacity = "0";
    document.body.append(area);
    area.select();
    let ok = false;
    try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
    area.remove();
    return ok;
  }
  async function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      try { await navigator.clipboard.writeText(text); return true; } catch (e) { /* fall through */ }
    }
    return legacyCopy(text);
  }
  document.addEventListener("click", async (event) => {
    const button = event.target.closest(".tw-copy");
    if (!button) return;
    const box = button.closest(".tw-codebox");
    const source = box && (box.querySelector(".tw-copy-src code") || box.querySelector("pre.sq-code code"));
    if (!source) return;
    const ok = await copyText(source.textContent);
    button.textContent = ok ? "Copied" : "Copy failed";
    clearTimeout(button._twReset);
    button._twReset = setTimeout(() => { button.textContent = "Copy"; }, COPY_RESET_MS);
  });

  // ---- cheat sheet
  const STORE_KEY = "tw-cheat";
  const drawer = document.getElementById("tw-cheat");
  const cheatBtn = document.querySelector(".tw-cheat-btn");
  const cheatQ = document.getElementById("tw-cheat-q");
  const cheatTabs = document.getElementById("tw-cheat-tabs");
  const cheatBody = document.getElementById("tw-cheat-body");
  const searchDialog = document.getElementById("tw-search");
  const cheatState = { open: false, tab: "" };
  let cheatNorm = null;

  function loadCheatState() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORE_KEY) || "{}");
      cheatState.open = saved.open === true;
      cheatState.tab = typeof saved.tab === "string" ? saved.tab : "";
    } catch (e) { /* storage unavailable or corrupt: use defaults */ }
  }
  function saveCheatState() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(cheatState)); } catch (e) { /* storage unavailable */ }
  }

  function cheatTable(rows) {
    const table = document.createElement("table");
    table.className = "tw-keytable";
    rows.forEach((row) => {
      const tr = document.createElement("tr");
      const keyCell = document.createElement("td");
      const kbd = document.createElement("kbd");
      kbd.className = "tw-key";
      kbd.textContent = row[0];
      keyCell.append(kbd);
      const actionCell = document.createElement("td");
      actionCell.textContent = row[1];
      tr.append(keyCell, actionCell);
      table.append(tr);
    });
    return table;
  }

  function renderCheat() {
    const sheets = window.TW_CHEAT;
    if (!drawer || !Array.isArray(sheets) || !sheets.length) return;
    if (!sheets.some((s) => s.id === cheatState.tab)) cheatState.tab = sheets[0].id;
    if (!cheatNorm) cheatNorm = sheets.map((s) => s.rows.map((r) => norm(r[0] + " " + r[1])));
    const q = norm(cheatQ.value);
    cheatTabs.replaceChildren();
    sheets.forEach((s) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "tw-cheat-tab";
      b.textContent = s.title;
      b.setAttribute("aria-pressed", String(!q && s.id === cheatState.tab));
      b.addEventListener("click", () => {
        cheatState.tab = s.id;
        cheatQ.value = "";
        saveCheatState();
        renderCheat();
      });
      cheatTabs.append(b);
    });
    cheatBody.replaceChildren();
    if (!q) {
      cheatBody.append(cheatTable(sheets.find((s) => s.id === cheatState.tab).rows));
      return;
    }
    const tokens = q.split(" ");
    let found = 0;
    sheets.forEach((s, si) => {
      const rows = s.rows.filter((_, ri) => tokens.every((t) => cheatNorm[si][ri].includes(t)));
      if (!rows.length) return;
      found += rows.length;
      const h = document.createElement("h3");
      h.className = "tw-cheat-group";
      h.textContent = s.title;
      cheatBody.append(h, cheatTable(rows));
    });
    if (!found) {
      const p = document.createElement("p");
      p.className = "tw-cheat-empty";
      p.textContent = "No match.";
      cheatBody.append(p);
    }
  }

  function setCheatOpen(open) {
    if (!drawer) return;
    cheatState.open = open;
    drawer.hidden = !open;
    document.body.classList.toggle("tw-cheat-open", open);
    if (cheatBtn) cheatBtn.setAttribute("aria-expanded", String(open));
    saveCheatState();
  }

  if (drawer && cheatBtn && cheatQ && cheatTabs && cheatBody) {
    loadCheatState();
    renderCheat();
    setCheatOpen(cheatState.open);
    cheatBtn.addEventListener("click", () => setCheatOpen(!cheatState.open));
    drawer.querySelector(".tw-cheat-close").addEventListener("click", () => setCheatOpen(false));
    cheatQ.addEventListener("input", renderCheat);
    document.addEventListener("keydown", (event) => {
      if (searchDialog && !searchDialog.hidden) return;
      if (event.key === "Escape" && cheatState.open) {
        setCheatOpen(false);
      } else if (event.key === "?" && !event.metaKey && !event.ctrlKey && !event.altKey) {
        if (event.target.closest && event.target.closest(TYPING_TARGET)) return;
        event.preventDefault();
        setCheatOpen(!cheatState.open);
      }
    });
  }

  // ---- search
  const dialog = document.getElementById("tw-search");
  const input = document.getElementById("tw-q");
  const list = document.getElementById("tw-results");
  const openButton = document.querySelector(".tw-search-btn");
  if (!dialog || !input || !list) return;

  let cache = null;
  let active = -1;
  let shown = [];
  let lastFocus = null;

  function index() {
    const data = window.TW_SEARCH;
    if (!data) return null;
    if (!cache) {
      cache = {
        both: data.items.map((it) => norm(it[4] + " " + it[5])),
        text: data.items.map((it) => norm(it[5])),
      };
    }
    return cache;
  }

  function isOpen() { return !dialog.hidden; }

  function openSearch() {
    if (isOpen()) return;
    lastFocus = document.activeElement;
    dialog.hidden = false;
    document.body.classList.add("tw-search-open");
    input.focus();
    input.select();
  }

  function closeSearch() {
    if (!isOpen()) return;
    dialog.hidden = true;
    document.body.classList.remove("tw-search-open");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function search(q) {
    const data = window.TW_SEARCH;
    const c = index();
    if (!data || !c) return [];
    const tokens = q.split(" ");
    const hits = [];
    data.items.forEach((it, i) => {
      const hay = c.both[i];
      if (!tokens.every((t) => hay.includes(t))) return;
      let score = KIND_WEIGHT[it[0]] || 0;
      if (hay.includes(q)) score += PHRASE_BONUS;
      if (c.text[i].startsWith(q)) score += START_BONUS;
      if (data.files[it[1]] === here) score += SAME_FILE_BONUS;
      score -= Math.min(it[5].length, TEXT_LEN_CAP) / TEXT_LEN_DIVISOR;
      hits.push({ i, score });
    });
    hits.sort((a, b) => b.score - a.score || a.i - b.i);
    return hits.slice(0, MAX_RESULTS).map((h) => data.items[h.i]);
  }

  // Mark every case-insensitive literal occurrence of a token, using text nodes only.
  function highlight(host, text, tokens) {
    const lower = text.toLowerCase();
    const marked = new Array(text.length).fill(false);
    tokens.forEach((t) => {
      if (!t) return;
      for (let at = lower.indexOf(t); at !== -1; at = lower.indexOf(t, at + t.length)) {
        for (let k = at; k < at + t.length; k++) marked[k] = true;
      }
    });
    let start = 0;
    while (start < text.length) {
      let end = start;
      while (end < text.length && marked[end] === marked[start]) end++;
      const piece = text.slice(start, end);
      if (marked[start]) {
        const mark = document.createElement("mark");
        mark.textContent = piece;
        host.append(mark);
      } else {
        host.append(document.createTextNode(piece));
      }
      start = end;
    }
  }

  function setActive(next) {
    const options = list.querySelectorAll('[role="option"]');
    if (!options.length) return;
    active = (next + options.length) % options.length;
    options.forEach((li, i) => li.setAttribute("aria-selected", String(i === active)));
    input.setAttribute("aria-activedescendant", options[active].id);
    options[active].scrollIntoView({ block: "nearest" });
  }

  function render(q) {
    list.replaceChildren();
    input.removeAttribute("aria-activedescendant");
    shown = [];
    active = -1;
    if (!q) { input.setAttribute("aria-expanded", "false"); return; }
    input.setAttribute("aria-expanded", "true");
    shown = search(q);
    if (!shown.length) {
      const li = document.createElement("li");
      li.className = "tw-r-text";
      li.textContent = "No match. Try a key like Ctrl-w or a command like git worktree.";
      list.append(li);
      return;
    }
    const data = window.TW_SEARCH;
    const tokens = q.split(" ");
    shown.forEach((it, i) => {
      const li = document.createElement("li");
      li.id = `tw-r-${i}`;
      li.setAttribute("role", "option");
      const mod = data.mods[it[1]];
      const meta = document.createElement("div");
      meta.className = "tw-r-meta";
      const kind = document.createElement("span");
      kind.className = "tw-r-kind";
      kind.textContent = KIND_LABEL[it[0]] || it[0];
      meta.append(kind, document.createTextNode(`M${mod.n} · ${mod.pages[it[2] - 1] || ""}`));
      const title = document.createElement("div");
      title.className = "tw-r-title";
      title.textContent = it[4];
      const snippet = document.createElement("div");
      snippet.className = "tw-r-text";
      highlight(snippet, it[5], tokens);
      li.append(meta, title, snippet);
      li.addEventListener("click", () => go(it));
      list.append(li);
    });
    setActive(0);
  }

  function go(it) {
    const file = window.TW_SEARCH.files[it[1]];
    const target = it[3];
    closeSearch();
    if (file === here) {
      if (location.hash === "#" + target) dispatchEvent(new HashChangeEvent("hashchange"));
      else location.hash = target;
    } else {
      location.href = root + file.replace(MODULE_FILE_RE, "$1") + "#" + target;
    }
  }

  input.addEventListener("input", () => render(norm(input.value)));
  if (openButton) openButton.addEventListener("click", openSearch);
  dialog.addEventListener("click", (event) => { if (event.target === dialog) closeSearch(); });

  document.addEventListener("keydown", (event) => {
    if (isOpen()) {
      if (event.key === "Escape") { event.preventDefault(); event.stopPropagation(); closeSearch(); }
      else if (event.key === "ArrowDown") { event.preventDefault(); setActive(active + 1); }
      else if (event.key === "ArrowUp") { event.preventDefault(); setActive(active - 1); }
      else if (event.key === "Enter" && shown[active]) { event.preventDefault(); go(shown[active]); }
      return;
    }
    if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.target.closest && event.target.closest(TYPING_TARGET)) return;
    event.preventDefault();
    openSearch();
  }, true);
})();
