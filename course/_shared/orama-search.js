/* Orama retrieval for course text, code, keyboard shortcuts and command flags. */
"use strict";
(function (scope) {
  const commonJS = typeof module !== "undefined" && module.exports;
  const orama = commonJS ? require("./orama.js") : scope.Orama;
  // Page and section context is not searched: it would retrieve every row of a page that mentions the word once.
  const FIELDS = ["title", "snippet", "body", "symbols"];
  const BOOST = { title: 3, snippet: 2, body: 1, symbols: 4 };

  function symbolTerms(text) {
    const terms = new Set();
    for (const token of text.split(/\s+/)) {
      // Keep shell punctuation that Orama's default English tokenizer drops, such as $# and :w.
      const unwrapped = token.replace(/^[`'"(\[]+|[`'"),;\]]+$/g, "");
      for (const word of [token, unwrapped]) {
        if (word && /[^\p{L}\p{N}]/u.test(word)) {
          terms.add("twsymbol" + Array.from(word, (char) => char.codePointAt(0).toString(16)).join("x"));
        }
      }
    }
    return [...terms];
  }

  // Whole words only, so "reset" does not retrieve "resettable"; these endings are the inflections a word may take.
  function inflections(word) {
    if (!/^[a-z]{3,}$/.test(word)) return [word];
    const forms = new Set([word]);
    const stems = [word];
    if (/[aeiou][bcdfgklmnprt]$/.test(word)) stems.push(word + word.slice(-1));
    if (word.endsWith("e")) stems.push(word.slice(0, -1));
    for (const stem of stems) for (const ending of ["s", "es", "ed", "ing", "er", "est"]) forms.add(stem + ending);
    return [...forms];
  }

  function create(data, normalize) {
    let index;

    function rank(query, tokens) {
      if (!tokens.length || !data.items.length) return new Map();
      if (!index) {
        index = orama.create({ schema: {
          position: "number", title: "string", snippet: "string", body: "string", symbols: "string",
        } });
        orama.insertMultiple(index, data.items.map((item, position) => {
          const title = normalize(item[4]);
          const snippet = normalize(item[5]);
          const body = normalize(item[8] || "");
          return { position, title, snippet, body, symbols: symbolTerms(title + " " + snippet + " " + body).join(" ") };
        }));
      }

      // Orama's exact mode ANDs a multi-word term, so each whole-word form is searched alone and its scores add up.
      const variants = new Set(tokens.flatMap((token) => token.variants.flatMap(inflections)));
      const options = { properties: FIELDS, boost: BOOST, limit: data.items.length };
      const scores = new Map();
      for (const term of [...variants, ...symbolTerms(normalize(query))]) {
        for (const hit of orama.search(index, { ...options, term, exact: true }).hits) {
          scores.set(hit.document.position, (scores.get(hit.document.position) || 0) + hit.score);
        }
      }
      if (!scores.size) {
        const words = tokens.map((token) => token.original).filter((word) => /^[a-z]{5,}$/.test(word));
        if (words.length) {
          for (const hit of orama.search(index, { ...options, term: words.join(" "), tolerance: 2 }).hits) scores.set(hit.document.position, hit.score);
        }
      }
      return scores;
    }

    return { rank };
  }

  if (commonJS) module.exports = { create };
  else scope.TW_ORAMA_SEARCH = { create };
})(typeof window === "undefined" ? globalThis : window);
