/* GOGPT review app front end. Vanilla JS, no modules, no build step. All I/O goes through Store.
   The page shows the edits a research batch staged for the Global Oil and Gas Plant Tracker and
   records one call per edit (accept / hold / reject / suggest) in each staging folder's
   review_log.jsonl. Nothing here, and nothing behind it, writes the GEM database: accepted edits
   go into the actions workbook that is applied by hand in the GEM web form. */
(function () {
  "use strict";
  var T0 = performance.now();

  // ---- Store adapter: the local loopback server ----
  var NOT_YET = "this server cannot record decisions";
  var Store = {
    caps: {decide: false},
    _json: function (r) {
      return r.json().then(function (body) {
        if (!r.ok) throw new Error(body && body.error ? body.error : "HTTP " + r.status);
        return body;
      });
    },
    load: function () { return fetch("/api/data", {cache: "no-store"}).then(Store._json); },
    whoami: function () {
      return fetch("/api/whoami").then(Store._json).then(function (b) {
        if (b.caps) Store.caps = {decide: !!b.caps.decide};
        return b.reviewer;
      });
    },
    _post: function (url, records) {
      if (!Store.caps.decide) return Promise.reject(new Error(NOT_YET));
      return fetch(url, {method: "POST", headers: {"Content-Type": "application/json"},
                         body: JSON.stringify(records)}).then(Store._json).then(function (b) { return b.saved; });
    },
    decide: function (records) { return Store._post("/api/decide", records); },
    item: function (records) { return Store._post("/api/item", records); }
  };
  // the single-file page (build_static.py) embeds the dataset and keeps the log in the browser:
  // static_store.js provides the same interface and runs before this file
  if (window.StaticStore) Store = window.StaticStore;
  var STATIC = Store.mode === "static";
  window.Store = Store;

  // ---- state ----
  var D = null;              // the dataset (review_data.py)
  var ME = "";
  var LINES = [];            // every line, flat; l._i is its index, l._p its plant index
  var ITEMS = [];            // every item, flat; it._p its plant index
  var FS = defaults();       // filter state (what the chips and controls show)
  var S = {
    visible: [],             // plant indexes passing the filter
    pipe: -1,                // index into D.plants
    line: -1,                // selected line index (LINES)
    pin: -1,                 // a plant opened by link that the filters would hide
    shown: [],               // line indexes drawn on the current card, in order
    stay: {},                // line keys decided this session: kept in view even if the filter would drop them
    saving: {},              // line / item keys with a save in flight
    tab: "major",            // the card's tab: "major" | "minor" | "items" | "all"
    igOpen: {}               // item kind -> details open state (survives a re-render; reset per plant)
  };
  var ITEM_BY_KEY = {};
  var LINE_BY_KEY = {};
  // the call vocabulary per item kind: must match review_app/store.py ITEM_CALLS
  var ITEM_CALLS = {concern: ["confirmed", "dismissed", "needs_research"]};
  var OTHER_CALLS = ["noted", "todo", "dismissed"];
  var CALL_HELP = {confirmed: "the concern stands", dismissed: "the concern is closed", needs_research: "goes back to the researcher",
                   noted: "seen, nothing to do", todo: "to do later"};
  var VERB = {accept: "accepted", hold: "held", reject: "rejected", suggest: "suggested"};
  var $ = function (id) { return document.getElementById(id); };
  var LINE_KINDS = ["fill", "change", "delete", "plant", "reverified", "new_row"];
  var ITEM_KINDS = ["concern", "monitor", "entity", "other"];
  var KIND_LABEL = {fill: "fill a blank", change: "change a value", "delete": "clear a value", plant: "plant-wide",
                    reverified: "re-verified", new_row: "new row",
                    concern: "concern", monitor: "monitor", entity: "entity check", other: "other"};
  var DEC = ["undecided", "accept", "hold", "reject", "suggest"];
  // severity (review_data.py): a MAJOR change moves a cell value (fills a blank, changes or clears
  // a value, sets a plant-wide field, adds a row); a MINOR change leaves the value as it is and
  // only adds a Data Source link because the value was checked again and stands.
  var SEV = ["major", "minor"];
  var SEV_LABEL = {major: "major changes", minor: "minor changes"};
  var SEV_TIP = {major: "major change: a cell value moves. A blank is filled, a value is changed or cleared, a plant-wide field is set, or a row is added",
                 minor: "minor change: the value was checked again and stands. Only a Data Source link is added"};
  function sevOf(l) { return l.severity || "major"; }

  function defaults() {
    return {decision: "undecided", kind: "", severity: "", tier: "", dir: "", column: "", q: "", country: "", state: [], by: "", status: false};
  }
  // the tab a plant opens on: its major changes, or the minor ones when it has no major change
  function defaultTab(p) { return p && p.lines.some(function (l) { return sevOf(l) === "major"; }) ? "major" : "minor"; }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"}[c];
    });
  }
  function isItemKind(k) { return ITEM_KINDS.indexOf(k) >= 0; }
  function blankv(v) { return v == null || String(v).trim() === ""; }
  // "batches/us-md/staging" -> "us-md"
  function dirLabel(d) {
    var parts = String(d || "").split("/").filter(Boolean);
    if (parts.length && parts[parts.length - 1] === "staging") parts.pop();
    return parts.length ? parts[parts.length - 1] : String(d || "");
  }
  // "new:<name>" ids mark a plant GEM does not track yet (a discovery candidate on the monitor list)
  function untracked(p) { return !p.pid || p.pid.indexOf("new:") === 0; }
  function tierOf(l) { return l.tier === "high" || l.tier === "medium" || l.tier === "low" ? l.tier : "untiered"; }
  function cur(l) { return l.reviewed && l.decision ? l.decision : null; }
  // drawn grayed once decided (hold stays bright: still open)
  function settled(l) { var d = cur(l); return d === "accept" || d === "reject" || d === "suggest"; }
  function dstate(o) {
    var d = o._item ? o.call : cur(o);
    return d ? d : "undecided";
  }
  var TODAY = (function () {
    try { return new Intl.DateTimeFormat("en-CA", {timeZone: "America/New_York"}).format(new Date()); } catch (e) { return ""; }
  })();
  // today's decisions show HH:MM, older ones their date too (the log keeps every decision ever made)
  function timeOf(iso) {
    var s = String(iso || "").replace("T", " ");
    return !TODAY || s.slice(0, 10) === TODAY ? s.slice(11, 16) : s.slice(0, 16);
  }
  function decisionText(l) {
    if (l.reviewed && l.decision === "suggest") {
      return "suggested: " + (blankv(l.suggested_value) ? "(note only)" : l.suggested_value) + " by " + (l.decided_by || "?") + " " + timeOf(l.decided_at) +
        (blankv(l.decision_note) ? "" : ". " + l.decision_note);
    }
    if (l.reviewed && l.decision) return (VERB[l.decision] || l.decision) + " by " + (l.decided_by || "?") + " " + timeOf(l.decided_at);
    return "";
  }
  function unitOf(p, id) {
    for (var i = 0; i < p.units.length; i++) if (p.units[i].gem_unit_id === id) return p.units[i];
    return null;
  }
  function unitText(u, id) {
    if (!u) return id ? "unit " + id : "";
    return "unit " + (u.unit_name ? u.unit_name + " (" + u.gem_unit_id + ")" : u.gem_unit_id);
  }
  // where on the plant a line lands: "unit F701 (G100000401771)", "plant-wide (4 units)", "new row"
  function rowLabel(l) {
    if (l.kind === "new_row") return "new row";
    var p = D.plants[l._p];
    if (l.kind === "plant") {
      var n = 1 + (l.sibling_unit_ids || []).length;
      return "plant-wide" + (n > 1 ? " (" + n + " units)" : "");
    }
    return unitText(unitOf(p, l.gem_unit_id), l.gem_unit_id);
  }

  // ---- theme ----
  // theme = a palette (dropdown; "" = the default look) x a mode (light / dark button; unset = follow the system).
  function initTheme() {
    var root = document.documentElement, pick = $("theme-pick"), mq = matchMedia("(prefers-color-scheme: dark)");
    var pal = "", mode = "";
    function store(k, v) { try { if (v) localStorage.setItem(k, v); else localStorage.removeItem(k); } catch (e) { /* ignore */ } }
    function eff() { return mode || (mq.matches ? "dark" : "light"); }
    function apply() {
      if (!pal && !mode) root.removeAttribute("data-theme");
      else root.setAttribute("data-theme", pal ? pal + "-" + eff() : mode);
      pick.value = pal;
    }
    try {
      pal = localStorage.getItem("review-palette") || "";
      mode = localStorage.getItem("review-mode") || "";
    } catch (e) { /* storage blocked: follow the system theme */ }
    apply();
    pick.onchange = function () { pal = this.value; store("review-palette", pal); apply(); };
    $("theme").onclick = function () { mode = eff() === "dark" ? "light" : "dark"; store("review-mode", mode); apply(); };
    if (mq.addEventListener) mq.addEventListener("change", function () { if (!mode) apply(); });
  }

  // ---- derived data, once per load ----
  function prepare() {
    LINES = []; ITEMS = []; LINE_BY_KEY = {}; ITEM_BY_KEY = {};
    D.plants.forEach(function (p, pi) {
      p.units = p.units || [];
      p.items = (p.items || []).filter(function (it) { return isItemKind(it.kind); });
      p.items.forEach(function (it) {
        it._item = true; it._p = pi; it._i = ITEMS.length; ITEM_BY_KEY[it.key] = it;
        ITEMS.push(it);
      });
      p.lines = p.lines || [];
      p.lines.forEach(function (l) {
        l._p = pi; l._i = LINES.length; LINE_BY_KEY[l.key] = l;
        LINES.push(l);
      });
      p._hay = [p.name, p.pid, p.state].concat(p.units.map(function (u) { return u.gem_unit_id + " " + u.unit_name; }))
        .join(" ").toLowerCase();
    });
  }

  // ---- filters ----
  // One matcher for lines and items. `skip` names a facet to ignore (for faceted chip counts).
  function match(o, p, fs, skip, q) {
    var item = !!o._item;
    if (skip !== "kind") {
      if (fs.kind) { if (o.kind !== fs.kind) return false; }
      else if (item) return false;
    }
    if (skip !== "decision" && fs.decision && dstate(o) !== fs.decision && !(!item && S.stay[o.key])) return false;
    if (skip !== "severity" && fs.severity && (item || sevOf(o) !== fs.severity)) return false;
    if (skip !== "tier" && fs.tier && (item || tierOf(o) !== fs.tier)) return false;
    if (fs.dir && o.dir !== fs.dir) return false;
    if (fs.column && (item || o.column !== fs.column)) return false;
    if (fs.status && (item || o.column !== "Status")) return false;
    if (fs.by && (o.reviewed ? o.decided_by : "") !== fs.by) return false;
    if (skip !== "country" && fs.country && p.country !== fs.country) return false;
    if (skip !== "state" && fs.state.length && fs.state.indexOf(p.state) < 0) return false;
    if (q && p._hay.indexOf(q) < 0) return false;
    return true;
  }
  function pipeMatches(p) {
    var q = FS.q.trim().toLowerCase(), n = 0, todo = 0, ni = 0, tsev = {major: 0, minor: 0};
    p.lines.forEach(function (l) {
      if (!match(l, p, FS, null, q)) return;
      n++;
      if (!cur(l)) { todo++; tsev[sevOf(l)]++; }
    });
    p.items.forEach(function (it) { if (match(it, p, FS, null, q)) ni++; });
    p._n = n; p._todo = todo; p._ni = ni; p._tsev = tsev;
    return n + ni;
  }
  function refilter(keep) {
    var sel = D.plants[S.pipe];
    S.visible = [];
    var nl = 0, ni = 0;
    D.plants.forEach(function (p, i) {
      var m = pipeMatches(p);
      nl += p._n; ni += p._ni;
      if (m || i === S.pin) S.visible.push(i);
    });
    S.countText = nl + " change" + (nl === 1 ? "" : "s") + (ni ? " + " + ni + " item" + (ni === 1 ? "" : "s") : "") +
      " on " + S.visible.length + " plant" + (S.visible.length === 1 ? "" : "s");
    if (S.visible.indexOf(S.pipe) < 0) S.pipe = S.visible.length ? S.visible[0] : -1;
    if (D.plants[S.pipe] !== sel) { S.line = -1; S.tab = defaultTab(D.plants[S.pipe]); S.igOpen = {}; }
    renderChips();
    renderActive();
    renderProgress();
    renderQueue();
    renderCard();
    if (keep !== true) writeRoute(false);
  }
  function facetCounts(facet, values) {
    var q = FS.q.trim().toLowerCase(), c = {};
    values.forEach(function (v) { c[v] = 0; });
    function tally(o, p, v) { if (match(o, p, FS, facet, q) && v in c) c[v]++; }
    D.plants.forEach(function (p) {
      p.lines.forEach(function (l) {
        tally(l, p, facet === "decision" ? dstate(l) : facet === "kind" ? l.kind : facet === "severity" ? sevOf(l) : tierOf(l));
      });
      if (facet === "kind" || (facet === "decision" && isItemKind(FS.kind))) {
        p.items.forEach(function (it) { tally(it, p, facet === "kind" ? it.kind : dstate(it)); });
      }
    });
    return c;
  }
  // a facet dropdown: "any" plus one option per value with its live count ("accept (3)")
  function facetSelect(id, facet, values, labels, totals) {
    var counts = facetCounts(facet, values), h = '<option value="">any</option>';
    values.forEach(function (v) {
      if (totals && !totals[v] && FS[facet] !== v) return;      // a kind this dataset does not have
      h += '<option value="' + v + '"' + (FS[facet] === v ? " selected" : "") + ">" + esc(labels[v] || v) + " (" + counts[v] + ")</option>";
    });
    var s = $(id);
    s.innerHTML = h;
    s.value = FS[facet];
  }
  function allStates() { return (D.scope && D.scope.states) || []; }
  // the states of the picked country; none while no country is picked (the state box only shows after a country)
  function states() {
    if (!FS.country) return allStates();
    return allStates().filter(function (k) { return D.plants.some(function (p) { return p.state === k && p.country === FS.country; }); });
  }
  function countries() { return uniq(D.plants.map(function (p) { return p.country; })); }
  // country picker: one choice, with the live line + item count under the other filters
  function renderCountries() {
    var sel = $("f-country"), all = countries(), q = FS.q.trim().toLowerCase(), c = {};
    $("f-country-wrap").hidden = all.length < 2;
    all.forEach(function (k) { c[k] = 0; });
    D.plants.forEach(function (p) {
      var n = 0;
      p.lines.forEach(function (l) { if (match(l, p, FS, "country", q)) n++; });
      p.items.forEach(function (it) { if (match(it, p, FS, "country", q)) n++; });
      if (p.country in c) c[p.country] += n;
    });
    sel.innerHTML = '<option value="">all</option>' + all.map(function (k) {
      return '<option value="' + esc(k) + '">' + esc(k) + " (" + c[k] + ")</option>";
    }).join("");
    sel.value = FS.country;
  }
  var NO_STATE = "(none)";   // FS.state sentinel: every box unticked, so nothing matches (empty = no filter)
  // the batch states as checkboxes (any ticked state matches; none ticked = every state), each
  // with its live line + item count under the other filters
  function renderStates() {
    var box = $("f-state"), all = states();
    renderScope();
    box.hidden = !FS.country || all.length < 2;
    if (box.hidden) return;
    var q = FS.q.trim().toLowerCase(), c = {};
    all.forEach(function (k) { c[k] = 0; });
    D.plants.forEach(function (p) {
      var n = 0;
      p.lines.forEach(function (l) { if (match(l, p, FS, "state", q)) n++; });
      p.items.forEach(function (it) { if (match(it, p, FS, "state", q)) n++; });
      if (p.state in c) c[p.state] += n;
    });
    var was = box.querySelector("details"), open = was && was.open, n = FS.state.length;
    box.innerHTML = '<details class="cdrop"' + (open ? " open" : "") + '><summary>state</summary><div class="cmenu"><button type="button" class="ctoggle"></button>' + all.map(function (k) {
      return '<label class="check"><input type="checkbox" value="' + esc(k) + '"' + (!n || FS.state.indexOf(k) >= 0 ? " checked" : "") +
        "> " + esc(k) + " (" + c[k] + ")</label>";
    }).join("") + "</div></details>";
    toggleLabel();
  }
  // header: each batch state as a box with its plant count
  function renderScope() {
    var list = countries();
    if (FS.country) list = list.filter(function (k) { return k === FS.country; });   // only the selected one
    $("scope").innerHTML = list.map(function (k) {
      var n = D.plants.filter(function (p) { return p.country === k; }).length;
      return '<span class="cbox" data-tip="' + esc(k) + ": " + n + " plant" + (n === 1 ? "" : "s") + ' in this review">' + esc(k) + "</span>";
    }).join("");
  }
  function toggleLabel() {
    var b = document.querySelector("#f-state .ctoggle"); if (!b) return;
    var boxes = Array.prototype.slice.call(document.querySelectorAll("#f-state .cmenu input"));
    b.textContent = boxes.length && boxes.every(function (i) { return i.checked; }) ? "deselect all" : "select all";
  }
  function toggleStates() {
    var all = states(), sel = FS.state.length ? all.filter(function (k) { return FS.state.indexOf(k) >= 0; }) : all.slice();
    var allOn = sel.length === all.length;
    FS.state = allOn ? [NO_STATE] : [];
    changed();
  }
  document.addEventListener("click", function (e) {
    Array.prototype.forEach.call(document.querySelectorAll("#f-state details"), function (d) {
      if (d.open && !d.contains(e.target)) d.open = false;
    });
  });
  // everyone with a live decision in this dataset
  function fillBy() {
    var seen = {}, s = $("f-by");
    LINES.concat(ITEMS).forEach(function (o) { if (o.reviewed && o.decided_by) seen[o.decided_by] = (seen[o.decided_by] || 0) + 1; });
    if (FS.by && !seen[FS.by]) seen[FS.by] = 0;
    s.innerHTML = '<option value="">anyone</option>' + Object.keys(seen).sort().map(function (k) {
      return '<option value="' + esc(k) + '">' + esc(k) + " (" + seen[k] + ")</option>";
    }).join("");
    s.value = FS.by;
  }
  function renderChips() {
    renderCountries();
    renderStates();
    fillBy();
    facetSelect("f-decision", "decision", DEC, {});
    var tot = {};
    LINES.forEach(function (l) { tot[l.kind] = 1; });
    ITEMS.forEach(function (i) { tot[i.kind] = 1; });
    facetSelect("f-kind", "kind", LINE_KINDS.concat(ITEM_KINDS), KIND_LABEL, tot);
    facetSelect("f-severity", "severity", SEV, SEV_LABEL);
    var tt = {};
    LINES.forEach(function (l) { tt[tierOf(l)] = 1; });
    facetSelect("f-tier", "tier", ["high", "medium", "low", "untiered"], {untiered: "unrated"}, tt);
  }
  function fillSelect(id, values) {
    var s = $(id);
    values.forEach(function (v) { var o = document.createElement("option"); o.value = v; o.textContent = id === "f-dir" ? dirLabel(v) : v; s.appendChild(o); });
  }
  function uniq(arr) { return arr.filter(function (x, i) { return x && arr.indexOf(x) === i; }).sort(); }
  function fillFilters() {
    ["f-column", "f-dir"].forEach(function (id) { $(id).innerHTML = '<option value="">any</option>'; });
    var cols = uniq(LINES.map(function (l) { return l.column; }));
    cols.sort(function (a, b) {
      var ia = D.columns.indexOf(a), ib = D.columns.indexOf(b);
      return (ia < 0 ? 9999 : ia) - (ib < 0 ? 9999 : ib);
    });
    fillSelect("f-column", cols);
    var LISTED = LINES.concat(ITEMS);
    fillSelect("f-dir", D.dirs.filter(function (d) { return LISTED.some(function (o) { return o.dir === d; }); }));
  }
  function initFilters() {
    fillFilters();
    $("filters").addEventListener("click", function (e) {
      var c = e.target.closest("button[data-clear]");
      if (c) { clearOne(c.getAttribute("data-clear")); changed(); }
    });
    ["decision", "kind", "severity", "tier", "column", "dir"].forEach(function (f) {
      $("f-" + f).onchange = function () { FS[f] = this.value; changed(); };
    });
    $("f-status").onchange = function () { FS.status = this.checked; changed(); };
    $("f-country").onchange = function () { FS.country = this.value; FS.state = []; changed(); };
    $("f-state").onclick = function (e) { if (e.target.classList.contains("ctoggle")) { e.stopPropagation(); toggleStates(); } };
    $("f-state").onchange = function () {
      FS.state = Array.prototype.map.call(this.querySelectorAll("input[type=checkbox]:checked"), function (i) { return i.value; });
      if (FS.state.length === this.querySelectorAll("input[type=checkbox]").length) FS.state = [];
      else if (!FS.state.length) FS.state = [NO_STATE];   // all ticked = no filter
      changed();
    };
    // "decided by" only ever matches decided lines: leave the undecided-only default
    $("f-by").onchange = function () { FS.by = this.value; if (FS.by && FS.decision === "undecided") FS.decision = ""; changed(); };
    $("f-q").oninput = function () { FS.q = this.value; changed(true); };
    $("f-more").onclick = function () { toggleMore(); };
    $("f-reset").onclick = function () { FS = defaults(); syncControls(); changed(); };
  }
  function changed(replace) { S.pin = -1; S.stay = {}; refilter(true); writeRoute(replace === true); }
  function clearOne(id) {
    var d = defaults();
    FS[id] = d[id];
    syncControls();
  }
  function toggleMore(open) {
    var box = $("more-filters");
    box.hidden = open == null ? !box.hidden : !open;
    $("f-more").setAttribute("aria-expanded", String(!box.hidden));
    renderActive();
  }
  function syncControls() {
    ["column", "dir"].forEach(function (f) {
      $("f-" + f).value = FS[f];
      if ($("f-" + f).value !== FS[f]) { FS[f] = ""; $("f-" + f).value = ""; }
    });
    $("f-country").value = FS.country;
    if ($("f-country").value !== FS.country) FS.country = "";
    $("f-status").checked = FS.status;
    fillBy();
    $("f-q").value = FS.q;
  }
  // Every filter that is set is a removable chip, so a control tucked behind "more filters"
  // never filters silently.
  function renderActive() {
    var chips = [], n = 0;
    function chip(id, text, hidden) {
      chips.push('<span class="chip on">' + esc(text) + ' <button type="button" data-clear="' + id +
        '" aria-label="clear ' + esc(text) + '">&times;</button></span>');
      if (hidden) n++;
    }
    if (FS.column) chip("column", "column: " + FS.column, true);
    if (FS.dir) chip("dir", "batch: " + dirLabel(FS.dir), true);
    if (FS.by) chip("by", "decided by: " + FS.by, true);
    if (FS.status) chip("status", "status changes only", true);
    $("active-filters").innerHTML = chips.join(" ");
    $("active-filters").hidden = !chips.length;
    $("f-more").textContent = ($("more-filters").hidden ? "more filters" : "fewer filters") + (n ? " (" + n + ")" : "");
  }
  function renderProgress() {
    var total = 0, done = 0, sev = {major: {done: 0, total: 0}, minor: {done: 0, total: 0}};
    LINES.forEach(function (l) {
      total++; sev[sevOf(l)].total++; if (cur(l)) { done++; sev[sevOf(l)].done++; }
    });
    S.progress = {done: done, total: total, sev: sev};
  }
  function showProgress() {
    var dlg = $("dialog"), g = S.progress || {done: 0, total: 0, sev: {major: {done: 0, total: 0}, minor: {done: 0, total: 0}}};
    var items = ITEMS.length, calls = ITEMS.filter(function (it) { return it.call && it.reviewed; }).length;
    dlg.setAttribute("data-kind", "progress");
    dlg.innerHTML = "<h3>progress</h3><p>" + esc(S.countText || "") + " in view</p>" +
      '<div class="progress" aria-hidden="true"><div id="progress-bar" style="width:' + (g.total ? 100 * g.done / g.total : 0) + '%"></div></div>' +
      "<p>" + g.done + " of " + g.total + " changes decided &middot; major " + g.sev.major.done + " of " + g.sev.major.total +
      " &middot; minor " + g.sev.minor.done + " of " + g.sev.minor.total + "</p>" +
      "<p>" + calls + " of " + items + " items have a call</p>" +
      '<div class="actions"><button type="button" id="dlg-close">close</button></div>';
    $("dlg-close").onclick = function () { dlg.close(); };
    dlg.showModal();
  }

  // ---- queue ----
  function unitNames(p) {
    return p.units.map(function (u) { return String(u.unit_name || u.gem_unit_id || "").trim(); }).filter(Boolean);
  }
  function renderQueue() {
    var h = [];
    S.visible.forEach(function (i) {
      var p = D.plants[i];
      var dots = {};
      p.lines.forEach(function (l) { dots[tierOf(l)] = 1; });
      var dd = ["high", "medium", "low"].filter(function (t) { return dots[t]; })
        .map(function (t) { return '<span class="dot ' + t + '" data-tip="' + t + ' confidence" role="img" aria-label="' + t + ' confidence"></span>'; }).join("");
      var ts = p._tsev || {}, parts = SEV.filter(function (s) { return ts[s]; }).map(function (s) { return ts[s] + " " + s; });
      var badge = p._todo ? '<span class="n todo">' + (parts.length ? parts.join(" &middot; ") : p._todo) + " to decide</span>"
        : (p._n ? '<span class="n">' + p._n + " &middot; done</span>" : (p._ni ? '<span class="n">' + p._ni + " item" + (p._ni === 1 ? "" : "s") + "</span>" : '<span class="n"></span>'));
      var un = unitNames(p);
      var where = p.statewide ? "statewide" : (p.units.length + " unit" + (p.units.length === 1 ? "" : "s"));
      h.push('<li data-i="' + i + '"' + (i === S.pipe ? ' class="sel"' : "") + '><div class="pname">' + esc(p.name || "(no name)") +
        (un.length ? ' <span class="pseg">' + esc(un[0]) + (un.length > 1 ? " +" + (un.length - 1) : "") + "</span>" : "") +
        '</div><div class="pmeta"><span>' + esc(p.statewide ? p.state : (untracked(p) ? "not in GEM yet" : p.pid)) + " &middot; " + esc(where) +
        '</span><span class="grow"></span>' + badge + '</div>' + (dd ? '<div class="dots">' + dd + "</div>" : "") + "</li>");
    });
    $("pipes").innerHTML = h.join("");
  }
  function selectPipe(i, lineIdx) {
    if (S.pipe !== i) S.igOpen = {};          // item groups collapse again on a new plant
    S.pipe = i;
    S.tab = defaultTab(D.plants[i]);
    S.line = lineIdx == null ? -1 : lineIdx;
    if (S.line >= 0 && LINES[S.line] && S.tab !== sevOf(LINES[S.line])) S.tab = sevOf(LINES[S.line]);
    var prev = $("pipes").querySelector("li.sel");
    if (prev) prev.classList.remove("sel");
    var li = $("pipes").querySelector('li[data-i="' + i + '"]');
    if (li) { li.classList.add("sel"); li.scrollIntoView({block: "nearest"}); }
    renderCard();
    writeRoute(true);
  }

  // ---- card pieces ----
  function urlLink(u, long) {
    var t = u.length > (long || 78) ? u.slice(0, (long || 78) - 1) + "…" : u;
    if (!/^https?:\/\//i.test(u)) return esc(u);
    return '<a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(t) + " ↗</a>";
  }
  function asList(v) {
    if (Array.isArray(v)) return v.filter(Boolean);
    return String(v || "").split(/,\s*(?=https?:\/\/)|\n+/).map(function (s) { return s.trim(); }).filter(Boolean);
  }
  // `tip` shows in the #tip popover on hover / keyboard focus; `note` (optional) scrolls under it when long
  function chip(text, cls, tip, note) {
    return '<span class="chip' + (cls ? " " + cls : "") + '"' + (tip ? ' tabindex="0"' + tipAttrs(tip, note) : "") + ">" + esc(text) + "</span>";
  }
  function tipAttrs(tip, note) {
    return ' data-tip="' + esc(tip) + '"' + (note ? ' data-tip-note="' + esc(note) + '"' : "") +
      ' aria-description="' + esc(tip + (note ? ". note: " + note : "")) + '"';
  }
  var TIER_TIP = {high: "green: one fully checked source (a status change needs two independent publishers)",
                  medium: "yellow: a single source on a status change, or a source that only partly supports the value",
                  low: "red: a single weak or unchecked source"};
  function tierChip(l) {
    var t = tierOf(l);
    return chip(t === "untiered" ? "unrated" : t, t === "untiered" ? "" : t,
      t === "untiered" ? "no confidence rating on this record: defaults to hold" : TIER_TIP[t]);
  }
  function sevChip(l) {
    var s = sevOf(l);
    var what = l.reverified ? "checked, stands" : (KIND_LABEL[l.kind] || l.kind);
    return chip(s + " · " + what, s, SEV_TIP[s]);
  }
  // One mark per proposed URL: ✓ when it loads, states the value and names the plant; else the failed checks.
  function vmark(u, l) {
    var v = (l.verifications || {})[u];
    if (!v) return chip("unchecked", "", "no verification record for this link: url_verifier.py did not check it at staging, so whether it loads, states the value or names the plant is unknown");
    var bad = [];
    if (!v.ok) bad.push("load");
    if (!v.contains_value) bad.push("value");
    if (!v.name_found) bad.push("name");
    var tip = "link checks:\n" +
      (v.ok ? "✓" : "✗") + " loads: the page fetched and its text is readable\n" +
      (v.contains_value ? "✓" : "✗") + " states value: the proposed value is on the page\n" +
      (v.name_found ? "✓" : "✗") + " names plant: the plant's name is on the page";
    return bad.length ? chip("✗ " + bad.join(", "), "bad", tip, v.note) : chip("✓", "ok", tip, v.note);
  }
  // a URL shortened for the table: host + path, decoded, Wayback shown as "archive › <origin>"
  function shortUrl(u) {
    var s = String(u);
    try { s = decodeURI(s); } catch (e) { /* keep as is */ }
    s = s.replace(/^https?:\/\/(www\.)?/i, "");
    var wb = s.match(/^web\.archive\.org\/web\/\d+[a-z_]*\/(?:https?:\/\/)?(?:www\.)?(.*)$/i);
    if (wb) s = "archive › " + wb[1];
    s = s.replace(/\/$/, "");
    return s.length > 64 ? s.slice(0, 63) + "…" : s;
  }
  function shortLink(u) {
    if (!/^https?:\/\//i.test(u)) return esc(u);
    return '<a href="' + esc(u) + '" target="_blank" rel="noopener">' + esc(shortUrl(u)) + "</a>";
  }
  function tag(t) { return t ? '<span class="tag tag-' + t + '">' + t + "</span>" : ""; }
  // one value row: field | now | proposed | tag
  function valueRow(c, was, now, reverified) {
    var wasH = blankv(was) ? "" : "<span>" + esc(was) + "</span>";
    var nowH, t = "", same = false;
    if (!blankv(was) && String(was).trim() === String(now).trim()) { nowH = wasH; same = true; t = reverified ? "re-verified" : ""; }
    else if (blankv(now)) { nowH = '<span class="blank">(clear)</span>'; t = "clear"; }
    else { t = blankv(was) ? "fill" : "change"; nowH = '<span class="newv c-' + t + '">' + esc(now) + "</span>"; }
    return '<tr class="' + (same ? "same" : "") + '"><td class="f">' + esc(c) + "</td><td>" + wasH + "</td><td>" + nowH + '</td><td class="t">' + tag(t) + "</td></tr>";
  }
  function valueRows(l) {
    var pv = l.proposed_values || {}, cols = Object.keys(pv), curv = l.current || {};
    if (!cols.length) cols = l.columns || [l.column];
    return cols.map(function (c) {
      if (!(c in pv) && blankv(curv[c])) return "";
      return valueRow(c, curv[c], c in pv ? pv[c] : curv[c], l.reverified);
    }).join("");
  }
  // a plant-wide line: the same value lands on every unit row of the plant
  function siblingRow(l) {
    var ids = l.sibling_unit_ids || [];
    if (!ids.length) return "";
    var p = D.plants[l._p], sc = l.sibling_current || {};
    var txt = ids.map(function (id) {
      var u = unitOf(p, id), nm = u && u.unit_name ? u.unit_name : id;
      return nm + (blankv(sc[id]) ? " (blank now)" : " (now " + sc[id] + ")");
    }).join(", ");
    return '<tr class="note"><td></td><td colspan="3"><div class="faint">the same edit lands on the other unit rows of this plant: ' + esc(txt) + "</div></td></tr>";
  }
  // the Data Source row: the cell now, and the cell it would be. Links are ADDED next to the ones
  // already there (the manual's merge rule: a Data Source is never replaced or deleted).
  function refRow(l) {
    var col = l.ref_col || "Data Source";
    var curr = asList(l.current_ref), prop = asList(l.proposed_refs);
    var added = prop.filter(function (u) { return curr.indexOf(u) < 0; });
    var nowH = curr.length ? "<ul>" + curr.map(function (u) { return "<li>" + shortLink(u) + "</li>"; }).join("") + "</ul>" : "";
    var propH, t;
    if (!prop.length) { propH = '<span class="muted">no link proposed' + (l.kind === "delete" ? " (the value is cleared; the links stay)" : "") + "</span>"; t = ""; }
    else {
      t = !curr.length ? "fill" : (added.length ? "add" : "");
      propH = "<ul>" + curr.map(function (u) { return '<li class="kept">' + shortLink(u) + "</li>"; }).join("") +
        added.map(function (u) { return '<li><span class="newref c-fill">' + shortLink(u) + "</span> " + vmark(u, l) + "</li>"; }).join("") + "</ul>";
    }
    return '<tr class="ref"><td class="f">' + esc(col) + "</td><td>" + nowH + "</td><td>" + propH + '</td><td class="t">' + tag(t) + "</td></tr>";
  }
  function pairTable(rows) {
    return '<table class="pair"><thead><tr><th></th><th>now</th><th>proposed</th><th></th></tr></thead><tbody>' + rows + "</tbody></table>";
  }
  function lineBody(l) {
    if (l.kind === "new_row") return newRowBody(l);
    var h = pairTable(valueRows(l) + siblingRow(l) + refRow(l));
    var facts = [];
    if (l.column === "Status") {
      if ((l.publishers || 0) < 2) facts.push(chip("single source", "single", "fewer than two independent publishers: a status change is green only with two or more. One source makes it yellow"));
      else facts.push(chip(l.publishers + " publishers"));
    }
    if (l.independent) facts.push(chip("second source", "ok", "a second independent source was recorded for this value"));
    return h + (facts.length ? '<div class="facts">' + facts.join(" ") + "</div>" : "");
  }
  function newRowTable(vals, refs, l) {
    vals = vals || {}; refs = refs || {};
    var tr = Object.keys(vals).filter(function (c) { return !blankv(vals[c]); }).map(function (c) {
      return "<tr><td>" + esc(c) + "</td><td>" + esc(vals[c]) + "</td></tr>";
    });
    Object.keys(refs).forEach(function (c) {
      var us = asList(refs[c]);
      if (!us.length) return;
      tr.push("<tr><td>" + esc(c) + "</td><td>" + us.map(function (u) { return urlLink(u) + " " + vmark(u, l); }).join("<br>") + "</td></tr>");
    });
    return '<table class="rowdata">' + tr.join("") + "</table>";
  }
  function newRowBody(l) {
    var units = l.units || [];
    var h = '<div class="row1">' + chip(l.lane === "newunits" ? "new unit on a tracked plant" : "new plant", "newrow") +
      ' <span class="faint">' + (l.lane === "newunits" ? "a unit row to add under a plant GEM already tracks" :
        "a plant GEM does not track yet; every field below is new" + (units.length ? ", with " + units.length + " unit row" + (units.length === 1 ? "" : "s") + " to add under it. One call covers the plant and its units" : "")) + "</span></div>";
    h += newRowTable(l.proposed_values, l.refs_by_col, l);
    // a new plant's unit rows: each one its own small table under the plant fields
    units.forEach(function (u) {
      h += '<div class="row1 newunit"><span class="col">unit ' + esc(u.unit_name || "(unnamed)") + "</span></div>" + newRowTable(u.fields, u.refs_by_col, l);
      if (u.action) h += '<div class="dtxt"><span class="k">what to do in the GEM form:</span> ' + esc(u.action) + "</div>";
      if (u.notes) h += '<div class="dtxt"><span class="k">researcher notes:</span> ' + esc(u.notes) + "</div>";
    });
    return h;
  }
  function detailsHtml(l) {
    var d = [];
    if (l.action) d.push('<div class="dtxt"><span class="k">what to do in the GEM form:</span> ' + esc(l.action) + "</div>");
    if (l.notes) d.push('<div class="dtxt"><span class="k">researcher notes:</span> ' + esc(l.notes) + "</div>");
    var vs = l.verifications || {};
    Object.keys(vs).forEach(function (u) {
      if (vs[u] && vs[u].note) d.push('<div class="dtxt"><span class="k">' + esc(u) + ":</span> " + esc(vs[u].note) + "</div>");
    });
    var misc = ["batch " + dirLabel(l.dir), "default " + (l.default || "hold"), "record " + (l.record_id || "?")];
    if (l.source_language && l.source_language !== "en") misc.push("source language " + l.source_language);
    if (l.lane) misc.push("lane " + l.lane);
    d.push('<div class="dtxt"><span class="k">record:</span> ' + esc(misc.join(" · ")) + "</div>");
    return '<details data-more><summary>notes &amp; record</summary>' + d.join("") + "</details>";
  }
  function lineHtml(l) {
    var chips = [];
    if (l.kind === "new_row") chips.push(chip(KIND_LABEL.new_row, "newrow"));
    if (l.kind === "plant") chips.push(chip("plant-wide", "oo", "a plant-level field: the export repeats it on every unit row, so the edit lands on every unit row of this plant"));
    chips.push(tierChip(l));
    chips.push(sevChip(l));
    var title = l.kind === "new_row" ? ((l.proposed_values || {})["Plant name"] || (l.proposed_values || {})["Unit name"] || l.unit_name || l.plant_name || "new row") : (l.column || "");
    var h = '<div class="row1"><span class="col">' + esc(title) + "</span> " + chips.join(" ") +
      '<span class="where">' + esc(rowLabel(l)) + "</span></div>";
    h += lineBody(l);
    var dis = !Store.caps.decide;
    h += '<div class="controls">' + [["accept", "a"], ["hold", "h"], ["reject", "r"]].map(function (b) {
      return '<button type="button" class="b-' + b[0] + '" data-decide="' + b[0] + '"' +
        (dis ? tipAttrs(NOT_YET) + ' aria-disabled="true"' : "") +
        ' aria-pressed="' + (cur(l) === b[0]) + '">' + b[0] + "</button>";
    }).join("") + '<button type="button" class="b-suggest" data-suggest="1"' + (dis ? ' aria-disabled="true"' + tipAttrs(NOT_YET) : "") +
      ' aria-pressed="' + (cur(l) === "suggest") + '">suggest</button>' + (cur(l) ? '<button type="button" class="ghost" data-undo="1">undo</button>' : "") +
      '<span class="dstat" id="dstat-' + l._i + '" role="status">' + esc(decisionText(l)) + "</span></div>";
    h += detailsHtml(l);
    return h;
  }

  // ---- items ----
  var HIDE = {call_note: 1, decided_by: 1, decided_at: 1, key: 1, dir: 1, record_id: 1, call: 1, reviewed: 1, kind: 1,
              gem_unit_id: 1, unit_name: 1, links: 1, verifications: 1, _item: 1, _p: 1, _i: 1};
  var BODY = ["notes", "recommendation", "reason", "lookup_result"];
  var CONCERN_ISSUE = {unverified_value: "a value could not be checked against its source", conflict: "two sources disagree",
                       duplicate: "this may duplicate another row", missing_source: "a value has no source link",
                       capacity: "the capacity figure needs a closer look", status: "the status needs a closer look",
                       ownership: "the owner or operator needs a closer look"};
  function concernHead(it) {
    var t = String(it.concern_type || "concern");
    return CONCERN_ISSUE[t] || t.replace(/_/g, " ");
  }
  function itemHead(it) {
    switch (it.kind) {
      case "concern": return concernHead(it);
      case "monitor": return (it.item || "watch this plant") + (it.recheck_by ? " (check again by " + it.recheck_by + ")" : "");
      case "entity": return (it.entity_name || "entity") + (it.role ? " as " + it.role : "");
      default: return it.title || it.kind;
    }
  }
  function itemBody(it) {
    var h = "", used = {};
    BODY.forEach(function (k) {
      var t = it[k];
      if (blankv(t) || typeof t !== "string") return;
      var cut = t.length > 700;
      h += '<div class="body">' + (k === "notes" ? "" : "<b>" + esc(k.replace(/_/g, " ")) + ":</b> ") + esc(cut ? t.slice(0, 700) + "…" : t) + "</div>";
      if (!cut) used[k] = 1;
    });
    var links = asList(it.links);
    if (links.length) {
      h += '<div class="body">' + links.map(function (u) {
        var v = (it.verifications || {})[u];
        return urlLink(u) + (v ? " " + vmark(u, it) : "");
      }).join("<br>") + "</div>";
    }
    return {html: h, used: used};
  }
  function fieldRows(it, used) {
    var rows = [];
    Object.keys(it).forEach(function (k) {
      if (HIDE[k] || used[k] || k.charAt(0) === "_") return;
      var v = it[k];
      if (v == null || v === "" || (Array.isArray(v) && !v.length)) return;
      var t;
      if (Array.isArray(v) && v.every(function (x) { return typeof x === "string"; })) t = v.map(function (x) { return /^https?:/.test(x) ? urlLink(x) : esc(x); }).join("<br>");
      else if (typeof v === "object") t = esc(JSON.stringify(v).slice(0, 400));
      else t = /^https?:\/\//.test(String(v)) ? urlLink(String(v)) : esc(v);
      rows.push("<tr><td>" + esc(k.replace(/_/g, " ")) + "</td><td>" + t + "</td></tr>");
    });
    return rows;
  }
  function itemHtml(it) {
    var b = itemBody(it), rows = fieldRows(it, b.used), p = D.plants[it._p];
    var where = it.gem_unit_id ? unitText(unitOf(p, it.gem_unit_id), it.gem_unit_id) : "plant";
    var h = '<div class="item' + (it.call && it.reviewed ? " done" : "") + '"><div class="row1">' + chip(KIND_LABEL[it.kind] || it.kind, "") +
      " <b>" + esc(itemHead(it)) + "</b>" + '<span class="where">' + esc(where) + "</span></div>";
    h += b.html;
    if (rows.length) h += "<details><summary>all fields</summary><table class=\"rowdata\">" + rows.join("") + "</table></details>";
    return h + itemControls(it) + "</div>";
  }
  function itemVocab(it) { return ITEM_CALLS[it.kind] || OTHER_CALLS; }
  function itemStat(it) {
    return it.call && it.reviewed ? (it.call.replace("_", " ") + " by " + (it.decided_by || "?") + " " + timeOf(it.decided_at)) : "";
  }
  function itemControls(it) {
    var dis = !Store.caps.decide, v = itemVocab(it);
    var opts = '<option value="">no call</option>' + v.map(function (c) {
      return '<option value="' + c + '"' + (it.call === c ? " selected" : "") + ' title="' + esc(CALL_HELP[c] || "") + '">' + c.replace("_", " ") + "</option>";
    }).join("");
    var hint = it.kind === "concern" ? "confirmed: the concern stands and goes into the evidence file. dismissed: closed, nothing to do. needs research: back to the researcher for another pass" : "noted: seen. todo: to do later. dismissed: closed";
    return '<div class="icall"><label' + (dis ? tipAttrs(NOT_YET) : tipAttrs(hint)) + '>call <select data-icall="' + it._i + '"' + (dis ? " disabled" : "") + ">" + opts + "</select></label>" +
      '<input type="text" data-inote="' + it._i + '" placeholder="note" value="' + esc(it.call_note || "") + '"' + (dis ? " disabled" : "") + ">" +
      '<span class="dstat" id="istat-' + it._i + '" role="status">' + esc(itemStat(it)) + "</span></div>";
  }
  function itemsHtml(p) {
    if (!p.items.length) return '<div class="hiddennote">nothing to decide on this plant.</div>';
    var by = {};
    p.items.forEach(function (it) { (by[it.kind] = by[it.kind] || []).push(it); });
    var h = '<section class="items">';
    ITEM_KINDS.forEach(function (k) {
      if (!by[k]) return;
      // every kind group starts collapsed on a freshly opened plant; a group the reviewer opens
      // stays open across re-renders of the SAME card (igOpen resets in selectPipe)
      var open = k in S.igOpen ? S.igOpen[k] : false;
      h += '<details class="igroup" data-kind="' + k + '"' + (open ? " open" : "") + "><summary>" + esc(KIND_LABEL[k]) + ' <span class="n">(' + by[k].length + ")</span></summary>" +
        by[k].map(itemHtml).join("") + "</details>";
    });
    return h + "</section>";
  }

  // ---- card ----
  function tierSummary(p) {
    var c = {high: 0, medium: 0, low: 0, untiered: 0};
    p.lines.forEach(function (l) { c[tierOf(l)]++; });
    return ["high", "medium", "low", "untiered"].filter(function (t) { return c[t]; })
      .map(function (t) { return chip(c[t] + " " + (t === "untiered" ? "unrated" : t), t === "untiered" ? "" : t); }).join(" ");
  }
  // the unit a line sits under for grouping: "" = plant-wide
  function lineUnit(l) { return l.kind === "plant" || l.kind === "new_row" ? "" : (l.gem_unit_id || ""); }
  function renderCard() {
    var card = $("card");
    if (S.pipe < 0) { card.innerHTML = '<div class="empty">nothing matches the filters.</div>'; S.shown = []; return; }
    var p = D.plants[S.pipe], q = FS.q.trim().toLowerCase();
    var un = unitNames(p);
    var ctx = [p.statewide && "<b>statewide notes, not one plant</b>", untracked(p) && !p.statewide && "<b>not in GEM yet: a candidate plant</b>",
               p.state && esc(p.state), p.units.length && p.units.length + " unit" + (p.units.length === 1 ? "" : "s") + " in the export",
               tierSummary(p)]
      .filter(Boolean).map(function (x) { return "<span>" + x + "</span>"; }).join("");
    var h = '<div class="cardhead"><div class="headrow">' + "<h2>" + (p.statewide || untracked(p) ? "" : '<span class="pid"' + tipAttrs("click to copy the GEM plant id") + '>' + esc(p.pid) + "</span>") +
      '<a href="#" class="only" data-tab="all"' + tipAttrs("review everything on this plant: every change (filters ignored) and every item") + '>' + esc(p.name || "(no name)") + "</a>" +
      (un.length ? '<span class="hseg">' + esc(un.length > 4 ? un.slice(0, 3).join(" / ") + " / +" + (un.length - 3) : un.join(" / ")) + "</span>" : "") + '</h2><div class="bulkbtns">' +
      (function () {
        var minor = p.lines.filter(function (l) { return sevOf(l) === "minor"; });
        var on = minor.some(function (l) { return !cur(l); });
        var why = !minor.length ? "no minor changes on this plant" : "every minor change is already decided";
        return '<button type="button" class="bulk b-accept' + (on ? "" : " off") + '" data-bulk="pipe-minor"' + (on ? "" : ' aria-disabled="true" data-why="' + esc(why) + '"') +
          tipAttrs(on ? "accept every undecided minor change on this plant (the values stand, only links are added) that the filters show" : why) + '>accept all minor changes</button>';
      })() +
      '<button type="button" class="bulk b-accept" data-bulk="pipe-high"' + tipAttrs("accept every undecided green (high confidence) change on this plant, major or minor, that the filters show") + '>accept all high-conf changes</button>' +
      (function () {
        var nonHigh = p.lines.filter(function (l) { return tierOf(l) !== "high"; });
        var on = nonHigh.some(function (l) { return !cur(l); });
        var why = !nonHigh.length ? "every change is high confidence" : "every medium- and low-confidence change is already decided";
        return '<button type="button" class="bulk b-hold' + (on ? "" : " off") + '" data-bulk="pipe-all"' + (on ? "" : ' aria-disabled="true" data-why="' + esc(why) + '"') +
          tipAttrs(on ? "accept every undecided change on this plant, any confidence level, that the filters show" : why) + '>accept all changes</button>';
      })() +
      '</div></div><div class="ctx">' + ctx + "</div>";
    var nOpenItems = p.items.filter(function (it) { return !it.call; }).length;
    function todo(n, total) {
      if (!total) return "(0)";
      if (!n) return "(" + total + ", all decided)";
      return "(" + (n === total ? n : n + " of " + total) + " to decide)";
    }
    var bySev = {major: p.lines.filter(function (l) { return sevOf(l) === "major"; }), minor: p.lines.filter(function (l) { return sevOf(l) === "minor"; })};
    h += '<div class="tabs" role="tablist">' + SEV.map(function (s) {
      var openS = bySev[s].filter(function (l) { return !cur(l); }).length;
      return '<button type="button" role="tab" data-tab="' + s + '" aria-selected="' + (S.tab === s) + '"' + tipAttrs(SEV_TIP[s]) + ">" + SEV_LABEL[s] + " " + todo(openS, bySev[s].length) + "</button>";
    }).join("") +
      '<button type="button" role="tab" data-tab="items" aria-selected="' + (S.tab === "items") + '">items ' + todo(nOpenItems, p.items.length) + "</button>" +
      '<button type="button" role="tab" data-tab="all" aria-selected="' + (S.tab === "all") + '"' + tipAttrs("every change (filters ignored) and every item on this plant; also: click the name") + '>everything</button></div></div>';
    if (S.tab === "items") {
      S.shown = []; S.line = -1;
      card.innerHTML = h + itemsHtml(p);
      return;
    }
    // lines the filter lets through, grouped by unit when the plant has several units
    var all = S.tab === "all";
    var base = bySev[S.tab] || p.lines;
    var keep = all ? p.lines.slice() : base.filter(function (l) { return match(l, p, FS, null, q); });
    var hidden = base.length - keep.length;
    if (S.pin === S.pipe && !keep.length) { keep = base.slice(); hidden = 0; }
    var groups = [];
    var multi = p.units.length > 1 || keep.some(function (l) { return lineUnit(l) === ""; }) && keep.some(function (l) { return lineUnit(l) !== ""; });
    if (multi) {
      var pw = keep.filter(function (l) { return lineUnit(l) === ""; });
      if (pw.length) groups.push({label: "plant-wide", lines: pw});
      p.units.forEach(function (u) {
        groups.push({label: unitText(u), lines: keep.filter(function (l) { return lineUnit(l) === u.gem_unit_id; })});
      });
      var rest = keep.filter(function (l) { return lineUnit(l) && !unitOf(p, lineUnit(l)); });
      if (rest.length) groups.push({label: "other units", lines: rest});
    } else groups.push({label: "", lines: keep, plain: true});
    S.shown = [];
    groups.forEach(function (g) {
      if (!g.lines.length) return;
      if (!g.plain) h += '<div class="segdiv">' + esc(g.label) + "</div>";
      g.lines.forEach(function (l) {
        S.shown.push(l._i);
        h += '<div class="line tier-' + tierOf(l) + (cur(l) ? " d-" + cur(l) : "") + (settled(l) ? " dim" : "") +
          (l.kind === "new_row" ? " newcard" : "") + (l._i === S.line ? " cur" : "") + '" id="line-' + l._i + '" data-i="' + l._i + '">' + lineHtml(l) + "</div>";
      });
    });
    if (hidden) h += '<div class="hiddennote">' + hidden + " more change" + (hidden === 1 ? "" : "s") + " on this plant " + (hidden === 1 ? "is" : "are") +
      ' hidden by the filter. <a href="#" class="only" data-showall="1">show all</a></div>';
    if (!keep.length && !hidden) h += '<div class="hiddennote">no ' + (SEV_LABEL[S.tab] || "changes") + ' on this plant.</div>';
    if (all) h += '<h3 class="allitems">items</h3>' + itemsHtml(p);
    card.innerHTML = h;
    if (S.line < 0 || S.shown.indexOf(S.line) < 0) S.line = S.shown.length ? S.shown[0] : -1;
    var el = S.line >= 0 && $("line-" + S.line);
    if (el) el.classList.add("cur");
  }
  function setLine(i, noScroll) {
    var prev = S.line >= 0 && $("line-" + S.line);
    if (prev) prev.classList.remove("cur");
    S.line = i;
    var el = $("line-" + i);
    if (el) { el.classList.add("cur"); if (!noScroll) el.scrollIntoView({block: "nearest"}); }
  }

  // ---- keyboard navigation ----
  function stepLine(dir) {
    var at = S.shown.indexOf(S.line), n = at + dir;
    if (n >= 0 && n < S.shown.length) return setLine(S.shown[n]);
    stepPipe(dir, dir < 0);
  }
  function stepPipe(dir, toLast) {
    var at = S.visible.indexOf(S.pipe), n = at + dir;
    if (n < 0 || n >= S.visible.length) return;
    selectPipe(S.visible[n]);
    if (toLast && S.shown.length) setLine(S.shown[S.shown.length - 1]);
  }
  function firstRef(l) {
    if (!l) return "";
    if (l.kind === "new_row") {
      var refs = l.refs_by_col || {}, out = "";
      Object.keys(refs).forEach(function (c) { if (!out) out = asList(refs[c])[0] || ""; });
      return out;
    }
    return asList(l.proposed_refs)[0] || asList(l.current_ref)[0] || "";
  }
  function openFirstRef() {
    var u = firstRef(LINES[S.line]);
    if (u) window.open(u, "_blank", "noopener"); else toast("this change has no link to open");
  }
  function notYet() { toast(NOT_YET); }
  function setStat(i, text, failed) {
    var e = $("dstat-" + i);
    if (e) { e.textContent = text; e.className = "dstat" + (failed ? " err" : (text === "saving…" ? " saving" : "")); }
  }
  // Save one line's call. The UI changes only after the server confirms; while it is in flight the
  // line says "saving…", then "accepted by <reviewer> <time>" (or the refusal). No confirm dialog.
  function save(l, rec, advance) {
    if (!Store.caps.decide) return notYet();
    if (S.saving[l.key]) return;
    S.saving[l.key] = true;
    setStat(l._i, "saving…");
    Store.decide([rec]).then(function (saved) {
      applySaved(saved);
      S.stay[l.key] = true;
      banner("");
      var keepLine = S.line;
      refilter(true);
      if (keepLine >= 0 && $("line-" + keepLine)) setLine(keepLine, true);
      if (advance && S.line === l._i) nextUndecided();
    }).catch(function (e) {
      setStat(l._i, "not saved: " + e.message, true);
      toast("not saved: " + e.message);
    }).then(function () { delete S.saving[l.key]; });
  }
  function applyRecord(r) {
    var l = LINE_BY_KEY[r.key];
    if (!l) return;
    l.decision = r.undecided ? null : r.decision;
    l.reviewed = !r.undecided;
    l.decided_by = r.undecided ? null : r.reviewer;
    l.decided_at = r.undecided ? null : r.ts;
    l.suggested_value = r.undecided ? "" : (r.suggested_value || "");
    l.decision_note = r.undecided ? "" : (r.note || "");
  }
  function applyItemRecord(r) {
    var it = ITEM_BY_KEY[r.key];
    if (!it) return;
    it.call = r.undecided ? null : r.call;
    it.call_note = r.undecided ? null : r.note;
    it.reviewed = !r.undecided;
    it.decided_by = r.undecided ? null : r.reviewer;
    it.decided_at = r.undecided ? null : r.ts;
  }
  function applySaved(saved) {
    saved.forEach(function (r) { if ("call" in r) applyItemRecord(r); else applyRecord(r); });
  }
  // Save one item's call. Same in-place feedback as a line; the card re-renders in place.
  function saveItem(it, rec) {
    if (!Store.caps.decide) return notYet();
    if (S.saving[it.key]) return;
    S.saving[it.key] = true;
    var el = $("istat-" + it._i);
    if (el) { el.textContent = "saving…"; el.className = "dstat saving"; }
    Store.item([rec]).then(function (saved) {
      saved.forEach(applyItemRecord);
      banner("");
      refilter(true);
    }).catch(function (e) {
      renderCard();
      var e2 = $("istat-" + it._i);
      if (e2) { e2.textContent = "not saved: " + e.message; e2.className = "dstat err"; }
      toast("not saved: " + e.message);
    }).then(function () { delete S.saving[it.key]; });
  }
  function onItemChange(e) {
    var sel = e.target.closest("select[data-icall]"), inp = e.target.closest("input[data-inote]");
    var t = sel || inp;
    if (!t) return;
    var it = ITEMS[+t.getAttribute(sel ? "data-icall" : "data-inote")];
    if (!it) return;
    var box = t.closest(".icall"), call = box.querySelector("select").value, note = box.querySelector("input").value;
    if (!call) { if (sel && it.call) saveItem(it, {key: it.key, undo: true}); return; }
    if (inp && call === it.call && note === (it.call_note || "")) return;
    saveItem(it, {key: it.key, call: call, note: note});
  }
  function decideCurrent(decision, advance) {
    var l = LINES[S.line];
    if (S.tab === "items") return toast("the items tab takes calls, not change decisions: press i to go back to the changes");
    if (!l) return;
    save(l, {key: l.key, decision: decision}, advance);
  }
  function undoCurrent() {
    var l = LINES[S.line];
    if (S.tab === "items" || !l) return;
    if (!cur(l)) return toast("nothing to undo on this change");
    save(l, {key: l.key, undo: true}, false);
  }
  function nextUndecided() {       // after a keypress decision: the next open line, then the next plant
    var at = S.shown.indexOf(S.line);
    for (var n = at + 1; n < S.shown.length; n++) {
      if (!cur(LINES[S.shown[n]])) return setLine(S.shown[n]);
    }
    stepPipe(1);
  }
  // Suggest: an inline form on the current line. Prefill = the proposed value of the line's column.
  // Enter saves decision "suggest" with suggested_value + note; Esc cancels.
  function suggestPrefill(l) {
    var pv = l.proposed_values || {}, v = pv[l.column];
    if (blankv(v)) { var ks = Object.keys(pv).filter(function (k) { return !blankv(pv[k]); }); v = ks.length ? pv[ks[0]] : ""; }
    return blankv(v) ? "" : String(v);
  }
  function closeSuggest() {
    var f = document.querySelector("#card .sform");
    if (f) f.parentNode.removeChild(f);
  }
  function openSuggest(l) {
    if (!Store.caps.decide) return notYet();
    if (!l) return;
    var el = $("line-" + l._i);
    if (!el) return;
    closeSuggest();
    setLine(l._i, true);
    var prior = l.reviewed && l.decision === "suggest";
    var f = document.createElement("form");
    f.className = "sform";
    f.innerHTML = '<label>suggested value <input type="text" class="sv" autocomplete="off"></label>' +
      '<label>note <input type="text" class="sn" autocomplete="off" placeholder="why"></label>' +
      '<button type="submit" class="sv-save">save suggestion</button><button type="button" class="ghost sv-cancel">cancel (esc)</button>' +
      '<span class="faint sv-err" role="alert"></span>';
    var sv = f.querySelector(".sv"), sn = f.querySelector(".sn"), err = f.querySelector(".sv-err");
    sv.value = prior ? (l.suggested_value || "") : suggestPrefill(l);
    sn.value = prior ? (l.decision_note || "") : "";
    f.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); closeSuggest(); }
    });
    f.querySelector(".sv-cancel").onclick = closeSuggest;
    f.onsubmit = function (e) {
      e.preventDefault();
      if (blankv(sv.value) && blankv(sn.value)) { err.textContent = "give a suggested value or a note"; return; }
      var b = f.querySelector(".sv-save"); b.disabled = true;
      if (S.saving[l.key]) return;
      S.saving[l.key] = true;
      Store.decide([{key: l.key, decision: "suggest", suggested_value: sv.value, note: sn.value}]).then(function (saved) {
        applySaved(saved);
        S.stay[l.key] = true;
        banner("");
        var keepLine = S.line;
        refilter(true);
        if (keepLine >= 0 && $("line-" + keepLine)) setLine(keepLine, true);
        toast("suggestion saved");
      }).catch(function (e2) {
        b.disabled = false; err.textContent = "not saved: " + e2.message;
      }).then(function () { delete S.saving[l.key]; });
    };
    var ctl = el.querySelector(".controls");
    ctl.parentNode.insertBefore(f, ctl.nextSibling);
    sv.focus(); sv.select();
  }
  function suggestKey(e) {
    if (e && e.preventDefault) e.preventDefault();   // the "s" must not land in the form's input
    if (S.tab === "items") return toast("the items tab takes calls, not suggestions: press i to go back to the changes");
    openSuggest(LINES[S.line]);
  }
  var KEYS = {
    j: function () { stepLine(1); }, k: function () { stepLine(-1); },
    J: function () { stepPipe(1); }, K: function () { stepPipe(-1); },
    o: openFirstRef,
    d: function () {
      var l = S.line >= 0 && $("line-" + S.line), m = l && l.querySelector("details[data-more]");
      if (m) m.open = !m.open;
    },
    a: function () { decideCurrent("accept", true); }, h: function () { decideCurrent("hold", true); },
    r: function () { decideCurrent("reject", true); }, s: suggestKey, u: undoCurrent,
    "/": function (e) { e.preventDefault(); $("f-q").focus(); $("f-q").select(); },
    i: toggleItemsTab,
    "?": showHelp
  };
  function toggleItemsTab() {
    if (S.pipe < 0) return;
    S.tab = S.tab === "items" ? defaultTab(D.plants[S.pipe]) : "items";
    renderCard();
    if (S.tab === "items") { var s1 = document.querySelector("#card select[data-icall]"); if (s1) s1.focus(); }
  }
  var HELP = [["j / k", "next / previous change (runs on into the next plant)"], ["J / K", "next / previous plant"],
              ["a / h / r", "accept / hold / reject the change; saved at once, then on to the next open change"],
              ["s", "suggest a different value: an inline form on the change (value + note; enter saves, esc cancels)"],
              ["i", "switch the card between changes and items; calls save on change"],
              ["u", "undo: the change goes back to undecided"], ["o", "open the change's first source link (new tab)"], ["d", "show / hide the change's notes"],
              ["/", "search"], ["?", "this help"]];
  function showHelp() {
    var dlg = $("dialog");
    dlg.setAttribute("data-kind", "help");
    dlg.innerHTML = "<h3>keyboard</h3><table>" + HELP.map(function (r) { return "<tr><td><kbd>" + r[0] + "</kbd></td><td>" + r[1] + "</td></tr>"; }).join("") +
      '</table><div class="actions"><button type="button" id="dlg-close">close</button></div>';
    $("dlg-close").onclick = function () { dlg.close(); };
    dlg.showModal();
  }
  // "how to": a plain-language page on what the app shows and what each call does.
  var INFO =
    "<h3>how this works</h3>" +
    "<p>This page shows the <b>edits a research batch proposes</b> for the Global Oil and Gas Plant Tracker. " +
    "Nothing here is in the GEM database yet, and nothing on this page can write to it. Your job is to say yes or no to each edit.</p>" +
    "<h4>what you see</h4>" +
    "<ul>" +
    "<li><b>Left list:</b> the plants with something to decide. Click one to open it.</li>" +
    "<li><b>Card:</b> that plant's proposed changes, one per cell, grouped by unit. Each change shows the cell as it is <b>now</b> and the <b>proposed</b> value, " +
    "plus the source links that back it. A new link is <b>added next to</b> the links already in the Data Source cell. It never replaces one.</li>" +
    "<li><b>Major / minor:</b> a <b>major change</b> moves a value: it fills a blank, changes or clears a value, sets a plant-wide field, or adds a row. " +
    "A <b>minor change</b> means the value was checked again and stands, so only a source link is added. " +
    "The card opens on the major changes; the minor ones have their own tab and an <b>accept all minor changes</b> button.</li>" +
    "<li><b>Color:</b> green means one fully checked source (a status change needs two independent publishers), yellow means one source or a partial match, and red means weak. " +
    "Green changes default to accept; the rest default to hold.</li>" +
    "<li><b>Plant-wide:</b> a plant-level field such as the location or the owner is repeated on every unit row, so one accept covers all of them.</li>" +
    "<li><b>Items</b> tab: concerns the researcher raised, plants to watch, and owner or operator checks. They take a call and a note, but they never change a cell.</li>" +
    "</ul>" +
    "<h4>your four calls</h4>" +
    "<ul>" +
    "<li><b>accept:</b> yes, this edit goes into the actions workbook.</li>" +
    "<li><b>hold:</b> not sure yet, leave it open.</li>" +
    "<li><b>reject:</b> no, do not apply this.</li>" +
    "<li><b>suggest:</b> something else is right, so type the value or a note. The researcher looks at it again; it does not go into the workbook as is.</li>" +
    "</ul>" +
    "<h4>what happens when you accept</h4>" +
    "<ol>" +
    "<li>Your click is saved at once in the decision log" + (STATIC ? (Store.status && Store.status().state === "synced" ?
      " on this page, where the sender reads it back. <b>download decisions</b> gives you a backup copy of your calls" :
      " kept in this browser. Click <b>download decisions</b> when you are done (or any time) and send the file back; the calls are then added to the batch's log") :
      " in the batch's staging folder") + ". The GEM database is <b>not</b> touched.</li>" +
    "<li>When the batch is built, every accepted change goes into the <b>actions workbook</b> and the evidence file. Held, rejected and suggested changes are listed there as left out.</li>" +
    "<li>Someone then applies the workbook by hand, cell by cell, in the GEM web form.</li>" +
    "</ol>" +
    "<h4>good to know</h4>" +
    "<ul>" +
    "<li><b>Undo:</b> click the pressed button again, or press <kbd>u</kbd>. Nothing is deleted; the log just records the undo.</li>" +
    "<li>A grayed change is already decided. A bright change still needs you.</li>" +
    "<li>Press <kbd>?</kbd> for the keyboard shortcuts.</li>" +
    "</ul>";
  function showInfo() {
    var dlg = $("dialog");
    dlg.setAttribute("data-kind", "info");
    dlg.innerHTML = INFO + '<div class="actions"><button type="button" id="dlg-close">close</button></div>';
    $("dlg-close").onclick = function () { dlg.close(); };
    dlg.showModal();
    dlg.scrollTop = 0;
  }
  function onKey(e) {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    if ($("dialog").open) return;
    var t = e.target;
    if (t && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) { if (e.key === "Escape") t.blur(); return; }
    var f = KEYS[e.key];
    if (f) f(e);
  }
  var toastTimer = null;
  function toast(msg) {
    var t = $("toast");
    t.textContent = msg;
    t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, 4000);
  }
  var STICKY = "";
  function banner(msg) { var b = $("banner"); msg = msg || STICKY; b.textContent = msg; b.hidden = !msg; }

  function onCardClick(e) {
    var pidEl = e.target.closest(".pid");
    if (pidEl) { copyText(pidEl.textContent, pidEl.textContent + " copied"); return; }
    if (e.target.closest("[data-showall]")) {
      e.preventDefault();
      var keepPipe = S.pipe;
      FS = defaults(); FS.decision = "";
      syncControls(); S.pin = keepPipe; refilter(true); writeRoute(false);
      return;
    }
    var tb = e.target.closest("[data-tab]");
    if (tb && tb.tagName === "A") e.preventDefault();
    if (tb) {
      if (tb.getAttribute("data-tab") === "all") S.pin = S.pipe;   // deciding lines here must not drop the plant from the queue
      if (S.tab !== tb.getAttribute("data-tab")) { S.tab = tb.getAttribute("data-tab"); renderCard(); }
      return;
    }
    var sb = e.target.closest("button[data-suggest]");
    var b = e.target.closest("button[data-decide]");
    var ub = e.target.closest("button[data-undo]");
    var ln = e.target.closest(".line");
    if (ln) setLine(+ln.getAttribute("data-i"), true);
    if (ub && !ub.disabled) return undoCurrent();
    if (sb) {
      if (!Store.caps.decide) return notYet();
      return openSuggest(LINES[S.line]);
    }
    if (!b) return;
    if (!Store.caps.decide) return notYet();
    // a click on the pressed button takes the call back (the same record an undo writes)
    if (b.getAttribute("aria-pressed") === "true") return undoCurrent();
    decideCurrent(b.getAttribute("data-decide"), false);
  }

  // ---- bulk ----
  // The targets are the CURRENT filtered lines of the open plant. Lines already decided are skipped.
  function bulkTargets(mode) {
    var q = FS.q.trim().toLowerCase();
    var t = {lines: [], byKind: {}, decision: "accept", skip: {decided: 0, other: 0}};
    var p = D.plants[S.pipe];
    p.lines.forEach(function (l) {
      if (!match(l, p, FS, null, q)) return;
      if (cur(l)) { t.skip.decided++; return; }
      if ((mode === "pipe-high" && tierOf(l) !== "high") || (mode === "pipe-minor" && sevOf(l) !== "minor")) { t.skip.other++; return; }
      t.lines.push(l);
      t.byKind[l.kind] = (t.byKind[l.kind] || 0) + 1;
    });
    return t;
  }
  var BULK_TITLE = {"pipe-minor": "accept all minor changes", "pipe-high": "accept all high-conf changes", "pipe-all": "accept all changes"};
  function showBulk(mode) {
    if (!Store.caps.decide) return notYet();
    if (S.pipe < 0) return toast("nothing in view");
    var t = bulkTargets(mode), dlg = $("dialog"), sk = t.skip;
    var skipTxt = [sk.decided && sk.decided + " already decided",
                   sk.other && sk.other + (mode === "pipe-high" ? " not high confidence" : " major (the value moves: decide those by hand)")].filter(Boolean).join(", ");
    if (!t.lines.length) return toast("nothing to accept in view" + (skipTxt ? " (skipped: " + skipTxt + ")" : ""));
    var kinds = Object.keys(t.byKind).map(function (k) { return "<tr><td>" + esc(KIND_LABEL[k] || k) + "</td><td>" + t.byKind[k] + "</td></tr>"; }).join("");
    dlg.setAttribute("data-kind", "bulk");
    dlg.innerHTML = "<h3>" + esc(BULK_TITLE[mode]) + " (this plant)</h3><p><b>" + t.lines.length + " change" + (t.lines.length === 1 ? "" : "s") + "</b> will be accepted as " + esc(ME) + ", in one save:</p><table>" + kinds + "</table>" +
      (skipTxt ? '<p class="faint">skipped: ' + esc(skipTxt) + ".</p>" : "") +
      '<p class="faint" id="bulk-err"></p><div class="actions"><button type="button" class="ghost" id="dlg-cancel">cancel</button>' +
      '<button type="button" id="dlg-ok">accept ' + t.lines.length + "</button></div>";
    $("dlg-cancel").onclick = function () { dlg.close(); };
    $("dlg-ok").onclick = function () {
      var ok = $("dlg-ok"); ok.disabled = true; ok.textContent = "saving…";
      Store.decide(t.lines.map(function (l) { return {key: l.key, decision: "accept"}; })).then(function (saved) {
        applySaved(saved);
        t.lines.forEach(function (l) { S.stay[l.key] = true; });
        dlg.close();
        refilter(true);
        toast("accepted " + saved.length + " change" + (saved.length === 1 ? "" : "s"));
      }).catch(function (e) {
        ok.disabled = false; ok.textContent = "retry";
        $("bulk-err").textContent = "not saved: " + e.message;
        $("bulk-err").className = "err";
      });
    };
    dlg.showModal();
  }
  function copyText(text, msg) {
    msg = msg || "copied";
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      document.body.removeChild(ta);
      toast(ok ? msg : "could not copy: select the text by hand");
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { toast(msg); }, fallback);
    else fallback();
  }
  function reload(data) {
    var pid = D.plants[S.pipe] ? D.plants[S.pipe].pid : "";
    D = data;
    prepare();
    fillFilters(); syncControls();
    S.pin = -1; S.stay = {}; S.line = -1; S.igOpen = {};
    S.pipe = -1;
    D.plants.forEach(function (p, i) { if (p.pid === pid) S.pipe = i; });
    renderScope();
    refilter(true);
  }

  // ---- routing: #/L100000402511 plus an optional ?query with the filters that differ from the defaults ----
  var ROUTING = false;
  var QK = {decision: "d", kind: "k", severity: "sev", tier: "t", dir: "dir", column: "col", q: "q", country: "c", state: "st", by: "by", status: "status"};
  function routeHash() {
    var p = D.plants[S.pipe], d = defaults(), q = [];
    Object.keys(QK).forEach(function (f) {
      var v = FS[f];
      if (Array.isArray(v)) {
        if (v.join("|") === d[f].join("|")) return;
        v = v.join("|");
      }
      else if (v === d[f]) return;
      if (typeof v === "boolean") v = "1";
      else if (f === "decision" && v === "") v = "any";
      q.push(QK[f] + "=" + encodeURIComponent(v));
    });
    return "#/" + (p ? encodeURIComponent(p.pid) : "") + (q.length ? "?" + q.join("&") : "");
  }
  function curHash() { return location.hash || ""; }
  function writeRoute(replace) {
    if (ROUTING || !D) return;
    var h = routeHash();
    if (h === curHash()) return;
    try { history[replace ? "replaceState" : "pushState"](null, "", h); } catch (e) { /* file:// or blocked */ }
  }
  function applyRoute() {
    ROUTING = true;
    try {
      var m = /^#\/([^?]*)(?:\?(.*))?$/.exec(curHash()), pid = "";
      FS = defaults();
      if (m) {
        pid = decodeURIComponent(m[1]);
        (m[2] || "").split("&").forEach(function (kv) {
          var i = kv.indexOf("="); if (i < 1) return;
          var k = kv.slice(0, i), v = decodeURIComponent(kv.slice(i + 1));
          Object.keys(QK).forEach(function (f) {
            if (QK[f] !== k) return;
            FS[f] = Array.isArray(FS[f]) ? v.split("|").filter(function (c) { return c === NO_STATE || allStates().indexOf(c) >= 0; }) :
              typeof FS[f] === "boolean" ? v === "1" : (f === "decision" && v === "any" ? "" : v);
          });
        });
      }
      syncControls();
      S.pin = -1;
      var pi = -1;
      if (pid) D.plants.forEach(function (p, i) { if (p.pid === pid) pi = i; });
      S.pipe = pi;
      refilter(true);
      if (pi >= 0 && S.visible.indexOf(pi) < 0) {      // a link to a plant the filters would hide
        FS = defaults(); FS.decision = "";
        syncControls(); S.pin = pi; refilter(true);
      }
      if (pi >= 0 && S.visible.indexOf(pi) >= 0 && S.pipe !== pi) selectPipe(pi);
      if (pi >= 0 && S.visible.indexOf(pi) >= 0) { S.pipe = pi; renderQueue(); renderCard(); var li = $("pipes").querySelector("li.sel"); if (li) li.scrollIntoView({block: "nearest"}); }
    } finally { ROUTING = false; }
    writeRoute(true);
  }
  window.addEventListener("popstate", applyRoute);
  window.addEventListener("hashchange", function () { if (!ROUTING && location.hash !== routeHash()) applyRoute(); });

  // ---- boot ----
  window.ReviewApp = {
    get data() { return D; }, state: S, filters: function () { return FS; }, refilter: refilter, Store: Store, timing: {},
    reload: reload, applyRoute: applyRoute, writeRoute: writeRoute, banner: banner, toast: toast, esc: esc, copyText: copyText, et: et
  };
  function et(iso) { return String(iso || "").replace("T", " ").slice(0, 16) + " ET"; }
  function boot(reviewer, data) {
    D = data; ME = reviewer;
    var tLoaded = performance.now();
    prepare();
    banner();
    $("whoami").textContent = reviewer;
    var synced = STATIC && Store.status && Store.status().state === "synced";
    $("whoami").dataset.tip = synced ? "your calls are saved under these initials on this page as you make them" :
      STATIC ? "your calls are saved under these initials in this browser until you download them" :
      "your calls are saved under these initials in review_log.jsonl in each batch's staging folder";
    if (STATIC) {
      var ex = $("export-btn");
      ex.hidden = false;
      ex.dataset.tip = synced ? "a backup copy of every call made here, as a file. Your calls are already saved on this page" :
        "save every call made in this browser as a review_log.jsonl file to send back. Safe to click more than once: the file always holds the whole log";
      ex.onclick = function () {
        if (!Store.count()) { toast("no calls yet; nothing to download"); return; }
        Promise.resolve(Store.download()).then(function (r) {
          toast("saved " + r.count + " call" + (r.count === 1 ? "" : "s") + " to " + r.name);
        }, function (e) { toast(e && e.message ? e.message : "download failed"); });
      };
      var st = Store.status ? Store.status() : {state: "local"};
      if (st.state === "error") { STICKY = st.message; banner(); }
      else if (!synced && !Store.storageOk()) { STICKY = "this browser is not keeping the log between visits (private window or storage blocked): download your decisions before closing the tab"; banner(); }
    }
    renderScope();
    document.querySelector(".top h1").dataset.tip = "built " + et(D.built) + " · " + D.dirs.length + " staging folder" + (D.dirs.length === 1 ? "" : "s") + ": " +
      D.dirs.map(dirLabel).join(", ") + (D.scope.quarter ? " · " + D.scope.quarter : "");
    initFilters();
    applyRoute();
    var tDone = performance.now();
    window.ReviewApp.timing = {loadMs: Math.round(tLoaded - T0), renderMs: Math.round(tDone - tLoaded), totalMs: Math.round(tDone - T0),
                               plants: D.plants.length, lines: LINES.length, items: ITEMS.length};
    if (window.console) console.info("review app: loaded in " + window.ReviewApp.timing.loadMs + " ms, first render " +
      window.ReviewApp.timing.renderMs + " ms", window.ReviewApp.timing);
  }
  initTheme();
  document.addEventListener("keydown", onKey);

  // ---- tip popover (shows on hover and focus, stays while hovered, Esc dismisses) ----
  (function () {
    var tip = document.createElement("div"), owner = null, hideT = 0, showT = 0;
    tip.id = "tip"; tip.className = "tip"; tip.setAttribute("role", "tooltip"); tip.hidden = true;
    document.body.appendChild(tip);
    function show(el) {
      clearTimeout(hideT);
      owner = el; tip.innerHTML = '<div class="tip-head"></div>'; tip.firstChild.textContent = el.getAttribute("data-tip");
      var note = el.getAttribute("data-tip-note");
      if (note) { var n = document.createElement("div"); n.className = "tip-note"; n.textContent = "note: " + note; tip.appendChild(n); }
      tip.hidden = false;
      var r = el.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight, m = 8;
      var x = Math.min(Math.max(m, r.left), window.innerWidth - w - m);
      var y = r.bottom + 6 + h > window.innerHeight - m ? r.top - 6 - h : r.bottom + 6;
      tip.style.left = x + "px"; tip.style.top = Math.max(m, y) + "px";
    }
    function hide() { clearTimeout(showT); tip.hidden = true; owner = null; }
    function later() { clearTimeout(hideT); hideT = setTimeout(hide, 150); }
    document.addEventListener("mouseover", function (e) {
      var el = e.target.closest && e.target.closest("[data-tip]");
      if (owner && !owner.isConnected) hide();
      if (el) {
        if (el === owner) { clearTimeout(hideT); return; }
        clearTimeout(showT);
        if (owner) show(el); else showT = setTimeout(function () { if (el.isConnected) show(el); }, 300);
      } else {
        clearTimeout(showT);
        if (owner && !tip.contains(e.target)) later(); else if (tip.contains(e.target)) clearTimeout(hideT);
      }
    });
    document.addEventListener("focusin", function (e) {
      var t = e.target.closest && e.target.closest("[data-tip]");
      if (t && e.target.matches(":focus-visible")) show(t);
    });
    document.addEventListener("focusout", function (e) { if (owner && owner.contains(e.target)) hide(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !tip.hidden) { hide(); e.stopPropagation(); } }, true);
    document.documentElement.addEventListener("mouseleave", hide);
    document.addEventListener("mousedown", function (e) { if (owner && !tip.contains(e.target) && !owner.contains(e.target)) hide(); });
    window.addEventListener("blur", hide);
    document.addEventListener("scroll", function (e) { if (owner && !tip.contains(e.target)) hide(); }, true);
  })();
  $("card").addEventListener("click", onCardClick);
  $("pipes").addEventListener("click", function (e) {
    var li = e.target.closest("li[data-i]");
    if (li) selectPipe(+li.getAttribute("data-i"));
  });
  $("help-btn").onclick = showHelp;
  $("info-btn").onclick = showInfo;
  $("progress-btn").onclick = showProgress;
  // every popup shares #dialog: a click on the backdrop (outside the box) closes it
  $("dialog").addEventListener("click", function (e) {
    var dlg = e.currentTarget, r = dlg.getBoundingClientRect();
    if (e.target !== dlg) return;
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dlg.close();
  });
  $("card").addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("button[data-bulk]");
    if (!b) return;
    if (b.getAttribute("aria-disabled") === "true") return toast(b.getAttribute("data-why"));
    showBulk(b.getAttribute("data-bulk"));
  });
  $("card").addEventListener("change", onItemChange);
  $("card").addEventListener("toggle", function (e) {
    var d = e.target;
    if (d && d.classList && d.classList.contains("igroup")) S.igOpen[d.getAttribute("data-kind")] = d.open;
  }, true);
  Promise.all([Store.whoami(), Store.load()]).then(function (r) { boot(r[0], r[1]); })
    .catch(function (e) { banner("could not load the dataset: " + e.message); });
})();
