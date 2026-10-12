/* Course page behaviour: tabs, hash links, rule cards, glossary. Base from the SQL course. */

"use strict";
document.documentElement.classList.add("js-ready");
const lessons = Array.from(document.querySelectorAll(".lesson"));
const tabsHost = document.getElementById("tabs");
const previousButton = document.getElementById("prevBtn");
const nextButton = document.getElementById("nextBtn");
const progress = document.getElementById("progressMini");
let activeLesson = 0;
const tabs = lessons.map((lesson, index) => {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "tab";
  button.id = `tab-${index + 1}`;
  button.setAttribute("role", "tab");
  button.setAttribute("aria-controls", lesson.id);
  button.setAttribute("aria-label", `Open page ${index + 1}`);
  button.textContent = String(index + 1);
  button.addEventListener("click", () => goTo(index));
  tabsHost.append(button);
  return button;
});
function showLesson(index, options = {}) {
  activeLesson = Math.max(0, Math.min(index, lessons.length - 1));
  lessons.forEach((lesson, position) => {
    const selected = position === activeLesson;
    lesson.classList.toggle("active", selected);
    lesson.setAttribute("aria-hidden", String(!selected));
    tabs[position].classList.toggle("active", selected);
    tabs[position].setAttribute("aria-selected", String(selected));
    tabs[position].tabIndex = selected ? 0 : -1;
  });
  previousButton.disabled = activeLesson === 0;
  nextButton.disabled = activeLesson === lessons.length - 1;
  progress.textContent = `${activeLesson + 1}/${lessons.length}`;
  if (options.scroll !== false) window.scrollTo({ top: 0, behavior: "auto" });
}
// Tab moves rewrite the hash without a new history entry, so reload and shared links keep the page.
function goTo(index) {
  showLesson(index);
  history.replaceState(null, "", `#${lessons[activeLesson].id}`);
}
previousButton.addEventListener("click", () => goTo(activeLesson - 1));
nextButton.addEventListener("click", () => goTo(activeLesson + 1));
tabsHost.addEventListener("keydown", (event) => {
  if (event.key === "ArrowRight") { event.preventDefault(); goTo(activeLesson + 1); tabs[activeLesson].focus(); }
  if (event.key === "ArrowLeft") { event.preventDefault(); goTo(activeLesson - 1); tabs[activeLesson].focus(); }
});

const HIT_FLASH_MS = 1600;
// Any id inside a page works as a deep link: open its tab, open its details, then scroll to it.
function routeToHash() {
  const id = decodeURIComponent(location.hash.slice(1));
  const target = id && document.getElementById(id);
  const lesson = target && target.closest(".lesson");
  if (!lesson) return false;
  showLesson(lessons.indexOf(lesson), { scroll: false });
  for (let d = target.closest("details"); d; d = d.parentElement && d.parentElement.closest("details")) d.open = true;
  requestAnimationFrame(() => {
    target.scrollIntoView({ block: "start" });
    if (target === lesson) return;
    target.classList.add("tw-hit");
    setTimeout(() => target.classList.remove("tw-hit"), HIT_FLASH_MS);
  });
  return true;
}
addEventListener("hashchange", routeToHash);
if (!routeToHash()) showLesson(0);

if (!("name" in HTMLDetailsElement.prototype)) {
  document.querySelectorAll(".rule-card").forEach((card) => {
    card.addEventListener("toggle", () => {
      if (!card.open || !card.getAttribute("name")) return;
      const name = card.getAttribute("name");
      document.querySelectorAll(`.rule-card[name="${name}"]`).forEach((other) => {
        if (other !== card && other.open) other.open = false;
      });
    });
  });
}

