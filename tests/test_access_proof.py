"""Access assurance (Baird 2026-11-03, Oklahoma planning: "I want to be ASSURED that
you're able to access any documents and websites that are helpful or relevant"):
access_check.py proves every listed source before the sweep and keeps the proof,
state_gate's `access-proof` gate refuses a batch without it, a searched coverage
entry carries what was read and when, and a harvester's failed reads reach the
access audit like any other read. No live network: fetch and gws are stubbed."""
import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import access_check  # noqa: E402
import access_audit  # noqa: E402
import fetch  # noqa: E402
import harvest_lib  # noqa: E402
from state_gate import gate_access_proof, gate_source_coverage, proof_strict  # noqa: E402

WHERE = {"kind": "state", "name": "Oklahoma", "slug": "oklahoma", "country": "United States", "postal": "ok"}
PDF = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF"
TABLE = "<html><table><tr><th>Company</th></tr><tr><td>OG&E</td></tr><tr><td>PSO</td></tr></table></html>"


@pytest.fixture(autouse=True)
def no_batch(monkeypatch):
    """Every test starts with GEM_BATCH unset and pytest puts it back afterwards (delenv
    alone records nothing when the variable is absent, so the setdefault in the code under
    test leaked into test_fetch_access the first time)."""
    monkeypatch.setenv("GEM_BATCH", "placeholder")
    monkeypatch.delenv("GEM_BATCH")


def stub_fetch(responses):
    """fetch_proof stand-in: url -> (status, content_type, raw, text, is_pdf, notes, final)."""
    def fn(url, proof, timeout):
        r = responses[url]
        raw = r.get("raw", b"")
        text = r.get("text", raw.decode("utf-8", "replace") if not raw.startswith(b"%PDF") else "permit text")
        is_pdf = r.get("is_pdf", raw.startswith(b"%PDF"))
        return r.get("status", "200"), r.get("ctype", ""), raw, text, is_pdf, r.get("notes", ["curl"]), url
    return fn


def listing(tmp_path, entries):
    lp = tmp_path / "coverage" / "us-ok.json"
    lp.parent.mkdir(parents=True, exist_ok=True)
    lp.write_text(json.dumps(entries), encoding="utf-8")
    return lp


def run_check(tmp_path, entries, responses, google=None):
    batch = tmp_path / "batches" / "us-ok"
    return access_check.run("us-ok", batch, fetch_fn=stub_fetch(responses),
                            google_fn=google or (lambda fid, t: (False, "no gws in tests", "")),
                            list_path=listing(tmp_path, entries), sample_dir=tmp_path / "samples"), batch


# ---------------------------------------------------------------- kinds ---

def test_a_pdf_the_ladder_read_counts_when_plain_curl_is_turned_away(tmp_path):
    # OG&E's investor host answers plain curl with a Cloudflare page but the browser-fingerprint
    # route reads the IRP PDF; the ladder's own %PDF check and the text it extracted are the proof
    entries = [{"id": "oge-irp", "name": "OG&E IRP", "url": "https://oge.example/irp",
                "proof": {"kind": "pdf", "expect": "Integrated Resource Plan"}}]
    proof, _ = run_check(tmp_path, entries, {"https://oge.example/irp": {
        "raw": b"", "text": "INTEGRATED RESOURCE PLAN 2026", "is_pdf": True, "notes": ["cf_impersonate", "pdf_via_ladder"]}})
    rec = proof["sources"]["oge-irp"]
    assert rec["ok"] and rec["route"] == "cf_impersonate, pdf_via_ladder" and rec["bytes"] > 0
    assert (tmp_path / "samples" / "oge-irp.txt").read_text(encoding="utf-8").startswith("INTEGRATED")


