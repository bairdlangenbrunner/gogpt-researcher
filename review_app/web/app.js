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
    item: function (records) { return Store._post("/api/item", records); },
    flag: function (records) { return Store._post("/api/flag", records); }
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
    view: "plants",          // the left pane: "plants" (the queue) | "checklist" (the QC/Country checklist groups)
    closeout: false,         // the card shows the close-out panel (checklist group 9) instead of a plant
    igOpen: {}               // checklist group id -> item details open state (survives a re-render; reset per plant)
  };
  var ITEM_BY_KEY = {};
  var LINE_BY_KEY = {};
  var ROW_LABEL = {};        // checklist row number -> its label (from the dataset's groups)
  // the call vocabulary per item kind: must match review_app/store.py ITEM_CALLS. A watch item
  // (monitor lane) is not accepted or rejected: it is added to the database now, held, sent to
  // the possible-updates sheet, or taken off the watchlist (review_app/checklist.py WATCH_CALLS).
  var ITEM_CALLS = {concern: ["confirmed", "dismissed", "needs_research"], monitor: ["add_to_database", "hold", "possible_updates", "remove"]};
  var OTHER_CALLS = ["noted", "todo", "dismissed"];
  var NOTE_REQUIRED = {"monitor:remove": 1};     // calls that need a note saying why
  var CALL_LABEL = {add_to_database: "incorporate into database", hold: "hold", possible_updates: "send to possible updates", remove: "remove from watchlist",
                    needs_research: "needs research"};
  var CALL_HELP = {confirmed: "the concern stands", dismissed: "the concern is closed", needs_research: "goes back to the researcher",
                   noted: "seen, nothing to do", todo: "to do later",
                   add_to_database: "this belongs in GEM now: the researcher turns it into a full edit (a new row or a change) for the next batch",
                   hold: "not sure yet, leave it on the watchlist", possible_updates: "goes on the possible-updates sheet for a later cycle",
                   remove: "take it off the watchlist for good; say why in the note"};
  var VERB = {accept: "accepted", hold: "held", reject: "rejected", suggest: "suggested"};
  var $ = function (id) { return document.getElementById(id); };
  var LINE_KINDS = ["fill", "change", "delete", "plant", "reverified", "new_row"];
  var ITEM_KINDS = ["concern", "monitor", "entity", "other"];
  var KIND_LABEL = {fill: "fill a blank", change: "change a value", "delete": "clear a value", plant: "plant-wide",
                    reverified: "re-verified", new_row: "new row",
                    concern: "question about existing data", monitor: "watch item", entity: "new owner or operator to create", other: "other"};
  var MONITOR_LABEL = {new_to_tracker: "watch item: new to the tracker", existing_plant: "watch item: existing plant"};
  var KIND_TIP = {concern: "a question the researcher raised about data already in GEM: a value that could not be checked, two sources that disagree, a possible duplicate. It never changes a cell by itself",
                  entity: "an owner, operator or parent that is not in GEM's entity list yet. Someone has to create it in the GEM web form before the ownership edit can land",
                  new_to_tracker: "a plant or project GEM does not track at all yet. The researcher found it but it did not clear the bar for a new row (too early, too small, or too thin on evidence). Decide whether it goes into the database now, stays on the watchlist, goes to the possible-updates sheet, or comes off the list",
                  existing_plant: "something to watch on a plant GEM already tracks: a permit in progress, an expansion, a retirement date to confirm. The plant's row is not changed by this item"};
  function kindLabel(o) { return o.kind === "monitor" ? (MONITOR_LABEL[o.monitor_kind] || KIND_LABEL.monitor) : (KIND_LABEL[o.kind] || o.kind); }
  function kindTip(o) { return o.kind === "monitor" ? KIND_TIP[o.monitor_kind] || "" : KIND_TIP[o.kind] || ""; }
  // the checklist group of a line or item as a string ("1".."9" or "other"); review_data.py sets it
  function groupOf(o) { return o.group == null ? "other" : String(o.group); }
  function groupLabel(gid) {
    var g = (D.groups || []).filter(function (x) { return String(x.id) === gid; })[0];
    return g ? g.label : (gid === "other" ? "other" : "group " + gid);
  }
  function groupTip(o) {
    var rows = (o.checks || []).map(function (n) { return "row " + n + (ROW_LABEL[n] ? ": " + ROW_LABEL[n] : ""); });
    return "QC/Country checklist group " + groupOf(o) + ": " + groupLabel(groupOf(o)) + (rows.length ? "\nticks " + rows.join("\n") : "\n(no checklist row: a gap the checklist does not cover)");
  }
  function isOpen(o) { return o._item ? !(o.call && o.reviewed) : !cur(o); }
  function flagged(o, p) { return !!(o.pm_flag || (p && p.pm_flag)); }
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
    return {decision: "undecided", kind: "", group: "", tier: "", dir: "", column: "", q: "", country: "", state: [], by: "", status: false, pm: false};
  }
  // items (questions, watch items, entity checks) sit beside the edits whenever a checklist group
  // or the ask-the-PM filter is on; otherwise they show only when their kind is picked
  function itemsInView(fs) { return !!(fs.group || fs.pm || isItemKind(fs.kind)); }
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
        (blankv(l.decision_note) ? "" : ". " + l.decision_note) + (blankv(l.reference) ? "" : ". source: " + l.reference);
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
    LINES = []; ITEMS = []; LINE_BY_KEY = {}; ITEM_BY_KEY = {}; ROW_LABEL = {};
    (D.groups || []).forEach(function (g) { (g.rows || []).forEach(function (r) { ROW_LABEL[r.row] = r.label; }); });
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
      // picking a checklist group puts items in view, so the group dropdown counts them too
      else if (item && !itemsInView(fs) && skip !== "group") return false;
    }
    if (skip !== "decision" && fs.decision && dstate(o) !== fs.decision && !(!item && S.stay[o.key])) return false;
    if (skip !== "group" && fs.group && groupOf(o) !== fs.group) return false;
    if (skip !== "tier" && fs.tier && (item || tierOf(o) !== fs.tier)) return false;
    if (fs.pm && !flagged(o, p)) return false;
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
    var q = FS.q.trim().toLowerCase(), n = 0, todo = 0, ni = 0, tsev = {major: 0, minor: 0}, pm = p.pm_flag ? 1 : 0;
    p.lines.forEach(function (l) {
      if (l.pm_flag) pm++;
      if (!match(l, p, FS, null, q)) return;
      n++;
      if (!cur(l)) { todo++; tsev[sevOf(l)]++; }
    });
    p.items.forEach(function (it) { if (it.pm_flag) pm++; if (match(it, p, FS, null, q)) ni++; });
    p._n = n; p._todo = todo; p._ni = ni; p._tsev = tsev; p._pm = pm;
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
  function facetVal(o, facet) {
    return facet === "decision" ? dstate(o) : facet === "kind" ? o.kind : facet === "group" ? groupOf(o) : tierOf(o);
  }
  function facetCounts(facet, values) {
    var q = FS.q.trim().toLowerCase(), c = {};
    values.forEach(function (v) { c[v] = 0; });
    function tally(o, p, v) { if (match(o, p, FS, facet, q) && v in c) c[v]++; }
    // items count under kind and group always, and under decision when the filters let items through
    var items = facet === "kind" || facet === "group" || (facet === "decision" && itemsInView(FS));
    D.plants.forEach(function (p) {
      p.lines.forEach(function (l) { tally(l, p, facetVal(l, facet)); });
      if (items) p.items.forEach(function (it) { tally(it, p, facetVal(it, facet)); });
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
  // the states of the picked country; every batch state while no country is picked
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
    // with several countries the box waits for a pick; a one-country review (the US states) shows it straight away
    box.hidden = (!FS.country && countries().length > 1) || all.length < 2;
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
    var gids = (D.groups || []).map(function (g) { return String(g.id); }), gl = {};
    (D.groups || []).forEach(function (g) { gl[String(g.id)] = (g.id === "other" ? "" : g.id + " · ") + g.label; });
    if (gids.indexOf("other") < 0 && LINES.concat(ITEMS).some(function (o) { return groupOf(o) === "other"; })) { gids.push("other"); gl.other = "other"; }
    facetSelect("f-group", "group", gids, gl);
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
    ["decision", "kind", "group", "tier", "column", "dir"].forEach(function (f) {
      $("f-" + f).onchange = function () { FS[f] = this.value; changed(); };
    });
    $("f-status").onchange = function () { FS.status = this.checked; changed(); };
    // "ask the PM" matches flagged lines and items whatever their decision: drop the undecided-only default
    $("f-pm").onchange = function () { FS.pm = this.checked; if (FS.pm && FS.decision === "undecided") FS.decision = ""; changed(); };
    $("pane-mode").onclick = function (e) {
      var b = e.target.closest("button[data-view]");
      if (b) setView(b.getAttribute("data-view"));
    };
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
  function changed(replace) { S.pin = -1; S.stay = {}; S.closeout = false; refilter(true); writeRoute(replace === true); }
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
    $("f-pm").checked = FS.pm;
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
    if (FS.group) chip("group", "checklist: " + groupLabel(FS.group), false);
    if (FS.pm) chip("pm", "ask the PM", false);
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
  // per checklist group: everything in it (edits and items), how much is still open, how much is flagged for the PM
  function groupStats() {
    var out = {};
    (D.groups || []).forEach(function (g) { out[String(g.id)] = {total: 0, open: 0, pm: 0, rows: {}}; });
    LINES.concat(ITEMS).forEach(function (o) {
      var gid = groupOf(o), s = out[gid] || (out[gid] = {total: 0, open: 0, pm: 0, rows: {}});
      s.total++;
      if (isOpen(o)) s.open++;
      if (o.pm_flag) s.pm++;
      (o.checks || []).forEach(function (n) { s.rows[n] = s.rows[n] || {total: 0, open: 0}; s.rows[n].total++; if (isOpen(o)) s.rows[n].open++; });
    });
    return out;
  }
  function showProgress() {
    var dlg = $("dialog"), g = S.progress || {done: 0, total: 0, sev: {major: {done: 0, total: 0}, minor: {done: 0, total: 0}}};
    var items = ITEMS.length, calls = ITEMS.filter(function (it) { return it.call && it.reviewed; }).length, gs = groupStats();
    var pm = LINES.concat(ITEMS).filter(function (o) { return o.pm_flag; }).length + D.plants.filter(function (p) { return p.pm_flag; }).length;
    dlg.setAttribute("data-kind", "progress");
    dlg.innerHTML = "<h3>progress</h3><p>" + esc(S.countText || "") + " in view</p>" +
      '<div class="progress" aria-hidden="true"><div id="progress-bar" style="width:' + (g.total ? 100 * g.done / g.total : 0) + '%"></div></div>' +
      "<p>" + g.done + " of " + g.total + " changes decided &middot; major " + g.sev.major.done + " of " + g.sev.major.total +
      " &middot; minor " + g.sev.minor.done + " of " + g.sev.minor.total + "</p>" +
      "<p>" + calls + " of " + items + " items have a call" + (pm ? " &middot; " + pm + " flagged for the PM" : "") + "</p>" +
      '<h4>by checklist group</h4><table class="sumtab"><tr><th>group</th><th>open</th><th>total</th></tr>' +
      (D.groups || []).filter(function (x) { return !x.panel; }).map(function (x) {
        var s = gs[String(x.id)] || {open: 0, total: 0};
        return "<tr><td>" + esc((x.id === "other" ? "" : x.id + " · ") + x.label) + '</td><td class="num">' + (s.total && !s.open ? "✓" : s.open) + '</td><td class="num">' + s.total + "</td></tr>";
      }).join("") + "</table>" +
      '<div class="actions"><button type="button" id="dlg-close">close</button></div>';
    $("dlg-close").onclick = function () { dlg.close(); };
    dlg.showModal();
  }

  // ---- queue ----
  function unitNames(p) {
    return p.units.map(function (u) { return String(u.unit_name || u.gem_unit_id || "").trim(); }).filter(Boolean);
  }
  function setView(v) {
    if (v !== "plants" && v !== "checklist") return;
    S.view = v;
    try { localStorage.setItem("review-view", v); } catch (e) { /* ignore */ }
    Array.prototype.forEach.call($("pane-mode").querySelectorAll("button[data-view]"), function (b) {
      b.setAttribute("aria-selected", String(b.getAttribute("data-view") === v));
    });
    renderQueue();
  }
  // the left pane in checklist mode: one row per QC/Country checklist group with how much of it is
  // still open; a click filters the plants to that group. A group with nothing open gets a check mark.
  function renderChecklist() {
    var gs = groupStats(), h = [];
    (D.groups || []).forEach(function (g) {
      var gid = String(g.id), s = gs[gid] || {total: 0, open: 0, pm: 0, rows: {}};
      var rows = (g.rows || []).filter(function (r) { return s.rows[r.row]; }).map(function (r) {
        var rs = s.rows[r.row];
        return '<span class="grow-row' + (rs.open ? "" : " done") + '"' + tipAttrs("checklist row " + r.row + ": " + r.label + (r.optional ? " (optional)" : "")) + ">" +
          (rs.open ? "" : "✓ ") + "row " + r.row + " <span class=\"n\">" + (rs.open ? rs.open + " open" : rs.total) + "</span></span>";
      });
      var badge = g.panel ? '<span class="n">' + (S.closeout ? "open" : "click to open the panel") + "</span>" :
        !s.total ? '<span class="n">nothing staged</span>' :
        s.open ? '<span class="n todo">' + s.open + " open of " + s.total + "</span>" : '<span class="n">' + s.total + " &middot; done</span>";
      h.push('<li data-g="' + esc(gid) + '" class="grp' + (FS.group === gid || (g.panel && S.closeout) ? " sel" : "") + (s.total && !s.open ? " done" : "") + '">' +
        '<div class="pname">' + (s.total && !s.open ? "✓ " : "") + esc((g.id === "other" ? "" : g.id + ". ") + g.label) + (s.pm ? ' <span class="pm" data-tip="' + s.pm + " flagged for the PM in this group\">PM " + s.pm + "</span>" : "") + "</div>" +
        '<div class="pmeta"><span class="grow">' + esc(g.blurb || "") + '</span>' + badge + "</div>" +
        (rows.length ? '<div class="grows">' + rows.join(" ") + "</div>" : "") + "</li>");
    });
    $("pipes").innerHTML = h.join("");
  }
  // "2 items", or "2 of 7 items" when a filter is hiding some of the plant's items
  function itemCount(p) {
    var t = p.items.length;
    return p._ni < t ? p._ni + " of " + t + " items" : t + " item" + (t === 1 ? "" : "s");
  }
  function renderQueue() {
    if (S.view === "checklist") return renderChecklist();
    var h = [];
    S.visible.forEach(function (i) {
      var p = D.plants[i];
      var dots = {};
      p.lines.forEach(function (l) { dots[tierOf(l)] = 1; });
      var dd = ["high", "medium", "low"].filter(function (t) { return dots[t]; })
        .map(function (t) { return '<span class="dot ' + t + '" data-tip="' + t + ' confidence" role="img" aria-label="' + t + ' confidence"></span>'; }).join("");
      var ts = p._tsev || {}, parts = SEV.filter(function (s) { return ts[s]; }).map(function (s) { return ts[s] + " " + s; });
      var badge = p._todo ? '<span class="n todo">' + (parts.length ? parts.join(" &middot; ") : p._todo) + " to decide</span>"
        : (p._n ? '<span class="n">' + p._n + " &middot; done</span>" : (p._ni ? '<span class="n">' + itemCount(p) + "</span>" : '<span class="n"></span>'));
      if (p._ni && p._todo) badge = '<span class="n">' + itemCount(p) + " &middot; </span>" + badge;
      var pm = p._pm ? ' <span class="pm"' + tipAttrs(p._pm + " question" + (p._pm === 1 ? "" : "s") + " for the PM on this plant") + ">PM " + p._pm + "</span>" : "";
      var un = unitNames(p);
      var where = p.statewide ? "statewide" : (p.units.length + " unit" + (p.units.length === 1 ? "" : "s"));
      h.push('<li data-i="' + i + '"' + (i === S.pipe ? ' class="sel"' : "") + '><div class="pname">' + esc(p.name || "(no name)") +
        (un.length ? ' <span class="pseg">' + esc(un[0]) + (un.length > 1 ? " +" + (un.length - 1) : "") + "</span>" : "") + pm +
        '</div><div class="pmeta"><span>' + esc(p.statewide ? p.state : (untracked(p) ? "not in GEM yet" : p.pid)) + " &middot; " + esc(where) +
        '</span><span class="grow"></span>' + badge + '</div>' + (dd ? '<div class="dots">' + dd + "</div>" : "") + "</li>");
    });
    $("pipes").innerHTML = h.join("");
  }
  // a click on a checklist group: filter the plants to it and show them
  function selectGroup(gid) {
    var g = (D.groups || []).filter(function (x) { return String(x.id) === gid; })[0];
    if (g && g.panel) {
      // the close-out group is not a filter: it opens a panel in the card pane that gathers what
      // the end-of-state checklist rows need (units to mark, a summary draft, the sheets to update)
      S.closeout = !S.closeout;
      S.line = -1;
      renderQueue(); renderCard();
      return;
    }
    FS.group = FS.group === gid ? "" : gid;
    FS.decision = "";                 // a group lists everything in it, decided or not
    changed();
    setView("plants");
  }
  function selectPipe(i, lineIdx) {
    if (S.pipe !== i) S.igOpen = {};          // item groups collapse again on a new plant
    S.closeout = false;
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
  // the checklist group chip every line and item carries: "checklist 3" with the rows it ticks on hover
  // the IRP box state of the unit a line or item sits on: "yes" / "no" / "" (unknown or no unit)
  function irpBoxOf(o) {
    var p = D.plants[o._p], u = p && o.gem_unit_id ? unitOf(p, o.gem_unit_id) : null;
    return u ? (u.irp_box || "") : "";
  }
  // a finding that comes from a utility integrated resource plan (US only; checklist row 37)
  function irpChip(o) {
    var box = irpBoxOf(o);
    var tip = "this comes from a utility integrated resource plan (IRP). " +
      (o.kind === "new_row" ? "Tick the IRP box on the new row when it is created." :
       box === "yes" ? "The unit's IRP box is already ticked in the database." :
       box === "no" ? "The unit's IRP box is not ticked yet: tick it in the web form when the change goes in." :
       "The export does not show this unit's IRP box; check it in the web form.") + " QC/Country checklist row 37.";
    return chip("IRP" + (box === "no" ? ": tick the box" : ""), box === "no" ? "irp todo" : "irp", tip);
  }
  function groupChip(o) {
    var gid = groupOf(o);
    return chip("checklist " + (gid === "other" ? "gap" : gid), "grp", groupTip(o));
  }
  // the ask-the-PM box: a flag beside the decision, with a short note. Works on a line, an item or the whole plant.
  function pmBox(o, attr, id) {
    var dis = !Store.caps.decide, on = !!o.pm_flag;
    return '<label class="pmbox' + (on ? " on" : "") + '"' + tipAttrs(dis ? NOT_YET : "flag this for the GOGPT project manager. The flag sits beside your decision: you can accept something and still ask about it. Flagged items are listed together in the evidence file and can be filtered with \"ask the PM\"") +
      '><input type="checkbox" ' + attr + '="' + esc(id) + '"' + (on ? " checked" : "") + (dis ? " disabled" : "") + "> ask the PM</label>" +
      (on ? '<input type="text" class="pmnote" ' + attr + '-note="' + esc(id) + '" placeholder="question for the PM" value="' + esc(o.pm_note || "") + '"' + (dis ? " disabled" : "") + ">" : "");
  }
  function lineHtml(l) {
    var chips = [];
    if (l.kind === "new_row") chips.push(chip(KIND_LABEL.new_row, "newrow"));
    if (l.kind === "plant") chips.push(chip("plant-wide", "oo", "a plant-level field: the export repeats it on every unit row, so the edit lands on every unit row of this plant"));
    chips.push(tierChip(l));
    chips.push(sevChip(l));
    chips.push(groupChip(l));
    if (l.irp) chips.push(irpChip(l));
    if (l.pm_flag) chips.push(chip("PM", "pm", "flagged for the project manager" + (l.pm_note ? ": " + l.pm_note : "")));
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
      pmBox(l, "data-pm", l.key) +
      '<span class="dstat" id="dstat-' + l._i + '" role="status">' + esc(decisionText(l)) + "</span></div>";
    h += detailsHtml(l);
    return h;
  }

  // ---- items ----
  var HIDE = {call_note: 1, call_reference: 1, decided_by: 1, decided_at: 1, key: 1, dir: 1, record_id: 1, call: 1, reviewed: 1, kind: 1,
              gem_unit_id: 1, unit_name: 1, links: 1, verifications: 1, _item: 1, _p: 1, _i: 1,
              group: 1, group_label: 1, checks: 1, monitor_kind: 1, pm_flag: 1, pm_note: 1, pm_by: 1, duplicate_of: 1, concern_type_raw: 1, plant_name: 1};
  var BODY = ["notes", "recommendation", "reason", "lookup_result"];
  var CONCERN_ISSUE = {unverified_value: "a value could not be checked against its source", conflict: "two sources disagree",
                       duplicate: "this may duplicate another row", missing_source: "a value has no source link",
                       capacity: "the capacity figure needs a closer look", status: "the status needs a closer look",
                       ownership: "the owner or operator needs a closer look",
                       // the normalized kinds (review_app/checklist.py CONCERN_KINDS)
                       existence: "does this plant or unit exist as GEM records it?", scope: "is this in the tracker's scope?",
                       "capacity-threshold": "is this above the capacity threshold?", identity: "which plant or unit is this?",
                       attribution: "who owns or operates this?", "conversion-link": "how does this link to a coal or other unit?",
                       location: "where exactly is this?", source: "the source needs a closer look", validation: "a GEM validation error",
                       other: "a question about this plant's data"};
  function concernHead(it) {
    var t = String(it.concern_type || "concern");
    if (CONCERN_ISSUE[t]) return CONCERN_ISSUE[t];
    // a column name: "Capacity (MW): a question about this value"
    return /^[A-Z]/.test(t) ? t + ": a question about this value" : t.replace(/_/g, " ");
  }
  function itemHead(it) {
    switch (it.kind) {
      case "concern": return concernHead(it);
      case "monitor": return (it.reason || it.item || "watch this plant") + (it.recheck_by ? " (check again by " + it.recheck_by + ")" : "");
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
    var cls = it.kind === "monitor" ? " watch-" + (it.monitor_kind || "existing_plant") : "";
    var h = '<div class="item' + (it.call && it.reviewed ? " done" : "") + cls + '"><div class="row1">' + chip(kindLabel(it), it.kind === "monitor" ? "watch" : "", kindTip(it)) +
      " <b>" + esc(itemHead(it)) + "</b> " + groupChip(it) + (it.irp ? " " + irpChip(it) : "") + (it.pm_flag ? " " + chip("PM", "pm", "flagged for the project manager" + (it.pm_note ? ": " + it.pm_note : "")) : "") +
      '<span class="where">' + esc(where) + "</span></div>";
    if (it.kind === "monitor") {
      var facts = [];
      if (it.capacity_mw) facts.push(chip(it.capacity_mw + " MW"));
      if (it.status) facts.push(chip(it.status));
      if (it.tier && it.tier !== "untiered") facts.push(chip(it.tier + " confidence", it.tier, TIER_TIP[it.tier]));
      if (it.duplicate_of) {
        var first = ITEM_BY_KEY[it.duplicate_of];
        facts.push(chip("also staged in " + dirLabel(first ? first.dir : it.duplicate_of.split("::")[0]), "oo", "the same candidate was staged twice (an update batch and a discovery batch): decide it once, on the first copy, and give this one the same call"));
      }
      if (facts.length) h += '<div class="facts">' + facts.join(" ") + "</div>";
    }
    h += b.html;
    if (rows.length) h += "<details><summary>all fields</summary><table class=\"rowdata\">" + rows.join("") + "</table></details>";
    return h + itemControls(it) + "</div>";
  }
  function itemVocab(it) { return ITEM_CALLS[it.kind] || OTHER_CALLS; }
  function callText(c) { return CALL_LABEL[c] || String(c || "").replace(/_/g, " "); }
  function itemStat(it) {
    return it.call && it.reviewed ? (callText(it.call) + " by " + (it.decided_by || "?") + " " + timeOf(it.decided_at)) : "";
  }
  var CALL_HINT = {concern: "confirmed: the concern stands and goes into the evidence file. dismissed: closed, nothing to do. needs research: back to the researcher for another pass",
                   monitor: "incorporate into database: this belongs in GEM now, the researcher writes it up as a full edit. hold: keep watching. send to possible updates: park it on the possible-updates sheet for a later cycle. remove from watchlist: drop it, with a note saying why",
                   other: "noted: seen. todo: to do later. dismissed: closed"};
  function itemControls(it) {
    var dis = !Store.caps.decide, v = itemVocab(it);
    var opts = '<option value="">no call</option>' + v.map(function (c) {
      return '<option value="' + c + '"' + (it.call === c ? " selected" : "") + ' title="' + esc(CALL_HELP[c] || "") + '">' + esc(callText(c)) + "</option>";
    }).join("");
    var hint = CALL_HINT[it.kind] || CALL_HINT.other;
    return '<div class="icall"><label' + (dis ? tipAttrs(NOT_YET) : tipAttrs(hint)) + '>call <select data-icall="' + it._i + '"' + (dis ? " disabled" : "") + ">" + opts + "</select></label>" +
      '<input type="text" data-inote="' + it._i + '" placeholder="note' + (it.kind === "monitor" ? " (needed to remove from the watchlist)" : "") + '" value="' + esc(it.call_note || "") + '"' + (dis ? " disabled" : "") + ">" +
      '<input type="url" data-iref="' + it._i + '" placeholder="source link, if you have one" value="' + esc(it.call_reference || "") + '"' + (dis ? " disabled" : "") + ">" +
      pmBox(it, "data-pm", it.key) +
      '<span class="dstat" id="istat-' + it._i + '" role="status">' + esc(itemStat(it)) + "</span></div>";
  }
  // items grouped by checklist group (the dataset's order), each with its kind chip; `only`
  // restricts to the items the filters let through
  function itemsHtml(p, only) {
    var q = FS.q.trim().toLowerCase(), list = p.items;
    if (only) list = list.filter(function (it) { return match(it, p, FS, null, q); });
    var hidden = p.items.length - list.length;
    if (!list.length) return '<div class="hiddennote">' + (hidden ? hidden + " item" + (hidden === 1 ? " is" : "s are") + ' hidden by the filter. <a href="#" class="only" data-showall="1">show all</a>' : "nothing to decide on this plant.") + "</div>";
    var by = {}, order = (D.groups || []).map(function (g) { return String(g.id); });
    list.forEach(function (it) { var g = groupOf(it); (by[g] = by[g] || []).push(it); if (order.indexOf(g) < 0) order.push(g); });
    var h = '<section class="items">';
    order.forEach(function (g) {
      if (!by[g]) return;
      // every group starts collapsed on a freshly opened plant unless it is the only one; a group the
      // reviewer opens stays open across re-renders of the SAME card (igOpen resets in selectPipe)
      var open = g in S.igOpen ? S.igOpen[g] : order.filter(function (x) { return by[x]; }).length === 1;
      var nOpen = by[g].filter(isOpen).length;
      h += '<details class="igroup" data-g="' + esc(g) + '"' + (open ? " open" : "") + "><summary>" + esc((g === "other" ? "" : "checklist " + g + ": ") + groupLabel(g)) +
        ' <span class="n">(' + (nOpen ? nOpen + " open of " + by[g].length : by[g].length + ", all called") + ")</span></summary>" +
        by[g].map(itemHtml).join("") + "</details>";
    });
    if (hidden) h += '<div class="hiddennote">' + hidden + " more item" + (hidden === 1 ? " is" : "s are") + ' hidden by the filter. <a href="#" class="only" data-showall="1">show all</a></div>';
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
  // ---- close-out panel (checklist group 9) ----
  // Not one plant: what the end-of-state rows of the QC/Country checklist need, computed from the
  // decisions made so far. Nothing here is saved; it is read off the page and typed into the sheets.
  function closeoutHtml() {
    var links = D.links || {}, us = !!D.us, where = (D.scope.states || []).join(", ") || D.scope.country || "";
    var quarter = D.scope.quarter || "";
    function link(key, fallback) {
      var l = links[key];
      return l && l.url ? '<a href="' + esc(l.url) + '" target="_blank" rel="noopener">' + esc(l.label) + " ↗</a>" : esc(fallback || (l && l.label) || key);
    }
    function row(n) { return '<span class="rown"' + tipAttrs("QC/Country checklist row " + n + (ROW_LABEL[n] ? ": " + ROW_LABEL[n] : "")) + ">row " + n + "</span>"; }
    function plantOf(o) { return D.plants[o._p]; }
    // units: every unit a staged change touches, by what its decisions add up to
    var units = {updated: [], open: [], none: []}, itemsOnly = [];
    D.plants.forEach(function (p) {
      if (p.statewide || untracked(p)) return;
      if (!p.lines.length && p.items.length) { itemsOnly.push(p); return; }
      p.units.forEach(function (u) {
        var ls = p.lines.filter(function (l) { return lineUnit(l) === u.gem_unit_id || (lineUnit(l) === "" && l.kind === "plant"); });
        if (!ls.length) return;
        var acc = ls.some(function (l) { return cur(l) === "accept"; });
        var open = ls.some(function (l) { var d = cur(l); return !d || d === "hold" || d === "suggest"; });
        var entry = {p: p, u: u, n: ls.length, nAcc: ls.filter(function (l) { return cur(l) === "accept"; }).length};
        (acc ? units.updated : open ? units.open : units.none).push(entry);
      });
    });
    function unitLine(e) { return esc(e.p.name) + " · " + esc(unitText(e.u)) + ' <span class="n">(' + e.nAcc + " of " + e.n + " accepted)</span>"; }
    function unitText2(e) { return e.p.name + "\t" + (e.u.unit_name || "") + "\t" + e.u.gem_unit_id; }
    function unitList(title, list, say) {
      if (!list.length) return "";
      return '<details class="colist"' + (list.length <= 12 ? " open" : "") + "><summary>" + esc(title) + ' <span class="n">(' + list.length + ")</span></summary><p class=\"muted\">" + esc(say) + "</p><ul>" +
        list.map(function (e) { return "<li>" + unitLine(e) + "</li>"; }).join("") + "</ul></details>";
    }
    // the numbers behind the summary draft
    var c = {accept: 0, hold: 0, reject: 0, suggest: 0, undecided: 0};
    LINES.forEach(function (l) { c[dstate(l)]++; });
    var statusAcc = LINES.filter(function (l) { return l.column === "Status" && cur(l) === "accept" && l.kind !== "reverified"; });
    var newRows = LINES.filter(function (l) { return l.kind === "new_row" && cur(l) === "accept"; });
    var watchNew = ITEMS.filter(function (it) { return it.kind === "monitor" && it.monitor_kind === "new_to_tracker"; });
    var watchOld = ITEMS.filter(function (it) { return it.kind === "monitor" && it.monitor_kind !== "new_to_tracker"; });
    var promote = ITEMS.filter(function (it) { return it.kind === "monitor" && it.call === "add_to_database"; });
    var toSheet = ITEMS.filter(function (it) { return it.kind === "monitor" && it.call === "possible_updates"; });
    var held = ITEMS.filter(function (it) { return it.kind === "monitor" && it.call === "hold"; });
    var entities = ITEMS.filter(function (it) { return it.kind === "entity"; });
    var concerns = ITEMS.filter(function (it) { return it.kind === "concern" && it.call === "confirmed"; });
    var pm = LINES.concat(ITEMS).filter(function (o) { return o.pm_flag; }).length + D.plants.filter(function (p) { return p.pm_flag; }).length;
    // records from a utility resource plan, by what the unit's IRP box needs (row 37)
    var irpRecs = LINES.concat(ITEMS).filter(function (o) { return o.irp; });
    var irpNew = irpRecs.filter(function (o) { return o.kind === "new_row"; });
    var irpTick = irpRecs.filter(function (o) { return o.kind !== "new_row" && irpBoxOf(o) === "no"; });
    var irpDone = irpRecs.filter(function (o) { return o.kind !== "new_row" && irpBoxOf(o) === "yes"; });
    var irpUnknown = irpRecs.filter(function (o) { return o.kind !== "new_row" && !irpBoxOf(o); });
    var nPlants = D.plants.filter(function (p) { return !p.statewide && !untracked(p); }).length;
    function plural(n, w) { return n + " " + w + (n === 1 ? "" : "s"); }
    var sentences = [];
    sentences.push((quarter ? quarter.toUpperCase() + " " : "") + "GOGPT review of " + (where || "this scope") + ": " + plural(nPlants, "tracked plant") + " looked at.");
    sentences.push(plural(c.accept, "change") + " accepted, " + c.reject + " rejected, " + c.hold + " held, " + c.suggest + " sent back with a suggestion" + (c.undecided ? ", " + c.undecided + " not decided yet" : "") + ".");
    if (statusAcc.length) sentences.push("Status changes: " + statusAcc.map(function (l) {
      var p = plantOf(l), v = l.proposed_values && l.proposed_values.Status, from = l.current && l.current.Status;
      return p.name + (l.unit_name ? " " + l.unit_name : "") + (from ? " from " + from : "") + " to " + (v || "?");
    }).join("; ") + ".");
    if (newRows.length) sentences.push(plural(newRows.length, "new row") + " accepted for the database.");
    if (us && irpRecs.length) sentences.push(plural(irpRecs.length, "finding") + " from utility resource plans" + (irpTick.length ? "; IRP box to tick on " + plural(irpTick.length, "unit") : "") + ".");
    if (watchNew.length || watchOld.length) sentences.push("Watch list: " + watchNew.length + " new to the tracker and " + watchOld.length + " on existing plants" +
      (promote.length ? "; " + promote.length + " to be added to the database" : "") + (toSheet.length ? "; " + toSheet.length + " sent to the possible-updates sheet" : "") + ".");
    if (entities.length) sentences.push(entities.length + " new owner" + (entities.length === 1 ? "" : "s") + " or operator" + (entities.length === 1 ? "" : "s") + " to create in the database.");
    if (concerns.length) sentences.push(plural(concerns.length, "open question") + " about existing data confirmed for follow-up.");
    if (pm) sentences.push(plural(pm, "question") + " for the project manager.");
    sentences.push("Researched with an AI agent (Claude); every change was checked by a person on the review page before it went into the actions workbook.");
    var draft = sentences.join(" ");
    var unitText3 = ["mark updated"].concat(units.updated.map(unitText2)).concat(["", "mark no changes"]).concat(units.none.map(unitText2)).join("\n");

    var h = '<div class="closeout">';
    h += '<div class="cohead"><h2>Close-out' + (where ? ": " + esc(where) : "") + "</h2>" +
      '<p class="muted">The end-of-state rows of the QC/Country checklist. Not one plant: this panel adds up the calls made so far so the sheet and doc updates can be typed from it. ' +
      "Nothing on it is saved; make the calls on the plants, then come back here. " + link("checklist", "QC/Country checklist tab") + "</p></div>";

    h += "<section><h3>Research status per unit " + row(53) + "</h3>" +
      '<p>In the database, every unit the state sweep touched is set to "updated" or "no changes". The lists below come from the decisions on this page. Units the sweep did not touch are not listed; their status is yours to set.</p>' +
      unitList("mark updated", units.updated, "at least one change on the unit was accepted") +
      unitList("still open: decide before marking", units.open, "the unit has changes that are undecided, held, or sent back with a suggestion") +
      unitList("mark no changes", units.none, "every change on the unit was rejected: the current values stand") +
      (itemsOnly.length ? '<details class="colist"><summary>plants with items only <span class="n">(' + itemsOnly.length + ")</span></summary><p class=\"muted\">no cell changes were staged, only questions or watch items; the research status is your call</p><ul>" +
        itemsOnly.map(function (p) { return "<li>" + esc(p.name) + ' <span class="n">(' + plural(p.items.length, "item") + ")</span></li>"; }).join("") + "</ul></details>" : "") +
      (units.updated.length || units.none.length ? '<p><button type="button" class="ghost" data-copy="units">copy the unit lists</button> <span class="muted">(plant, unit, GEM unit id; one per line)</span></p>' : "") +
      "</section>";

    h += "<section><h3>" + (us ? "United States research row for the state " + row(35) + " " + row(29) : "Country tips and trends row " + row(29)) + "</h3>" +
      "<p>A draft for the state's row, from the counts on this page. Edit it before pasting. " + link(us ? "us_research" : "country_tips", us ? "United States research tab" : "Country tips trends tab") + "</p>" +
      '<blockquote class="draft">' + esc(draft) + "</blockquote>" +
      '<p><button type="button" class="ghost" data-copy="draft">copy the draft</button></p></section>';

    h += "<section><h3>Assignments tab, columns M and N " + row(30) + "</h3>" +
      '<p>On the ' + link("assignments", "Researcher Country Assignments tab") + ' the state\'s row has two columns the researcher fills: M is the best estimate in days for the next update, N is the status for this cycle (to do, in progress, done). ' +
      'Set N to done only after the units above are marked and the validation report comes back clean.</p></section>';

    h += "<section><h3>Sheets and docs to review and update " + row(31) + " " + row(32) + " " + (us ? row(34) + " " + row(36) : row(33)) + "</h3><ul>" +
      "<li>" + link("possible_updates", "GEM trackers possible updates sheet") + ": " + (toSheet.length ? plural(toSheet.length, "watch item") + " on this page " + (toSheet.length === 1 ? "was" : "were") + " sent there; the actions workbook has them on a sheet in the possible-updates column order, ready to paste." : "no watch item on this page was sent there.") +
      " Rows for this state already on the sheet are marked done or moved to the next cycle.</li>" +
      "<li>" + link("data_sources", "Gas and oil power plant data sources by country doc") + ": add any source the sweep used that the doc does not list yet (the evidence file names every source).</li>" +
      (us ? "<li>" + link("us_irps", "US IRPs tab") + ": the state's utility resource plans. " + (irpRecs.length ? plural(irpRecs.length, "record") + " on this page " + (irpRecs.length === 1 ? "comes" : "come") + " from a plan (the IRP chip); the actions workbook's irp_notes_draft sheet has a draft line per utility for the tab's Notes column." : "No record on this page comes from a plan. If the IRP step did not run for this state, read the state's rows by hand.") + "</li>" +
            "<li>" + link("us_guide", "GOGPT United States Data/Research Guide") + ": the state's section, if the sweep found a better source or a way in.</li>"
          : "<li>" + link("europe_doc", "Europe Workflow Map doc") + " (Europe only): the country's section.</li>") +
      "</ul></section>";

    if (us) {
      h += "<section><h3>IRP box " + row(37) + "</h3>" +
        "<p>The database has an IRP checkbox on every unit (the export's IRP column). A unit whose data comes from a utility integrated resource plan gets the box ticked. " +
        "The lists below pair the records on this page that come from a plan (the IRP chip) with the box as the export shows it.</p>" +
        (irpTick.length ? '<details class="colist" open><summary>tick the IRP box <span class="n">(' + irpTick.length + ")</span></summary><p class=\"muted\">a change from a plan sits on a unit whose box is not ticked yet; tick it in the web form when the change goes in</p><ul>" +
          irpTick.map(function (o) { return "<li>" + esc(plantOf(o).name) + " · " + esc(unitText(unitOf(plantOf(o), o.gem_unit_id), o.gem_unit_id)) + "</li>"; }).join("") + "</ul></details>" : "") +
        (irpNew.length ? '<details class="colist" open><summary>new rows from a plan <span class="n">(' + irpNew.length + ")</span></summary><p class=\"muted\">tick the IRP box on the new row when it is created</p><ul>" +
          irpNew.map(function (o) { return "<li>" + esc(plantOf(o).name) + (o.unit_name ? " · " + esc(o.unit_name) : "") + "</li>"; }).join("") + "</ul></details>" : "") +
        (irpDone.length ? '<details class="colist"><summary>already ticked <span class="n">(' + irpDone.length + ")</span></summary><p class=\"muted\">the box is ticked in the export; nothing to do</p><ul>" +
          irpDone.map(function (o) { return "<li>" + esc(plantOf(o).name) + " · " + esc(unitText(unitOf(plantOf(o), o.gem_unit_id), o.gem_unit_id)) + "</li>"; }).join("") + "</ul></details>" : "") +
        (irpUnknown.length ? '<details class="colist"><summary>check the box by hand <span class="n">(' + irpUnknown.length + ")</span></summary><p class=\"muted\">the record comes from a plan but names no unit the export shows; open the plant in the web form</p><ul>" +
          irpUnknown.map(function (o) { return "<li>" + esc(plantOf(o).name) + (o.unit_name ? " · " + esc(o.unit_name) : "") + "</li>"; }).join("") + "</ul></details>" : "") +
        (!irpRecs.length ? '<p class="muted">No record on this page comes from a plan. Units already ticked keep their box; the actions workbook\'s irp_box sheet lists them when the IRP step ran.</p>' : "") +
        "</section>";
    }

    h += "<section><h3>What this page cannot see " + row(52) + " " + row(54) + " " + row(56) + "</h3><ul>" +
      "<li><b>AI used</b> (row 52): yes. This batch was researched with Claude and reviewed here.</li>" +
      "<li><b>Validation report</b> (row 54): Baird runs the database's validation report for the state at close-out; it has to come back clean before the row is marked done.</li>" +
      '<li><b>No tracker found</b> (row 56): the combustion tracker search in the GEM database has a "no tracker found" filter. Baird runs that check from the database side; the page cannot.</li>' +
      "</ul></section>";

    if (held.length) h += "<section><h3>Watch items held, with notes</h3><p>Still on the watch list after this review. They come back on the next rebuild.</p><ul>" +
      held.map(function (it) { return "<li>" + esc(plantOf(it).name) + ": " + esc(itemHead(it)) + (it.call_note ? ' <span class="muted">' + esc(it.call_note) + "</span>" : "") + "</li>"; }).join("") + "</ul></section>";
    if (pm) h += "<section><h3>Questions for the project manager</h3><p>" + plural(pm, "question") + ' flagged on this page. <a href="#/?pm=1">show them</a>. The evidence file gathers them in one place.</p></section>';
    h += "</div>";
    S.closeoutCopy = {units: unitText3, draft: draft};
    return h;
  }
  function renderCard() {
    var card = $("card");
    if (S.closeout) { card.innerHTML = closeoutHtml(); S.shown = []; return; }
    if (S.pipe < 0) { card.innerHTML = '<div class="empty">nothing matches the filters.</div>'; S.shown = []; return; }
    var p = D.plants[S.pipe], q = FS.q.trim().toLowerCase();
    var un = unitNames(p);
    var ctx = [p.statewide && "<b>statewide notes, not one plant</b>", untracked(p) && !p.statewide && "<b>not in GEM yet: a candidate plant</b>",
               p.state && esc(p.state), p.units.length && p.units.length + " unit" + (p.units.length === 1 ? "" : "s") + " in the export",
               tierSummary(p), '<span class="pmplant">' + pmBox(p, "data-pmplant", p.pid) + "</span>"]
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
      var inView = bySev[s].filter(function (l) { return match(l, p, FS, null, FS.q.trim().toLowerCase()); }).length;
      var hid = bySev[s].length - inView;
      return '<button type="button" role="tab" data-tab="' + s + '" aria-selected="' + (S.tab === s) + '"' + tipAttrs(hid ? SEV_TIP[s] + ". The filters show " + inView + " of " + bySev[s].length + " here; the count below ignores them" : SEV_TIP[s]) + ">" +
        SEV_LABEL[s] + " " + todo(openS, bySev[s].length) + (hid ? ' <span class="n">&middot; ' + inView + " shown</span>" : "") + "</button>";
    }).join("") +
      '<button type="button" role="tab" data-tab="items" aria-selected="' + (S.tab === "items") + '"' + (p._ni < p.items.length && itemsInView(FS) ? tipAttrs("the filters show " + p._ni + " of this plant's " + p.items.length + " items here; this tab lists all of them, and the count ignores the filters") : "") + ">items " + todo(nOpenItems, p.items.length) + (p._ni < p.items.length && itemsInView(FS) ? ' <span class="n">&middot; ' + p._ni + " shown</span>" : "") + "</button>" +
      '<button type="button" role="tab" data-tab="all" aria-selected="' + (S.tab === "all") + '"' + tipAttrs("every change (filters ignored) and every item on this plant; also: click the name") + '>everything</button></div></div>';
    if (S.tab === "items") {
      S.shown = []; S.line = -1;
      // with a checklist group or the PM filter on, the items tab shows the matching items only
      card.innerHTML = h + itemsHtml(p, S.pin !== S.pipe && (FS.group || FS.pm || isItemKind(FS.kind)));
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
    l.reference = r.undecided ? "" : (r.reference || "");
    l.decision_note = r.undecided ? "" : (r.note || "");
  }
  function applyItemRecord(r) {
    var it = ITEM_BY_KEY[r.key];
    if (!it) return;
    it.call = r.undecided ? null : r.call;
    it.call_note = r.undecided ? null : r.note;
    it.call_reference = r.undecided ? "" : (r.reference || "");
    it.reviewed = !r.undecided;
    it.decided_by = r.undecided ? null : r.reviewer;
    it.decided_at = r.undecided ? null : r.ts;
  }
  // an ask-the-PM flag: key "pm::<line or item key>", or "pm::<dir>::plant:<pid>" for a whole plant
  function applyFlagRecord(r) {
    var key = String(r.key || "").replace(/^pm::/, ""), o = LINE_BY_KEY[key] || ITEM_BY_KEY[key];
    if (!o && r.kind === "plant") D.plants.forEach(function (p) { if (p.pid === r.pid && (!r.dir || p.dir === r.dir)) o = p; });
    if (!o) return;
    o.pm_flag = !!r.on && !r.undecided;
    o.pm_note = o.pm_flag ? (r.note || "") : "";
    o.pm_by = o.pm_flag ? r.reviewer : null;
  }
  function applySaved(saved) {
    saved.forEach(function (r) { if ("flag" in r) applyFlagRecord(r); else if ("call" in r) applyItemRecord(r); else applyRecord(r); });
  }
  // Save an ask-the-PM flag (line, item or plant). The box re-renders when the server confirms.
  function saveFlag(target, rec) {
    if (!Store.caps.decide) return notYet();
    var k = "pm:" + (rec.key || rec.pid);
    if (S.saving[k]) return;
    S.saving[k] = true;
    Store.flag([rec]).then(function (saved) {
      applySaved(saved);
      if (target && target.key) S.stay[target.key] = true;
      banner("");
      var keepLine = S.line;
      refilter(true);
      if (keepLine >= 0 && $("line-" + keepLine)) setLine(keepLine, true);
      toast(rec.on ? "flagged for the PM" : "flag removed");
    }).catch(function (e) {
      renderCard();
      toast("not saved: " + e.message);
    }).then(function () { delete S.saving[k]; });
  }
  function onPmChange(e) {
    var box = e.target.closest("input[data-pm], input[data-pm-note]"), pb = e.target.closest("input[data-pmplant], input[data-pmplant-note]");
    var t = box || pb;
    if (!t) return false;
    var isNote = t.hasAttribute("data-pm-note") || t.hasAttribute("data-pmplant-note");
    if (box) {
      var key = t.getAttribute(isNote ? "data-pm-note" : "data-pm"), o = LINE_BY_KEY[key] || ITEM_BY_KEY[key];
      if (!o) return true;
      var wrap = t.closest(".controls, .icall"), cb = wrap.querySelector("input[data-pm]"), nt = wrap.querySelector("input[data-pm-note]");
      var on = cb.checked, note = nt ? nt.value : (o.pm_note || "");
      if (isNote && on && note === (o.pm_note || "")) return true;
      saveFlag(o, {key: key, on: on, note: on ? note : ""});
      return true;
    }
    var p = D.plants[S.pipe];
    if (!p) return true;
    var pw = t.closest(".pmplant"), pcb = pw.querySelector("input[data-pmplant]"), pnt = pw.querySelector("input[data-pmplant-note]");
    var pon = pcb.checked, pnote = pnt ? pnt.value : (p.pm_note || "");
    if (isNote && pon && pnote === (p.pm_note || "")) return true;
    saveFlag(null, {pid: p.pid, dir: p.dir, on: pon, note: pon ? pnote : ""});
    return true;
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
    if (onPmChange(e)) return;
    var sel = e.target.closest("select[data-icall]"), inp = e.target.closest("input[data-inote]"), ref = e.target.closest("input[data-iref]");
    var t = sel || inp || ref;
    if (!t) return;
    var it = ITEMS[+t.getAttribute(sel ? "data-icall" : inp ? "data-inote" : "data-iref")];
    if (!it) return;
    var box = t.closest(".icall"), call = box.querySelector("select").value, note = box.querySelector("input[data-inote]").value,
        reference = (box.querySelector("input[data-iref]") || {}).value || "";
    if (!call) { if (sel && it.call) saveItem(it, {key: it.key, undo: true}); return; }
    if (!sel && call === it.call && note === (it.call_note || "") && reference === (it.call_reference || "")) return;
    if (NOTE_REQUIRED[it.kind + ":" + call] && !note.trim()) {
      var st = $("istat-" + it._i);
      if (st) { st.textContent = "say why in the note, then it saves"; st.className = "dstat err"; }
      if (sel) box.querySelector("input[data-inote]").focus();
      return;
    }
    saveItem(it, {key: it.key, call: call, note: note, reference: reference});
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
      '<label>source link <input type="url" class="sr" autocomplete="off" placeholder="https://… (where the value is stated)"></label>' +
      '<button type="submit" class="sv-save">save suggestion</button><button type="button" class="sv-cancel">cancel (esc)</button>' +
      '<span class="faint sv-err" role="alert"></span>';
    var sv = f.querySelector(".sv"), sn = f.querySelector(".sn"), sr = f.querySelector(".sr"), err = f.querySelector(".sv-err");
    sv.value = prior ? (l.suggested_value || "") : suggestPrefill(l);
    sn.value = prior ? (l.decision_note || "") : "";
    sr.value = prior ? (l.reference || "") : "";
    f.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); closeSuggest(); }
    });
    f.querySelector(".sv-cancel").onclick = closeSuggest;
    f.onsubmit = function (e) {
      e.preventDefault();
      if (blankv(sv.value) && blankv(sn.value)) { err.textContent = "give a suggested value or a note"; return; }
      if (!blankv(sr.value) && !/^https?:\/\/\S+$/.test(sr.value.trim())) { err.textContent = "the source link must start with http:// or https://"; return; }
      var b = f.querySelector(".sv-save"); b.disabled = true;
      if (S.saving[l.key]) return;
      S.saving[l.key] = true;
      Store.decide([{key: l.key, decision: "suggest", suggested_value: sv.value, note: sn.value, reference: sr.value.trim()}]).then(function (saved) {
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
    "<li><b>Items</b> tab: questions the researcher raised, plants and projects to watch, and owners or operators to create. They take a call and a note, but they never change a cell.</li>" +
    "<li><b>Checklist:</b> every change and item is sorted into one of the groups of the GOGPT QC/Country checklist (the \"checklist N\" chip; hover it for the rows it ticks). " +
    "The <b>checklist</b> button over the left list shows the groups with how much of each is still open, and a click on a group filters the plants to it. A group with nothing open gets a check mark. " +
    "The last group, <b>close-out</b>, is not a filter: it opens a panel with the end-of-state rows (units to mark updated or no changes, a draft for the state's summary row, the sheets and docs to update), all added up from the calls made so far.</li>" +
    "</ul>" +
    "<h4>your four calls</h4>" +
    "<ul>" +
    "<li><b>accept:</b> yes, this edit goes into the actions workbook.</li>" +
    "<li><b>hold:</b> not sure yet, leave it open.</li>" +
    "<li><b>reject:</b> no, do not apply this.</li>" +
    "<li><b>suggest:</b> something else is right, so type the value or a note, and the source link if you have one. The researcher looks at it again; it does not go into the workbook as is.</li>" +
    "</ul>" +
    "<p><b>Ask the PM:</b> a checkbox beside every change, every item and at the top of every plant. It sits beside your decision, so you can accept something and still flag it. " +
    "Write the question in the box that appears. The <b>ask the PM</b> filter lists everything flagged; the evidence file gathers the questions in one place.</p>" +
    "<h4>the four kinds of item</h4>" +
    "<ul>" +
    "<li><b>Question about existing data:</b> the researcher doubts something already in GEM: a value that could not be checked, two sources that disagree, a possible duplicate. " +
    "Calls: <b>confirmed</b> (the question stands and goes into the evidence file), <b>dismissed</b> (closed), <b>needs research</b> (back to the researcher).</li>" +
    "<li><b>Watch item, new to the tracker:</b> a plant or project GEM does not track at all yet. It did not clear the bar for a new row (too early, too small, or thin on evidence), so it is on a watchlist instead.</li>" +
    "<li><b>Watch item, existing plant:</b> something to keep an eye on at a plant GEM already tracks: a permit in progress, an expansion, a retirement date to confirm. The plant's row is not changed by the item.</li>" +
    "<li><b>New owner or operator to create:</b> a company that is not in GEM's entity list. Someone creates it in the GEM web form before the ownership edit can land.</li>" +
    "</ul>" +
    "<p><b>IRP chip</b> (United States only): the finding comes from a utility integrated resource plan. The chip says whether the unit's IRP box in the database is already ticked; \"IRP: tick the box\" means it is not. The close-out panel lists them under row 37.</p>" +
    "<p><b>Watch items take four calls</b> instead of accept and reject: <b>incorporate into database</b> (it belongs in GEM now; the researcher writes it up as a full edit for the next batch), " +
    "<b>hold</b> (keep watching), <b>send to possible updates</b> (park it on the possible-updates sheet for a later cycle), and <b>remove from watchlist</b> (drop it, with a note saying why). " +
    "A candidate staged in two batches shows an \"also staged in\" chip: decide it once and give the copy the same call.</p>" +
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
    "<li><b>Undo:</b> click the pressed button again, or press <kbd>u</kbd>. Nothing is deleted; the log just records the undo. Unticking <b>ask the PM</b> works the same way.</li>" +
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
    var cp = e.target.closest("button[data-copy]");
    if (cp) { var what = cp.getAttribute("data-copy"); copyText((S.closeoutCopy || {})[what] || "", what === "draft" ? "draft copied" : "unit lists copied"); return; }
    if (e.target.closest(".pmbox, .pmnote")) return;       // the ask-the-PM box saves on change, not on click
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
  var QK = {decision: "d", kind: "k", group: "g", tier: "t", dir: "dir", column: "col", q: "q", country: "c", state: "st", by: "by", status: "status", pm: "pm"};
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
      S.pin = -1; S.closeout = false;
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
      if (synced && Store.requestPush && !$("ledger-btn")) {
        var pb = document.createElement("button");
        pb.id = "ledger-btn"; pb.type = "button"; pb.className = "ghost"; pb.textContent = "push to ledger";
        pb.dataset.tip = "save your calls to the shared log and ask Claude to import them into the batch logs; nothing is written to the tracker";
        pb.onclick = function () {
          Promise.resolve(Store.requestPush()).then(function (r) {
            toast("push to ledger requested: " + r.count + " call" + (r.count === 1 ? "" : "s") + " in the shared log");
          }, function (e) { toast(e && e.message ? e.message : "the request did not go through"); });
        };
        ex.parentNode.insertBefore(pb, ex.nextSibling);
      }
      var st = Store.status ? Store.status() : {state: "local"};
      if (st.state === "error") { STICKY = st.message; banner(); }
      else if (!synced && !Store.storageOk()) { STICKY = "this browser is not keeping the log between visits (private window or storage blocked): download your decisions before closing the tab"; banner(); }
    }
    renderScope();
    document.querySelector(".top h1").dataset.tip = "built " + et(D.built) + " · " + D.dirs.length + " staging folder" + (D.dirs.length === 1 ? "" : "s") + ": " +
      D.dirs.map(dirLabel).join(", ") + (D.scope.quarter ? " · " + D.scope.quarter : "");
    initFilters();
    var view = "plants";
    try { view = localStorage.getItem("review-view") || "plants"; } catch (e) { /* ignore */ }
    if (view === "checklist" && !(D.groups || []).length) view = "plants";
    setView(view);
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
  // A press anywhere outside the open suggest form closes it, same as cancel.
  document.addEventListener("mousedown", function (e) {
    var f = document.querySelector("#card .sform");
    if (f && !f.contains(e.target)) closeSuggest();
  });
  $("card").addEventListener("click", onCardClick);
  $("pipes").addEventListener("click", function (e) {
    var li = e.target.closest("li[data-i]");
    if (li) return selectPipe(+li.getAttribute("data-i"));
    var g = e.target.closest("li[data-g]");
    if (g) selectGroup(g.getAttribute("data-g"));
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
    if (d && d.classList && d.classList.contains("igroup")) S.igOpen[d.getAttribute("data-g")] = d.open;
  }, true);
  Promise.all([Store.whoami(), Store.load()]).then(function (r) { boot(r[0], r[1]); })
    .catch(function (e) { banner("could not load the dataset: " + e.message); });
})();
