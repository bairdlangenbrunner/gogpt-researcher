/* Store adapter for the single-file review page (review_app/build_static.py). Same interface as
   the loopback adapter at the top of app.js (caps, load, whoami, decide, item), but there is no
   server: the dataset is embedded in the page and every call (decision, item call, ask-the-PM
   flag) is appended to a log kept in this browser (localStorage, falling back to memory). "download decisions" hands the reviewer the
   log to send back; review_app/import_log.py appends it to the staging dirs. The GEM database is
   never touched.

   Opened as a claude.ai artifact, the page also keeps the log in the artifact's own database
   (one document per viewer under logs/, named by the viewer's id, the whole log in `records`),
   so the sender reads it back directly and the download is only a backup. A viewer the
   artifact does not let write (not shared with them as an editor, or outside the owner's
   organization) is told so in the banner and keeps the log in the browser. Opened from disk
   there is no window.claude and the page runs on the browser log alone.

   The page sets window.REVIEW_STATIC = {reviewer, data} before this file runs; app.js picks the
   adapter up as window.StaticStore. */
(function () {
  "use strict";
  var cfg = window.REVIEW_STATIC || {};
  var DATA = cfg.data || {plants: [], dirs: []};
  var REVIEWER = cfg.reviewer || "reviewer";
  var DECISIONS = {accept: 1, hold: 1, reject: 1, suggest: 1};
  var LINE_KINDS = {fill: 1, change: 1, reverified: 1, "delete": 1, plant: 1, new_row: 1};
  // must match review_app/store.py ITEM_CALLS / NOTE_REQUIRED / FLAG_PREFIX
  var ITEM_CALLS = {concern: ["confirmed", "dismissed", "needs_research"], monitor: ["add_to_database", "hold", "possible_updates", "remove"]};
  var OTHER_CALLS = ["noted", "todo", "dismissed"];
  var NOTE_REQUIRED = {"monitor:remove": 1};
  var FLAG_PREFIX = "pm::";
  var URL_RE = /^https?:\/\/\S+$/;
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
    if (!LOG.length) carryOver();
  }
  // A rebuilt page has a new build stamp and so a new, empty log. Bring across the calls this
  // browser made on earlier builds of the same folders, for the records the rebuild still has
  // (record ids are stable across rebuilds). The earlier logs stay where they are.
  function carryOver() {
    var tail = ":" + (DATA.dirs || []).join(","), old = [];
    try {
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (!k || k === LOG_KEY || k.indexOf("review-log:") !== 0 || k.slice(-tail.length) !== tail) continue;
        var recs = JSON.parse(localStorage.getItem(k) || "[]");
        if (Array.isArray(recs)) old = old.concat(recs.filter(function (r) { return r && (IDX[r.key] || (r.flag && known(r))); }));
      }
    } catch (e) { return; }
    if (!old.length) return;
    LOG = merge(old);
    saveLog();
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
  function plantFlagKey(dir, pid) { return FLAG_PREFIX + str(dir) + "::plant:" + str(pid); }
  function plantByKey(key) {
    var hit = null;
    DATA.plants.forEach(function (p) { if (plantFlagKey(p.dir, p.pid) === key) hit = p; });
    return hit;
  }
  // a flag record names a line or item (pm::<key>) or a plant (pm::<dir>::plant:<pid>) this build has
  function known(r) {
    var key = str(r && r.key);
    if (key.indexOf(FLAG_PREFIX) !== 0) return false;
    return !!(IDX[key.slice(FLAG_PREFIX.length)] || plantByKey(key));
  }
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
      var note = str(r.note), sv = str(r.suggested_value), ref = str(r.reference).trim();
      if (decision === "suggest" && !undo && !sv.trim() && !note.trim()) throw new Error("record " + i + ": a suggestion needs a suggested_value or a note");
      if (ref && !URL_RE.test(ref)) throw new Error("record " + i + ": the reference must be a URL starting with http:// or https://");
      return {key: r.key, dir: e.obj.dir, pid: e.plant.pid, record_id: e.obj.record_id || null, column: e.obj.column || "",
              kind: e.obj.kind, decision: decision, suggested_value: sv, reference: undo ? "" : ref, note: note, reviewer: REVIEWER, ts: null, undecided: undo};
    });
  }
  // mirror of store.validate_items: {key, call, reference?, note?} or {key, undo: true}
  function validateItems(records) {
    if (!Array.isArray(records) || !records.length) throw new Error("expected a non-empty list of item records");
    return records.map(function (r, i) {
      var e = IDX[r && r.key];
      if (!e) throw new Error("record " + i + ": unknown key " + str(r && r.key));
      if (e.grp !== "items") throw new Error("record " + i + ": " + r.key + " is a line, not an item");
      var undo = !!(r.undo || r.undecided), call = undo ? "" : str(r.call), note = str(r.note), ref = str(r.reference).trim();
      var vocab = ITEM_CALLS[e.obj.kind] || OTHER_CALLS;
      if (!undo && vocab.indexOf(call) < 0) throw new Error("record " + i + ": call " + call + " is not one of " + vocab.join(", ") + " for a " + e.obj.kind + " item");
      if (!undo && NOTE_REQUIRED[e.obj.kind + ":" + call] && !note.trim()) throw new Error("record " + i + ": " + call.replace(/_/g, " ") + " needs a note saying why");
      if (ref && !URL_RE.test(ref)) throw new Error("record " + i + ": the reference must be a URL starting with http:// or https://");
      return {key: r.key, dir: e.obj.dir, pid: e.plant.pid, record_id: e.obj.record_id || null, kind: e.obj.kind,
              call: call, note: note, reference: undo ? "" : ref, reviewer: REVIEWER, ts: null, undecided: undo};
    });
  }
  // mirror of store.validate_flags: {key, on, note?} for a line or item, {pid, dir, on, note?} for a plant
  function validateFlags(records) {
    if (!Array.isArray(records) || !records.length) throw new Error("expected a non-empty list of flag records");
    return records.map(function (r, i) {
      if (!r) throw new Error("record " + i + ": empty");
      var on = !!r.on, note = str(r.note);
      if (r.key) {
        var e = IDX[r.key];
        if (!e) throw new Error("record " + i + ": unknown key " + str(r.key));
        return {key: FLAG_PREFIX + r.key, dir: e.obj.dir, pid: e.plant.pid, record_id: e.obj.record_id || null,
                kind: e.obj.kind, flag: "pm", on: on, note: note, reviewer: REVIEWER, ts: null, undecided: false};
      }
      var p = null;
      DATA.plants.forEach(function (x) { if (x.pid === r.pid && (!r.dir || x.dir === r.dir)) p = p || x; });
      if (!p) throw new Error("record " + i + ": unknown plant " + str(r.pid));
      return {key: plantFlagKey(p.dir, p.pid), dir: p.dir, pid: p.pid, record_id: null, kind: "plant", flag: "pm", on: on,
              note: note, reviewer: REVIEWER, ts: null, undecided: false};
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
    function flag(o, key) {
      var f = last[FLAG_PREFIX + key];
      if (!f) { if (o.pm_flag == null) { o.pm_flag = false; o.pm_note = ""; o.pm_by = null; } return; }
      o.pm_flag = !!f.on && !f.undecided;
      o.pm_note = o.pm_flag ? f.note || "" : "";
      o.pm_by = o.pm_flag ? f.reviewer : null;
    }
    data.plants.forEach(function (p) {
      flag(p, str(p.dir) + "::plant:" + str(p.pid));
      ["lines", "items"].forEach(function (grp) {
        (p[grp] || []).forEach(function (o) {
          flag(o, o.key);
          var rec = last[o.key];
          if (!rec) return;
          var live = rec.undecided ? null : rec;
          if (grp === "lines") {
            o.decision = live ? live.decision : null;
            o.suggested_value = live && live.decision === "suggest" ? live.suggested_value || "" : "";
            o.decision_note = live && live.decision === "suggest" ? live.note || "" : "";
            o.reference = live && live.decision === "suggest" ? live.reference || "" : "";
          } else {
            o.call = live ? live.call : null;
            o.call_note = live ? live.note || "" : null;
            o.call_reference = live ? live.reference || "" : "";
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
  var NO_WRITE = "this page is not allowed to save your calls to the artifact (it has to be shared with you by " +
    "email, as an editor, by the person who published it): your calls are kept in this browser; use download " +
    "decisions before closing";
  function saveError(e) {
    var code = (e && e.code) || "";
    if (code === "invalid_argument" || code === "not_granted" || code === "revoked") return NO_WRITE;
    return "the page could not save to the artifact (" + (code || (e && e.message) || "unknown") +
      "): your calls are kept in this browser; use download decisions before closing";
  }
  function fingerprint(r) {
    return [r.key, r.ts, r.reviewer, r.decision || "", r.call || "", !!r.undecided, r.suggested_value || "", r.reference || "", r.note || "",
            r.flag || "", r.flag ? String(!!r.on) : ""].join("\u0001");
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
      SYNC.state = "error"; SYNC.message = saveError(e);
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
      var can = user && user.can ? user.can("data.write") : Promise.resolve(null);
      return Promise.all([uid, me, can]).then(function (u) {
        var who = u[1] && u[1].name ? initials(u[1].name) : "";
        if (who) REVIEWER = who;                       // the viewer's own initials, not the build's
        if (u[2] === false) {                           // the artifact has said this viewer cannot write
          SYNC.state = "error"; SYNC.message = NO_WRITE; return null;
        }
        // one document per viewer, named by their id (their initials when the viewer has no id),
        // so every device they use merges into the same log
        SYNC.seg = segment(u[0] || REVIEWER);
        SYNC.doc = SYNC.db.doc("logs/" + SYNC.seg);
        return SYNC.doc.get();
      }).then(function (snap) {
        if (snap === null) return;
        var body = snap && snap.exists ? snap.data() : null;
        var remote = body && Array.isArray(body.records) ? body.records : [];
        var merged = merge(remote), had = LOG.length;
        LOG = merged; saveLog();
        SYNC.state = "synced";
        if (merged.length !== remote.length || had !== merged.length) return push();
      });
    }).catch(function (e) {
      SYNC.state = "error";
      SYNC.message = saveError(e);
    });
  }
  // "push to ledger": make sure the shared log is current, then leave a request document in the
  // `requests` collection for a Claude Code session watching this artifact (review_app/README.md).
  function requestPush() {
    if (!SYNC.db || !SYNC.doc) return Promise.reject(new Error("the shared log is not available here, so a push cannot be requested. Use download decisions."));
    if (!LOG.length) return Promise.reject(new Error("no calls yet; nothing to push"));
    var n = LOG.length;
    return Promise.resolve(SYNC.chain).then(function () {
      return SYNC.db.doc("requests/" + SYNC.seg + "~push").set({reviewer: REVIEWER, requested: now(), records: n,
        built: DATA.built || "", dirs: DATA.dirs || [], seq: Date.now(), status: "requested"});
    }).then(function () { return {count: n}; }, function (e) {
      throw new Error("the request did not go through (" + ((e && (e.code || e.message)) || "unknown") + ")");
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
    flag: function (records) { try { return write(validateFlags(records)); } catch (e) { return fail(e.message); } },
    download: download,
    requestPush: requestPush,
    // for tests and for a reviewer who wants to look: the raw log
    log: function () { return LOG.slice(); }
  };
})();