def test_kind_checks_tell_a_pdf_from_a_login_page():
    assert access_check.check_kind("pdf", PDF, "text", "application/pdf") == ""
    assert "not a PDF" in access_check.check_kind("pdf", b"<html>Sign in</html>", "Sign in", "text/html")
    assert access_check.check_kind("csv", b"a,b\n1,2\n3,4\n", "", "text/csv") == ""
    assert "rows" in access_check.check_kind("csv", b"a,b\n1,2\n", "", "text/csv", min_rows=5)
    assert "HTML" in access_check.check_kind("csv", b"<html><body>x</body></html>", "", "text/html")
    assert access_check.check_kind("json", b'{"a": 1}', "", "application/json") == ""
    assert "parse" in access_check.check_kind("json", b"<html>", "", "text/html")
    assert access_check.check_kind("table", b"", TABLE, "text/html") == ""
    assert "table rows" in access_check.check_kind("table", b"", "<html><div>drawn by script</div></html>", "text/html")
    assert "soft error" in access_check.check_kind("html", b"", "<html><title>Page Not Found</title></html>", "text/html")
    assert access_check.expect_missing("Horseshoe  Lake", "OG&E Horseshoe Lake unit 15") == ""
    assert "not on the page" in access_check.expect_missing("Mustang", "OG&E Horseshoe Lake")


# ---------------------------------------------------------------- check ---

def test_check_proves_each_listed_source_and_keeps_a_sample(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "FAIL_LOG", tmp_path / "failures.jsonl")
    entries = [
        {"id": "ppr", "name": "Permits table", "url": "https://deq.example/ppr",
         "proof": {"kind": "table", "min_rows": 1, "expect": "OG&E"}},
        {"id": "irp", "name": "IRP", "url": "https://occ.example/irp.pdf", "proof": {"kind": "pdf"}},
        {"id": "ecf", "name": "Case filing", "url": "https://ecf.example/", "human_wall": "Baird registers an account",
         "proof": {"kind": "html"}},
        {"id": "news", "name": "News", "url": "https://news.example/search"},
    ]
    responses = {
        "https://deq.example/ppr": {"raw": TABLE.encode(), "text": TABLE, "ctype": "text/html", "notes": ["insecure_tls"]},
        "https://occ.example/irp.pdf": {"raw": PDF, "ctype": "application/pdf"},
        "https://ecf.example/": {"status": "401", "raw": b"", "text": ""},
        "https://news.example/search": {"status": "403", "raw": b"", "text": "", "notes": ["cf_impersonate"]},
    }
    out, batch = run_check(tmp_path, entries, responses)
    s = out["sources"]
    assert s["ppr"]["ok"] and s["ppr"]["route"] == "insecure_tls" and s["ppr"]["kind"] == "table"
    assert s["irp"]["ok"] and (tmp_path / "samples" / "irp.pdf").read_bytes().startswith(b"%PDF")
    assert not s["ecf"]["ok"] and s["ecf"]["human_wall"] == "Baird registers an account" and "401" in s["ecf"]["reason"]
    assert not s["news"]["ok"] and "cf_impersonate" in s["news"]["reason"]
    assert out["ok_count"] == 2 and out["human_walls"] == 1
    assert json.loads((batch / access_check.PROOF_FILE).read_text())["sources"]["irp"]["ok"]
    md = (batch / "access_proof.md").read_text()
    assert "| ecf | NO |" in md and "PERSON: Baird registers an account" in md
    assert os.environ.get("GEM_BATCH") == "us-ok"


def test_a_failed_proof_lands_in_the_fetch_give_up_log(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "FAIL_LOG", tmp_path / "failures.jsonl")
    monkeypatch.setenv("GEM_BATCH", "us-ok")
    entries = [{"id": "irp", "name": "IRP", "url": "https://occ.example/irp.pdf", "proof": {"kind": "pdf"}}]
    run_check(tmp_path, entries, {"https://occ.example/irp.pdf": {"raw": b"<html>Sign in</html>", "ctype": "text/html"}})
    rec = json.loads((tmp_path / "failures.jsonl").read_text().splitlines()[-1])
    assert rec["url"] == "https://occ.example/irp.pdf" and rec["batch"] == "us-ok" and "access_check:irp" in rec["notes"]


def test_a_google_sheet_is_proven_through_the_work_profile_not_a_public_link(tmp_path):
    seen = []

    def google(fid, timeout):
        seen.append(fid)
        return True, "read through the work gws profile", "Captive LNG"

    entries = [{"id": "lng", "name": "Captive LNG sheet",
                "url": "https://docs.google.com/spreadsheets/d/19YvVT918PYHq_DkdvKWtoXYJ2Xl7l7R3/edit"}]
    out, _ = run_check(tmp_path, entries, {}, google=google)
    assert seen == ["19YvVT918PYHq_DkdvKWtoXYJ2Xl7l7R3"]
    assert out["sources"]["lng"]["ok"] and out["sources"]["lng"]["route"] == "gws-gem"
    assert out["sources"]["lng"]["file_name"] == "Captive LNG"


