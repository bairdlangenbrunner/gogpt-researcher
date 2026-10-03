/* Store adapter for the single-file review page (review_app/build_static.py). Same interface as
   the loopback adapter at the top of app.js (caps, load, whoami, decide, item), but there is no
   server: the dataset is embedded in the page and every call is appended to a log kept in this
   browser (localStorage, falling back to memory). "download decisions" hands the reviewer the
   log to send back; review_app/import_log.py appends it to the staging dirs. The GEM database is
   never touched.

   Opened as a claude.ai artifact, the page also keeps the log in the artifact's own database
   (one document per reviewer under logs/, the whole log in `records`), so the sender reads it
   back directly and the download is only a backup. Opened from disk there is no window.claude
   and the page runs on the browser log alone.

   The page sets window.REVIEW_STATIC = {reviewer, data} before this file runs; app.js picks the
   adapter up as window.StaticStore. */
(function () {
  "use strict";
  var cfg = window.REVIEW_STATIC || {};
  var DATA = cfg.data || {plants: [], dirs: []};
  var REVIEWER = cfg.reviewer || "reviewer";
  var DECISIONS = {accept: 1, hold: 1, reject: 1, suggest: 1};
  var LINE_KINDS = {fill: 1, change: 1, reverified: 1, "delete": 1, plant: 1, new_row: 1};
  var ITEM_CALLS = {concern: ["confirmed", "dismissed", "needs_research"]};
  var OTHER_CALLS = ["noted", "todo", "dismissed"];
  var LOG_KEY = "review-log:" + (DATA.built || "") + ":" + (DATA.dirs || []).join(",");
  var LOG = [];              // every record this browser has written for this build, in order
  var STORAGE_OK = true;
  // the artifact database, when the page is viewed as a claude.ai artifact
  var SYNC = {state: "local", message: "", db: null, dl: null, doc: null, chain: Promise.resolve()};

  function readLog() {
    try {
      var raw = localStorage.getItem(LOG_KEY);
      if (raw) LOG = JSON.parse(raw);
    } catch (e) { STORAGE_OK = false; }
  }
  function saveLog() {
    try { localStorage.setItem(LOG_KEY, JSON.stringify(LOG)); STORAGE_OK = true; }
    catch (e) { STORAGE_OK = false; }
  }
  // key -> (plant, object, group) for every line and item
  function index() {
    var out = {};
    DATA.plants.forEach(function (p) {
      ["lines", "items"].forEach(function (grp) {
        (p[grp] || []).forEach(function (o) { out[o.key] = {plant: p, obj: o, grp: grp}; });
      });
    });
    return out;
  }
  var IDX = index();
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  // ISO seconds in Eastern time with its offset, like store.now(): 2026-10-02T17:41:03-04:00
  function now() {
    var d = new Date(), parts = {};
    try {
      new Intl.DateTimeFormat("en-US", {timeZone: "America/New_York", hourCycle: "h23", year: "numeric", month: "2-digit",
        day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit"}).formatToParts(d)
        .forEach(function (p) { parts[p.type] = p.value; });
      var asUtc = Date.UTC(+parts.year, +parts.month - 1, +parts.day, +parts.hour, +parts.minute, +parts.second);
      var off = Math.round((asUtc - d.getTime()) / 60000), sign = off < 0 ? "-" : "+";
      off = Math.abs(off);
      return parts.year + "-" + parts.month + "-" + parts.day + "T" + parts.hour + ":" + parts.minute + ":" + parts.second +
        sign + pad(Math.floor(off / 60)) + ":" + pad(off % 60);
    } catch (e) {
      return d.toISOString().slice(0, 19) + "Z";
    }
  }
  function fail(msg) { return Promise.reject(new Error(msg)); }
  function str(v) { return String(v == null ? "" : v); }
  // mirror of store.initials for a viewer's profile name: "Amalia Llano" -> "AL"
  function initials(name) {
    var parts = str(name).trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return "";
    if (/^[A-Z]{1,4}$/.test(parts.join(""))) return parts.join("");
    return (parts[0][0] + (parts.length > 1 ? parts[parts.length - 1][0] : "")).toUpperCase();
  }

  // mirror of store.validate: {key, decision, suggested_value?, note?} or {key, undo: true}
  function validateLines(records) {
    if (!Array.isArray(records) || !records.length) throw new Error("expected a non-empty list of decision records");
    return records.map(function (r, i) {
      var e = IDX[r && r.key];
      if (!e) throw new Error("record " + i + ": unknown key " + str(r && r.key));
      if (e.grp !== "lines" || !LINE_KINDS[e.obj.kind]) throw new Error("record " + i + ": " + r.key + " is an item, not a line");
      var undo = !!(r.undo || r.undecided), decision = r.decision;
      if (undo && !decision) decision = e.obj["default"] || "hold";
      if (!undo && !decision) throw new Error("record " + i + ": no decision given");
      if (!DECISIONS[decision]) throw new Error("record " + i + ": decision " + decision + " is not one of accept, hold, reject, suggest");
      var note = str(r.note), sv = str(r.suggested_value);
      if (decision === "suggest" && !undo && !sv.trim() && !note.trim()) throw new Error("record " + i + ": a suggestion needs a suggested_value or a note");
      return {key: r.key, dir: e.obj.dir, pid: e.plant.pid, record_id: e.obj.record_id || null, column: e.obj.column || "",
              kind: e.obj.kind, decision: decision, suggested_value: sv, note: note, reviewer: REVIEWER, ts: null, undecided: undo};
    });
  }
  // mirror of store.validate_items: {key, call, note?} or {key, undo: true}
  function validateItems(records) {
    if (!Array.isArray(records) || !records.length) throw new Error("expected a non-empty list of item records");
    return records.map(function (r, i) {
      var e = IDX[r && r.key];
      if (!e) throw new Error("record " + i + ": unknown key " + str(r && r.key));
      if (e.grp !== "items") throw new Error("record " + i + ": " + r.key + " is a line, not an item");
      var undo = !!(r.undo || r.undecided), call = undo ? "" : str(r.call);
      var vocab = ITEM_CALLS[e.obj.kind] || OTHER_CALLS;
      if (!undo && vocab.indexOf(call) < 0) throw new Error("record " + i + ": call " + call + " is not one of " + vocab.join(", ") + " for a " + e.obj.kind + " item");
      return {key: r.key, dir: e.obj.dir, pid: e.plant.pid, record_id: e.obj.record_id || null, kind: e.obj.kind,
              call: call, note: str(r.note), reviewer: REVIEWER, ts: null, undecided: undo};
    });
  }
  function write(recs) {
    var ts = now();
    recs.forEach(function (r) { r.ts = ts; LOG.push(r); });
    saveLog();
    push();
    return Promise.resolve(recs);
  }
  // lay this browser's log over the embedded dataset (the sender already laid the committed log
  // over it at build time), latest record per key; mirror of store.overlay
  function overlay(data) {
    var last = {};
    LOG.forEach(function (r) { if (r.key) last[r.key] = r; });
    data.plants.forEach(function (p) {
      ["lines", "items"].forEach(function (grp) {
        (p[grp] || []).forEach(function (o) {
          var rec = last[o.key];
          if (!rec) return;
          var live = rec.undecided ? null : rec;
          if (grp === "lines") {
            o.decision = live ? live.decision : null;
            o.suggested_value = live && live.decision === "suggest" ? live.suggested_value || "" : "";
            o.decision_note = live && live.decision === "suggest" ? live.note || "" : "";
          } else {
            o.call = live ? live.call : null;
            o.call_note = live ? live.note || "" : null;
          }
          o.reviewed = !!live;
          o.decided_by = live ? live.reviewer : null;
          o.decided_at = live ? live.ts : null;
        });
      });
    });
    return data;
  }

  // ---- the artifact database ----
  function fingerprint(r) {
    return [r.key, r.ts, r.reviewer, r.decision || "", r.call || "", !!r.undecided, r.suggested_value || "", r.note || ""].join("\u0001");
  }
  // union of the browser log and the database copy, in time order; the browser's own order wins
  // on equal stamps
  function merge(remote) {
    var seen = {}, out = [];
    LOG.concat(remote || []).forEach(function (r, i) {
      if (!r || !r.key || !r.ts) return;
      var f = fingerprint(r);
      if (seen[f]) return;
      seen[f] = 1; out.push({r: r, i: i});
    });
    out.sort(function (a, b) { return a.r.ts < b.r.ts ? -1 : a.r.ts > b.r.ts ? 1 : a.i - b.i; });
    return out.map(function (x) { return x.r; });
  }
  function segment(s) { return str(s).replace(/[^A-Za-z0-9_\-.~:@+]/g, "_").slice(0, 120) || "x"; }
  function push() {
    if (!SYNC.doc) return;
    var snapshot = LOG.slice();
    SYNC.chain = SYNC.chain.then(function () {
      return SYNC.doc.set({reviewer: REVIEWER, built: DATA.built || "", dirs: DATA.dirs || [], updated: now(), records: snapshot});
    }).then(function () { SYNC.state = "synced"; SYNC.message = ""; }, function (e) {
      SYNC.state = "error"; SYNC.message = "the page could not save to the artifact (" + ((e && e.code) || (e && e.message) || "unknown") +
        "): your calls are kept in this browser; use download decisions before closing";
      if (window.ReviewApp && window.ReviewApp.banner) window.ReviewApp.banner(SYNC.message);
    });
    return SYNC.chain;
  }
  function connect() {
    if (!window.claude || typeof window.claude.use !== "function") return Promise.resolve();
    return Promise.all([window.claude.use("db"), window.claude.use("downloads"), window.claude.use("user")]).then(function (ns) {
      SYNC.db = ns[0]; SYNC.dl = ns[1];
      var user = ns[2];
      if (!SYNC.db) return;
      var uid = user && user.id ? user.id() : Promise.resolve(null);
      var me = user && user.me ? user.me() : Promise.resolve(null);
      return Promise.all([uid, me]).then(function (u) {
        var who = u[1] && u[1].name ? initials(u[1].name) : "";
        if (who) REVIEWER = who;                       // the viewer's own initials, not the build's
        SYNC.doc = SYNC.db.doc("logs/" + segment(REVIEWER + (u[0] ? "~" + u[0] : "")));
        return SYNC.doc.get();
      }).then(function (snap) {
        var body = snap && snap.exists ? snap.data() : null;
        var remote = body && Array.isArray(body.records) ? body.records : [];
        var merged = merge(remote), had = LOG.length;
        LOG = merged; saveLog();
        SYNC.state = "synced";
        if (merged.length !== remote.length || had !== merged.length) return push();
      });
    }).catch(function (e) {
      SYNC.state = "error";
      SYNC.message = "the page could not open the artifact's database (" + ((e && e.code) || (e && e.message) || "unknown") +
        "): your calls are kept in this browser only; use download decisions before closing";
    });
  }
  function download() {
    var stamp = now().slice(0, 16).replace(/[-:]/g, "").replace("T", "_");
    var base = "review_log_" + (DATA.dirs || []).map(function (d) {
      var parts = d.split("/").filter(Boolean); if (parts[parts.length - 1] === "staging") parts.pop(); return parts[parts.length - 1] || d;
    }).join("+") + "_" + REVIEWER + "_" + stamp + "_ET";
    var count = LOG.length;
    if (SYNC.dl) {    // the artifact viewer saves files itself; .json is on its list, .jsonl is not
      var name = base + ".json";
      var body = JSON.stringify({reviewer: REVIEWER, built: DATA.built || "", dirs: DATA.dirs || [], records: LOG}, null, 1);
      return SYNC.dl.save({filename: name, data: body}).then(function () { return {name: name, count: count}; },
        function (e) { throw new Error(e && e.code === "declined" ? "download cancelled" : (e && e.message) || "download failed"); });
    }
    var text = LOG.map(function (r) { return JSON.stringify(r); }).join("\n") + (LOG.length ? "\n" : "");
    var fname = base + ".jsonl";
    var blob = new Blob([text], {type: "application/x-ndjson;charset=utf-8"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = fname;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    return Promise.resolve({name: fname, count: count});
  }

  readLog();
  var READY = connect();
  window.StaticStore = {
    mode: "static",
    caps: {decide: true},
    get reviewer() { return REVIEWER; },
    storageOk: function () { return STORAGE_OK; },
    // "synced": the log is also in the artifact's database; "local": this browser only; "error": see message
    status: function () { return {state: SYNC.state, message: SYNC.message}; },
    count: function () { return LOG.length; },
    load: function () { return READY.then(function () { return overlay(JSON.parse(JSON.stringify(DATA))); }); },
    whoami: function () { return READY.then(function () { return REVIEWER; }); },
    decide: function (records) { try { return write(validateLines(records)); } catch (e) { return fail(e.message); } },
    item: function (records) { try { return write(validateItems(records)); } catch (e) { return fail(e.message); } },
    download: download,
    // for tests and for a reviewer who wants to look: the raw log
    log: function () { return LOG.slice(); }
  };
})();