(function () {
  const glossaryEntries = window.TW_GLOSSARY || [];
      const glossaryFormMap = new Map();
      glossaryEntries.forEach(function (entry) {
        entry.forms.forEach(function (form) {
          glossaryFormMap.set(form.toLowerCase(), entry);
        });
      });
      const glossaryForms = [...glossaryFormMap.keys()].sort(function (a, b) {
        return b.length - a.length;
      });
      const glossaryPattern = new RegExp(
        "\\b(" +
          glossaryForms
            .map(function (term) {
              return term.replace(/[-/\\^$*+?.()|[\]{}]/g, "\\$&");
            })
            .join("|") +
          ")\\b",
        "gi",
      );
      const glossarySkip =
        "button,a,summary,label,input,select,option,textarea,code,pre,script,style,noscript,svg,.tw-codebox,.tw-search,.tw-search-btn,kbd,.glossary-popover,.glossary-term,.eyebrow,.kitchen-strip";
      const glossarySection = 'section[id^="module-"]';

      function applyGlossary(scope) {
        const walker = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, {
          acceptNode: function (node) {
            if (!node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
            const parent = node.parentElement;
            if (!parent || parent.closest(glossarySkip))
              return NodeFilter.FILTER_REJECT;
            glossaryPattern.lastIndex = 0;
            return glossaryPattern.test(node.nodeValue)
              ? NodeFilter.FILTER_ACCEPT
              : NodeFilter.FILTER_REJECT;
          },
        });
        const nodes = [];
        while (walker.nextNode()) nodes.push(walker.currentNode);
        nodes.forEach(function (node) {
          const text = node.nodeValue;
          // One link per term per page. The DOM is the record: the observer below re-runs this on every caption change.
          const section = node.parentElement.closest(glossarySection);
          const linkedHere = new Set();
          const fragment = document.createDocumentFragment();
          let cursor = 0;
          glossaryPattern.lastIndex = 0;
          let match;
          while ((match = glossaryPattern.exec(text))) {
            const entry = glossaryFormMap.get(match[0].toLowerCase());
            if (
              section &&
              (linkedHere.has(entry.id) ||
                section.querySelector(
                  '.glossary-term[data-glossary="' + entry.id + '"]',
                ))
            )
              continue;
            if (match.index > cursor)
              fragment.append(
                document.createTextNode(text.slice(cursor, match.index)),
              );
            const term = document.createElement("button");
            term.type = "button";
            term.className = "glossary-term";
            term.dataset.glossary = entry.id;
            term.setAttribute("aria-haspopup", "dialog");
            term.setAttribute("aria-expanded", "false");
            term.setAttribute("aria-label", match[0] + ": open definition");
            term.textContent = match[0];
            fragment.append(term);
            linkedHere.add(entry.id);
            cursor = match.index + match[0].length;
          }
          // Nothing linked: leave the node alone, or the observer would loop forever.
          if (!linkedHere.size) return;
          if (cursor < text.length)
            fragment.append(document.createTextNode(text.slice(cursor)));
          node.replaceWith(fragment);
        });
      }

      const glossaryPopover = document.createElement("aside");
      glossaryPopover.className = "glossary-popover";
      glossaryPopover.id = "glossary-popover";
      glossaryPopover.hidden = true;
      glossaryPopover.setAttribute("role", "dialog");
      glossaryPopover.setAttribute("aria-label", "Term definition");
      glossaryPopover.innerHTML =
        '<button class="glossary-close" type="button" aria-label="Close definition">×</button><strong class="glossary-title"></strong><p class="glossary-definition"></p><span class="glossary-meta">Definition · Press Esc or click elsewhere to close</span>';
      document.body.append(glossaryPopover);

      let activeGlossaryTerm = null;
      function closeGlossary() {
        if (activeGlossaryTerm)
          activeGlossaryTerm.setAttribute("aria-expanded", "false");
        activeGlossaryTerm = null;
        glossaryPopover.hidden = true;
      }
      function positionGlossary(term) {
        const gap = 13,
          margin = 12,
          termRect = term.getBoundingClientRect();
        glossaryPopover.classList.remove("below");
        glossaryPopover.hidden = false;
        const popRect = glossaryPopover.getBoundingClientRect();
        const left = Math.max(
          margin,
          Math.min(
            innerWidth - popRect.width - margin,
            termRect.left + termRect.width / 2 - popRect.width / 2,
          ),
        );
        let top = termRect.top - popRect.height - gap;
        if (top < margin) {
          top = termRect.bottom + gap;
          glossaryPopover.classList.add("below");
        }
        const pointer = Math.max(
          16,
          Math.min(
            popRect.width - 16,
            termRect.left + termRect.width / 2 - left,
          ),
        );
        glossaryPopover.style.left = left + "px";
        glossaryPopover.style.top =
          Math.min(top, innerHeight - popRect.height - margin) + "px";
        glossaryPopover.style.setProperty("--pointer-x", pointer + "px");
      }
      function openGlossary(term) {
        const entry = glossaryEntries.find(function (item) {
          return item.id === term.dataset.glossary;
        });
        if (!entry) return;
        if (activeGlossaryTerm === term && !glossaryPopover.hidden) {
          closeGlossary();
          return;
        }
        if (activeGlossaryTerm)
          activeGlossaryTerm.setAttribute("aria-expanded", "false");
        activeGlossaryTerm = term;
        term.setAttribute("aria-expanded", "true");
        glossaryPopover.querySelector(".glossary-title").textContent =
          entry.label;
        glossaryPopover.querySelector(".glossary-definition").textContent =
          entry.definition;
        positionGlossary(term);
      }
      document.addEventListener("click", function (event) {
        const term = event.target.closest(".glossary-term");
        if (term) {
          event.preventDefault();
          event.stopPropagation();
          openGlossary(term);
          return;
        }
        if (event.target.closest(".glossary-close")) {
          closeGlossary();
          return;
        }
        if (!event.target.closest(".glossary-popover")) closeGlossary();
      });
      document.addEventListener("keydown", function (event) {
        if (event.key === "Escape" && !glossaryPopover.hidden) {
          const term = activeGlossaryTerm;
          closeGlossary();
          if (term) term.focus();
        }
      });
      addEventListener("resize", closeGlossary);
      addEventListener("scroll", closeGlossary, true);

      const glossaryRoot = document.querySelector("main");
      applyGlossary(glossaryRoot);
      let glossaryQueued = false;
      new MutationObserver(function () {
        if (glossaryQueued) return;
        glossaryQueued = true;
        requestAnimationFrame(function () {
          glossaryQueued = false;
          applyGlossary(glossaryRoot);
        });
      }).observe(glossaryRoot, {
        subtree: true,
        childList: true,
        characterData: true,
      });
    })();