def test_only_rechecks_named_ids_and_keeps_the_rest(tmp_path):
    entries = [{"id": "a", "name": "A", "url": "https://a.example/"}, {"id": "b", "name": "B", "url": "https://b.example/"}]
    good = {"https://a.example/": {"raw": b"<html>a</html>"}, "https://b.example/": {"raw": b"<html>b</html>"}}
    run_check(tmp_path, entries, good)
    batch = tmp_path / "batches" / "us-ok"
    access_check.run("us-ok", batch, only={"b"}, fetch_fn=stub_fetch({"https://b.example/": {"status": "500", "raw": b""}}),
                     google_fn=lambda f, t: (False, "", ""), list_path=tmp_path / "coverage" / "us-ok.json",
                     sample_dir=tmp_path / "samples")
    s = json.loads((batch / access_check.PROOF_FILE).read_text())["sources"]
    assert s["a"]["ok"] and not s["b"]["ok"]


# ----------------------------------------------------------------- gate ---

def proof_file(batch, sources, checked=None):
    batch.mkdir(parents=True, exist_ok=True)
    (batch / access_check.PROOF_FILE).write_text(json.dumps(
        {"scope": "us-ok", "checked": checked or time.strftime("%Y-%m-%dT%H:%M:%S"), "sources": sources}))


def test_gate_fails_without_a_proof_file(tmp_path):
    listing(tmp_path, [{"id": "a", "name": "A", "url": "https://a.example/"}])
    batch = tmp_path / "batches" / "us-ok"
    batch.mkdir(parents=True)
    out, _ = gate_access_proof(batch, {"where": WHERE}, tmp_path / "coverage")
    assert out and out[0][0] == access_check.PROOF_FILE and "access_check.py --scope us-ok" in out[0][1]


def test_gate_fails_on_a_stale_or_unproven_source_and_accepts_a_human_wall(tmp_path):
    listing(tmp_path, [{"id": "a", "name": "A", "url": "https://a.example/"},
                       {"id": "b", "name": "B", "url": "https://b.example/"},
                       {"id": "c", "name": "C", "url": "https://c.example/", "human_wall": "Baird signs in"},
                       {"id": "d", "name": "D", "url": "https://d.example/"}])
    batch = tmp_path / "batches" / "us-ok"
    proof_file(batch, {"a": {"ok": True}, "b": {"ok": False, "reason": "HTTP 403", "route": "cf_impersonate"},
                       "c": {"ok": False, "reason": "HTTP 401"}})
    out, info = gate_access_proof(batch, {"where": WHERE}, tmp_path / "coverage")
    assert {o[0] for o in out} == {"b", "d"}
    assert any("person needed: c: Baird signs in" in i for i in info)
    assert any(i.startswith("proven: 1 of 4") for i in info)
    proof_file(batch, {"a": {"ok": True}, "b": {"ok": True}, "c": {"ok": True}, "d": {"ok": True}},
               checked="2026-01-01T00:00:00")
    out, _ = gate_access_proof(batch, {"where": WHERE}, tmp_path / "coverage",
                               now=time.mktime(time.strptime("2026-01-20", "%Y-%m-%d")))
    assert [o[0] for o in out] == [access_check.PROOF_FILE] and "days old" in out[0][1]


def test_gate_skips_a_narrow_batch(tmp_path):
    listing(tmp_path, [{"id": "a", "name": "A", "url": "https://a.example/"}])
    batch = tmp_path / "batches" / "us-ok-dc"
    batch.mkdir(parents=True)
    out, info = gate_access_proof(batch, {"where": WHERE, "focus": "data_centers"}, tmp_path / "coverage")
    assert out == [] and info and info[0].startswith("skipped")


# ------------------------------------------------------- coverage proof ---

