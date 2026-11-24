/* Exercise the vendored Orama runtime in Node and in a classic-script browser context. */
"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { norm, createMatcher, createSearch } = require("../_shared/site.js");

const data = {
  syn: [["change", "switch"]],
  items: [
    ["t", 0, 1, "scan", "Inspect media", "Check a file with ffprobe", "Tools", "", "Read metadata about audio and video streams."],
    ["c", 0, 1, "convert", "Convert video", "ffmpeg -n -i input.webm output.mp4", "Tools", ""],
    ["c", 1, 2, "count", "Count arguments", 'printf "%s\\n" "$#"', "Bash Basics", ""],
    ["k", 2, 1, "split", "Switch panes", "Ctrl-w v  Split the window", "Neovim", ""],
    ["k", 2, 1, "write", "Save the file", ":w  Write edits", "Neovim", ""],
  ],
};

function check(runtime) {
  const matcher = createMatcher(data.syn);
  const search = runtime.create(data, norm);
  const rank = (query) => search.rank(query, matcher.query(query));
  assert.equal(rank(" ").size, 0);
  assert.equal(rank("unknownunindexedword").size, 0);
  assert.ok(rank("metadata").has(0), "full body is indexed separately from the snippet");
  assert.ok(rank("ffmepg").has(1), "typo tolerance finds ffmpeg");
  assert.ok(rank("-n").has(1), "command flags are indexed");
  assert.deepEqual(Array.from(rank("$#").keys()), [2], "punctuation-only shell terms are searchable");
  assert.ok(rank("change panes").has(3), "synonym variants retrieve the destination");
  assert.ok(rank("<C-w>v").has(3), "equivalent key notation retrieves the destination");
  assert.equal(Array.from(rank(":w").keys())[0], 4, "literal Vim commands outrank loose matches");
  assert.ok(rank("ffmpeg").get(1) > 0, "rank includes the Orama relevance score");
}

// The site search must retrieve through Orama: spy on the adapter, then use typos the old word matcher could not find.
function checkSiteSearch() {
  const adapter = require("../_shared/orama-search.js");
  const create = adapter.create;
  let created = 0;
  adapter.create = (...args) => { created++; return create(...args); };
  try {
    const small = createSearch({ ...data, files: ["a", "b", "c"] });
    assert.equal(small.search("ffmpg").items[0]?.[3], "convert", "createSearch finds a typo through Orama");
    assert.equal(created, 1, "createSearch builds its Orama index");
    const context = { window: {} };
    vm.runInNewContext(fs.readFileSync(path.join(__dirname, "..", "_shared", "search-index.js"), "utf8"), context);
    const built = context.window.TW_SEARCH;
    const top = (query) => { const it = createSearch(built).search(query).items[0]; return it && built.files[it[1]]; };
    assert.match(top("ffmpg"), /^tools\/ffmpeg\//, "typo ffmpg reaches the FFmpeg page");
    assert.match(top("worktre"), /^m4-worktrees\//, "typo worktre reaches the worktrees module");
  } finally {
    adapter.create = create;
  }
}

checkSiteSearch();
check(require("../_shared/orama-search.js"));
const browser = vm.createContext({ performance });
browser.window = browser;
for (const filename of ["orama.js", "orama-search.js"]) {
  const script = fs.readFileSync(path.join(__dirname, "..", "_shared", filename), "utf8");
  vm.runInContext(script, browser, { filename });
}
check(browser.TW_ORAMA_SEARCH);
console.log("Orama runtime checks passed in Node and a classic-script browser context.");
