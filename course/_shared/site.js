/* Site behaviour shared by every page: copy buttons, the cheat sheet drawer and site-wide search. */
"use strict";
(function () {
  const MAX_RESULTS = 40;
  const COPY_RESET_MS = 1500;
  const KIND_LABEL = { p: "Page", h: "Section", c: "Command", k: "Key", t: "Text" };
  const KIND_WEIGHT = { c: 30, k: 30, h: 20, p: 15, t: 0 };
  const PHRASE_BONUS = 100, START_BONUS = 50, SAME_FILE_BONUS = 5;
  const SYNONYM_START_BONUS = START_BONUS / 2;
  const TEXT_LEN_CAP = 200, TEXT_LEN_DIVISOR = 50;
  const ACTION_BONUS = PHRASE_BONUS + START_BONUS;
  const WORD_BONUS = 40;
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

  function stem(token) {
    if (!/^[a-z]+$/.test(token)) return token;
    const base = token.replace(/(?:ing|ed|es|s)$/, "");
    return base.length >= 3 ? base : token;
  }

  function whole(hay, word) {
    for (let at = hay.indexOf(word); at !== -1; at = hay.indexOf(word, at + word.length)) {
      const tail = hay.slice(at + word.length).match(/^[a-z0-9]*/)[0];
      if (!/[a-z0-9]/.test(hay[at - 1] || "") && /^(?:s|es|ed|ing)?$/.test(tail)) return true;
    }
    return false;
  }

  function createMatcher(groups) {
    const aliases = new Map();
    // Multiword everyday phrases become one query token, just like their synonym.
    const phrases = groups.flatMap((group) => group.filter((word) => norm(word).includes(" "))
      .map((phrase) => [new RegExp("\\b" + norm(phrase).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b", "g"), norm(group[0])]));
    groups.forEach((group) => {
      const words = [...new Set(group.flatMap((word) => [norm(word), stem(norm(word))]))];
      words.forEach((word) => {
        if (!aliases.has(word)) aliases.set(word, new Set());
        words.forEach((variant) => aliases.get(word).add(variant));
      });
    });
    function query(q) {
      const normalized = phrases.reduce((text, [pattern, word]) => text.replace(pattern, word), norm(q));
      return normalized ? normalized.split(" ").map((original) => {
        const base = stem(original);
        // saved -> sav must discover save's groups as well as literal sav matches.
        const inflected = base === original ? [] : [...aliases.keys()]
          .filter((word) => word.startsWith(base)).flatMap((word) => [...aliases.get(word)]);
        return { original, variants: [...new Set([original, base,
          ...(aliases.get(original) || []), ...(aliases.get(base) || []), ...inflected])] };
      }) : [];
    }
    function match(hay, tokens) {
      let exact = 0;
      const variants = [];
      for (const token of tokens) {
        const variant = token.variants.find((word) => hay.includes(word));
        if (!variant) return null;
        if (hay.includes(token.original)) exact++;
        variants.push(variant);
      }
      return { exact, variants };
    }
    return { query, match };
  }

  function createSearch(data) {
    const matcher = createMatcher(data.syn || []);
    const both = data.items.map((it) => norm(it[4] + " " + it[5]));
    const text = data.items.map((it) => norm(it[5]));
    const description = data.items.map((it) => it[0] === "k"
      ? norm(it[5].split(/ {2,}/).slice(1).join("  ")) : "");
    const title = data.items.map((it) => it[0] === "c" ? norm(it[4]) : "");
    function search(q, here = "", limit = MAX_RESULTS) {
      q = norm(q);
      const tokens = matcher.query(q);
      if (!tokens.length) return { items: [], total: 0 };
      const phrase = new RegExp("(^|[^a-z0-9])" + q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "($|[^a-z0-9])");
      const hits = [];
      data.items.forEach((it, i) => {
        const matched = matcher.match(both[i], tokens);
        if (!matched) return;
        let score = KIND_WEIGHT[it[0]] || 0;
        if (it[0] === "c" || it[0] === "k") score += ACTION_BONUS;
        if (it[0] === "c" && /^\s*(#|\/\/)/.test(it[5])) score -= ACTION_BONUS * 2;
        tokens.forEach((token) => {
          if (token.variants.some((variant) => whole(both[i], variant))) score += WORD_BONUS;
        });
        if (phrase.test(both[i])) score += PHRASE_BONUS;
        // Task titles retain command relevance for multiword queries; single words prefer key actions.
        const action = description[i] || (tokens.length > 1 ? title[i] : "");
        const starts = (variant) => action.startsWith(variant) && whole(action.split(" ")[0], variant);
        if (text[i].startsWith(q) || (action && (action.startsWith(q) || starts(tokens[0].original)))) {
          score += START_BONUS;
        } else if (action && tokens[0].variants.some(starts)) {
          score += SYNONYM_START_BONUS;
        }
        if (data.files[it[1]] === here) score += SAME_FILE_BONUS;
        score -= Math.min(it[5].length, TEXT_LEN_CAP) / TEXT_LEN_DIVISOR;
        hits.push({ i, score, exact: matched.exact });
      });
      hits.sort((a, b) => b.exact - a.exact || b.score - a.score || a.i - b.i);
      // The same row often appears on several pages; keep only its best-ranked copy.
      const seen = new Set();
      const unique = hits.filter((hit) => {
        const key = text[hit.i];
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
      return { items: unique.slice(0, limit).map((hit) => data.items[hit.i]), total: unique.length };
    }
    return { ...matcher, search };
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = { norm, stem, createMatcher, createSearch, highlight };
  }
  if (typeof document === "undefined") return;
  const root = document.body.dataset.root || "";
  const here = document.body.dataset.file || "index.html";
  const engine = createSearch(window.TW_SEARCH || { items: [], files: [] });

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
  // Set by the course menu below. Layers, topmost first: search, cheat sheet, menu panel.
  // Returns true when it closed an open panel.
  let closeMenu = () => false;
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

  function cheatTable(rows, taskFirst = false) {
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
      if (taskFirst) tr.append(actionCell, keyCell);
      else tr.append(keyCell, actionCell);
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
      const sheet = sheets.find((s) => s.id === cheatState.tab);
      cheatBody.append(cheatTable(sheet.rows, sheet.task_first));
      return;
    }
    const tokens = engine.query(q);
    let found = 0;
    sheets.forEach((s, si) => {
      const rows = s.rows.filter((_, ri) => engine.match(cheatNorm[si][ri], tokens));
      if (!rows.length) return;
      found += rows.length;
      const h = document.createElement("h3");
      h.className = "tw-cheat-group";
      h.textContent = s.title;
      cheatBody.append(h, cheatTable(rows, s.task_first));
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
    // An open panel would trap Tab behind the drawer, so close it first and move focus into the drawer.
    const fromMenu = open && closeMenu(false);
    cheatState.open = open;
    drawer.hidden = !open;
    document.body.classList.toggle("tw-cheat-open", open);
    if (cheatBtn) cheatBtn.setAttribute("aria-expanded", String(open));
    saveCheatState();
    if (fromMenu && cheatQ) cheatQ.focus();
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

  // ---- course menu: a permanent column on module pages from SIDE_MIN_WIDTH up, a slide-in panel otherwise
  const side = document.getElementById("tw-side");
  const menuBtn = document.querySelector(".tw-menu-btn");
  const backdrop = document.getElementById("tw-backdrop");
  const SIDE_MIN_WIDTH = 1000;
  const SIDE_MARGIN = 8;

  if (side && menuBtn && backdrop) {
    const wide = matchMedia(`(min-width: ${SIDE_MIN_WIDTH}px)`);
    const menuIsOpen = () => document.body.classList.contains("tw-side-open");

    // Keep the current page's link inside the menu's scroll area.
    function revealCurrent() {
      const link = side.querySelector('[aria-current="page"]');
      if (!link) return;
      const box = side.getBoundingClientRect();
      const at = link.getBoundingClientRect();
      if (at.top < box.top + SIDE_MARGIN) side.scrollTop -= box.top + SIDE_MARGIN - at.top;
      else if (at.bottom > box.bottom - SIDE_MARGIN) side.scrollTop += at.bottom - box.bottom + SIDE_MARGIN;
    }

    // The page switcher (course.js) owns which page is shown; the menu follows it.
    function syncCurrent() {
      const shown = document.querySelector(".lesson.active");
      if (!shown) return;
      side.querySelectorAll("a[data-page]").forEach((link) => {
        if (link.dataset.page === shown.dataset.module) link.setAttribute("aria-current", "page");
        else link.removeAttribute("aria-current");
      });
    }

    function setMenuOpen(open, restoreFocus = true) {
      if (open === menuIsOpen()) return;
      document.body.classList.toggle("tw-side-open", open);
      menuBtn.setAttribute("aria-expanded", String(open));
      if (open) {
        revealCurrent();
        (side.querySelector('[aria-current="page"]') || side.querySelector("summary, a")).focus();
      } else if (restoreFocus && side.contains(document.activeElement)) {
        menuBtn.focus();
      }
    }

    closeMenu = (restoreFocus = true) => {
      const wasOpen = menuIsOpen();
      setMenuOpen(false, restoreFocus);
      return wasOpen;
    };

    syncCurrent();
    document.querySelectorAll(".lesson").forEach((lesson) => {
      new MutationObserver(syncCurrent).observe(lesson, { attributes: true, attributeFilter: ["class"] });
    });
    if (document.body.classList.contains("has-side") && wide.matches) revealCurrent();

    menuBtn.addEventListener("click", () => setMenuOpen(!menuIsOpen()));
    backdrop.addEventListener("click", () => setMenuOpen(false));
    side.addEventListener("click", (event) => { if (event.target.closest("a")) setMenuOpen(false); });
    // Widening a module page turns the panel into the permanent column, so reset the panel state.
    wide.addEventListener("change", () => {
      if (document.body.classList.contains("has-side") && wide.matches) setMenuOpen(false, false);
    });
    document.addEventListener("keydown", (event) => {
      if (!menuIsOpen() || (searchDialog && !searchDialog.hidden)) return;
      if (event.key === "Escape") {
        if (cheatState.open) return; // the cheat sheet sits above the panel and closes first
        event.preventDefault();
        event.stopPropagation();
        setMenuOpen(false);
      } else if (event.key === "Tab") {
        if (drawer && drawer.contains(document.activeElement)) return;
        // Keep Tab inside the open panel.
        const stops = [...side.querySelectorAll("summary, a")].filter((el) => el.offsetParent !== null);
        if (!stops.length) return;
        const first = stops[0], last = stops[stops.length - 1];
        if (!side.contains(document.activeElement)) { event.preventDefault(); first.focus(); }
        else if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    }, true);
  }

  // ---- search
  const dialog = document.getElementById("tw-search");
  const input = document.getElementById("tw-q");
  const list = document.getElementById("tw-results");
  const openButtons = document.querySelectorAll("[data-tw-search]");
  if (!dialog || !input || !list) return;

  let active = -1;
  let shown = [];
  let lastFocus = null;

  function isOpen() { return !dialog.hidden; }

  function openSearch() {
    if (isOpen()) return;
    lastFocus = document.activeElement;
    // A panel left open would stay up, with the page scroll locked, once a result is picked.
    if (closeMenu(false)) lastFocus = menuBtn;
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
    return engine.search(q, here).items;
  }

  // Preserve source offsets when key spellings or whitespace normalize differently.
  function highlightSource(text) {
    let chars = text.split("").flatMap((char, at) => char.toLowerCase().split("")
      .map((value) => ({ value, start: at, end: at + 1 })));
    function replace(pattern, replacement) {
      const source = chars.map((char) => char.value).join("");
      const next = [];
      let at = 0;
      for (const match of source.matchAll(pattern)) {
        next.push(...chars.slice(at, match.index));
        const value = typeof replacement === "function" ? replacement(match) : replacement;
        const start = chars[match.index].start;
        const end = chars[match.index + match[0].length - 1].end;
        value.split("").forEach((letter) => next.push({ value: letter, start, end }));
        at = match.index + match[0].length;
      }
      chars = next.concat(chars.slice(at));
    }
    replace(/<c-([^>]+)>/g, (match) => " ctrl-" + match[1] + " ");
    replace(/<leader>/g, "<space>");
    replace(/\bctrl\+/g, "ctrl-");
    replace(/\s+/g, " ");
    replace(/^\s+|\s+$/g, "");
    return { lower: chars.map((char) => char.value).join(""), chars };
  }

  // Mark the actual matching variant using text nodes only.
  function highlight(host, text, tokens) {
    const { lower, chars } = highlightSource(text);
    const marked = new Array(text.length).fill(false);
    tokens.forEach((t) => {
      if (!t) return;
      for (let at = lower.indexOf(t); at !== -1; at = lower.indexOf(t, at + t.length)) {
        for (let k = chars[at].start; k < chars[at + t.length - 1].end; k++) marked[k] = true;
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
    const tokens = engine.query(q);
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
      const variants = engine.match(norm(it[4] + " " + it[5]), tokens).variants;
      highlight(title, it[4], variants);
      const snippet = document.createElement("div");
      snippet.className = "tw-r-text";
      highlight(snippet, it[5], variants);
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
  openButtons.forEach((button) => button.addEventListener("click", openSearch));
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