def test_searched_entries_carry_read_and_date_when_strict(tmp_path):
    lp = listing(tmp_path, [{"id": "a", "name": "A", "url": "https://a.example/", "what": "x"}])
    batch = tmp_path / "batches" / "us-ok"
    batch.mkdir(parents=True)
    bare = {"status": "searched", "how": "read the table", "found": "nothing new"}
    (batch / "coverage.json").write_text(json.dumps({"sources": {"a": bare}}))
    assert gate_source_coverage(batch, {"where": WHERE}, lp.parent)[0] == []
    out, _ = gate_source_coverage(batch, {"where": WHERE}, lp.parent, strict_proof=True)
    assert {o[1].split(":")[0] for o in out} == {"searched without proof", "searched without a `date` (YYYY-MM-DD) saying when it was read"} or len(out) == 2
    full = dict(bare, read=["https://a.example/?page=1", "scopes/us-ok/work/permits/L1.md"], date="2026-11-05")
    (batch / "coverage.json").write_text(json.dumps({"sources": {"a": full}}))
    assert gate_source_coverage(batch, {"where": WHERE}, lp.parent, strict_proof=True)[0] == []


def test_proof_is_strict_from_the_rule_date_or_by_flag():
    assert not proof_strict({"updates": {"generated": "2026-10-30T10:00:00"}})
    assert proof_strict({"updates": {"generated": "2026-10-30T10:00:00"}, "qa": {"generated": "2026-11-04T09:00:00"}})
    assert proof_strict({}, flag=True) and not proof_strict({})


# ------------------------------------------------------- harvester reads ---

def test_harvester_failures_reach_the_audit_before_briefs_exist(tmp_path, monkeypatch):
    monkeypatch.setattr(fetch, "FAIL_LOG", tmp_path / "failures.jsonl")
    repo = tmp_path / "repo"
    batch = repo / "batches" / "us-ok"
    batch.mkdir(parents=True)
    permits = repo / "scopes" / "us-ok" / "work" / "permits"
    permits.mkdir(parents=True)
    monkeypatch.setattr(harvest_lib, "scope_permits", lambda scope, legacy=False: permits)
    assert harvest_lib.harvest_out("us-ok") == permits and os.environ["GEM_BATCH"] == "us-ok"
    (permits / "L1.md").write_text("harvest")
    harvest_lib.report_failure("https://deq.example/pav/api/Document/x", 500, "certificate")
    rec = json.loads((tmp_path / "failures.jsonl").read_text().splitlines()[-1])
    assert rec["batch"] == "us-ok" and "harvester" in rec["notes"] and "certificate" in rec["notes"]
    failed = access_audit._fetch_failures([batch])          # no briefs yet: the harvest folder opens the window
    assert set(failed) == {"https://deq.example/pav/api/Document/x"}
    assert failed[rec["url"]]["reason"] == "HTTP 500"


# ------------------------------------------------- a cookie-walled service ---

def test_a_warm_address_is_opened_first_for_the_session_cookie(monkeypatch):
    """The OCC Laserfiche WebLink store answers its JSON search only with the cookie its
    welcome page sets. A proof with `warm` opens that page first in the same session."""
    calls = []

    class FakeResp:
        status_code = 200
        headers = {"content-type": "application/json"}
        content = b'{"data": {"hitCount": 2}}'

    class FakeSession:
        def get(self, url, **kw):
            calls.append(("GET", url))
            return FakeResp()

        def request(self, method, url, **kw):
            calls.append((method, url))
            return FakeResp()

    monkeypatch.setattr(access_check, "_session", FakeSession)
    proof = {"method": "POST", "json": {"repoName": "OCC"}, "kind": "json",
             "warm": "https://wl.example/WebLink/Welcome.aspx?dbid=0&repo=OCC"}
    status, ctype, raw, text, is_pdf, notes, final = access_check.fetch_proof(
        "https://wl.example/WebLink/SearchService.aspx/GetSearchListing", proof, timeout=5)
    assert calls == [("GET", "https://wl.example/WebLink/Welcome.aspx?dbid=0&repo=OCC"),
                     ("POST", "https://wl.example/WebLink/SearchService.aspx/GetSearchListing")]
    assert status == "200" and "warm_cookie" in notes and "direct_post" in notes
    assert access_check.check_kind("json", raw, text, ctype) == ""


def test_frame_only_page_fails_html_proof():
    shell = ('<html><head><title>OASIS</title></head>'
             '<frameset><frame src="https://www.oasis.oati.com/webSmartOASIS/HomePage?ProviderName=PNM"></frameset></html>')
    reason = access_check.check_kind("html", shell.encode(), shell, "text/html")
    assert "frame" in reason
    framed_with_text = ('<html><body><iframe src="x"></iframe><p>' + "queue row " * 60 + '</p></body></html>')
    assert access_check.check_kind("html", framed_with_text.encode(), framed_with_text, "text/html") == ""
