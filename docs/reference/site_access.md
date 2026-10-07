# Site access playbook

The research has to read every page and document a person at a desk could read. When a page will not open for a script, that is a fact about the tool, not about the page. This file says how to get in, what each kind of failure means, and which sites have needed what. It grows with every country.

## The ladder `fetch.py` climbs on its own

`url_verifier.py`, `harvest_permits.py` and every research agent fetch through `scripts/fetch.py`. For an ad hoc check:

```bash
python scripts/fetch.py <url> --head 3000      # the whole ladder; the notes line says which step worked
python scripts/fetch.py <url> --render --text  # force the real-Chrome step
```

1. Plain curl with a browser user agent.
2. A plain "429 Too Many Requests" is a queue. It is waited out with growing pauses, one process per server at a time.
3. A 401, 403, 406 or a bot-check page: retry with the network fingerprint of Chrome, then Firefox (`curl_cffi`).
4. A JavaScript challenge (Cloudflare, Imperva): a real Chrome earns the cookie and curl retries with it.
5. Still walled: the page is opened in a real Chrome and read as a person's browser sees it. The cookies Chrome earns are kept, so later pages on that host open with plain curl again.
6. Only then does `url_verifier.py` turn to the Internet Archive. It looks for up to three different saved copies, newest first, and passes if any of them shows the value. A pass keeps the live address as the citation.

Two things make the ladder learn:

- **Learned routes.** Each host that needed more than plain curl is written to `work/fetch_routes.json` with the step that worked. The next fetch to that host starts there.
- **The disk cache.** Any page that needed Chrome or a long wait, and every page from a throttled host, is kept in `work/fetch_cache/` for 30 days.

`LNGCT_NO_BROWSER=1` turns off the Chrome steps for runs nobody is watching.

Chrome works out of sight. By default it opens no window of its own and loads each page behind everything else, so it never takes focus. `LNGCT_BROWSER_MODE=headless` runs it with no window at all, and `LNGCT_BROWSER_MODE=visible` brings back the window in front. Signing in (`--login`) always opens a visible window. `python scripts/browser_mode_probe.py` loads one walled page of each kind in each mode, each in a fresh profile. It reports whether the wall cleared and whether Chrome ever came to the front. On 2026-10-07 the background and headless modes both cleared Cloudflare, AWS WAF, the energate puzzle page and the Cylex page, and neither came to the front. The DataDome check on waz.de was not tested, because the waz.de home page does not show it.

## What each failure means and what to do

Run `python scripts/access_audit.py <batch dir> --retry` at the end of a batch. It reads every failed citation check, and every page `fetch.py` could not open while the batch ran (logged to `work/fetch_failures.jsonl`, so pages an agent tried and gave up on show up too). It sorts each one into one of these kinds and re-runs it with the ladder as it is now.

| Kind | What it looks like | What to do |
|---|---|---|
| Rate limit | 429 that outlasts the waits | Run again later. If the host always throttles, add it to the paced hosts in `fetch.py` and harvest its pages before research starts, as with the German permit register. Meanwhile look for a copy of the same document on another site (see below). |
| Bot wall | 401, 403, 406, "Just a moment", "Access denied", a captcha page | The ladder passes most of these. If even Chrome is stopped, use the archive and record the host below. |
| Sign-in wall | A free or paid account is needed for the full text | A person signs in once: `python scripts/cf_clearance.py --login <site address>`. Chrome opens; sign in and close the tab. The session is kept and every later fetch to that site reads as that reader. The script never types a password. Creating an account is the user's call. |
| Geographic or network block | "The URL you requested has been blocked" even in Chrome | Use the archive. An in-country connection also works: curl honors the `https_proxy` setting. |
| Gone | 404, 410, or a "page not found" page | Search the site for the moved page. Official notices are often taken down after the display period, so look for the same document in the permit register or the agency's own archive. The verifier names an archived copy that still shows the value. Treat it as a lead to a live source; the Update SOP never cites an archive address. |
| Dead host | No connection at all, or the domain no longer exists | The archive. Companies that merged or renamed usually moved their press archive to the new domain. |
| Server error | 400 or 5xx | Try again later. If it persists, the site was rebuilt. Search for the document title to find its new address. |
| Empty record | The page opens but shows the site's "no record" template, such as the permit register's "Keine Detailinformationen verfügbar" | The record may have been taken down, or the server sent the template under load. It is never cached. Try again later, open the record's documents by their own addresses, and look for a copy on another site (see below). |
| Old encryption | The secure connection fails | `fetch.py` retries without checking the certificate and notes `insecure_tls`. The page content is real. |
| Scanned PDF with no text | "PDF has no extractable text" | Check the OCR language packs (`fetch.OCR_LANG`); add the country's language. |
| Archive refused | The archive lookup failed or showed "Temporarily Offline" | The archive goes down for minutes at a time. Run again later. This is never a verdict on the page. |
| Value missing | The page opened but the claimed value is not on it | Usually a research question. Some pages fill in their text with JavaScript; `access_audit.py --retry --render-missing` reopens them in Chrome. |

## When one site will not give it up, find the copy

A person who cannot open a document on one site looks for it somewhere else. Official documents are almost never published once. A permit notice goes on the national register, the permit authority's notice page, the official gazette and often the town's website. A company filing goes to the regulator and the company's own site. A press release is re-posted by trade papers.

- Search the web for the document's exact file name or its title in quotes. This finds copies on other hosts directly.
- Search for the town or plant with the local word for "public notice" or "permit decision", plus the authority's name.
- Cite the copy that opens. It is the same document from an official publisher, so it is a full source, not an archive stand-in. Two copies of one document still count as one source.
- Write the hosts that carried copies into the country note, by state or region. The next batch in that country starts there.

`harvest_permits.py` says this in a plant's summary whenever a register page or file could not be saved.

## Sites that have needed something special

Add a row whenever a host needs more than plain curl, and copy anything country specific into that country's note under "Site access".

| Country | Host | What it needs | Seen |
|---|---|---|---|
| Germany | uvp-verbund.de and the uvp.<state>.de front ends | Throttles almost every request. Paced, cached, harvested ahead with `harvest_permits.py`. | 2026-10-05 |
| Germany | energate-messenger.de | A browser puzzle on the first visit; Chrome solves it and curl reuses the cookie. Full article text needs a free account (sign-in mode). | 2026-10-06 |
| Germany | waz.de, waz-online.de | DataDome bot check. Chrome passes it once and curl reuses the cookie. | 2026-10-06 |
| Germany | chemieindustrie-online.de | Answers 406 to curl. The Chrome fingerprint passes. | 2026-10-06 |
| Germany | uniper.energy | The Chrome fingerprint. Old file addresses answer "Access denied" instead of "not found"; take the current link from the reports page. | 2026-10-05 |
| Germany | waerme.hamburg, hamburger-energiewerke.de | A network block that stops even Chrome. Archive, or an in-country connection. | 2026-10-06 |
| Germany | bra.nrw.de (district government public notices) | Notices are withdrawn after the display period and then answer 403 or 404. Use the permit register copy. | 2026-10-06 |
| Germany | neukieritzsch.de, lds.sachsen.de, lvwa.sachsen-anhalt.de, rp-darmstadt.hessen.de, regierung-schwaben.bayern.de and other authority and town sites | Plain curl. They re-post the permit register's notices and files without throttling. The country note lists them by state. | 2026-10-06 |
| Germany | pressearchiv.steag.com, kraftwerk-saarbruecken.com, pq-energy.com | Domains gone. Archive copies exist for some pages. Live replacements: cms.law and energie-saarlorlux.com carry the Steag and Saarbrücken facts, the Swabia government's reports carry PQ Gundelfingen. | 2026-10-06 |
| Germany | web2.cylex.de (business directory) | Opens only in a real Chrome. Learned route `browser_render`. | 2026-10-06 |
| Germany | infraserv.com | Old press release addresses answer 500. Releases moved to `/de/medien/pressemeldungen/`. | 2026-10-06 |
| United States | eia.gov (EIA-860M page) | Plain curl, but the page lists links for months not yet published, and those redirect (301) to an HTML landing page instead of answering 404. `eia860m.py` refuses redirects and checks the content type, so a download is only kept when it is a spreadsheet. | 2026-10-06 |
| United States | sec.gov | Not a bot wall. Needs a declared name and email in the user agent, which `fetch.py` sends. | 2026-10-02 |
| United States | conedison.gcs-web.com, spglobal.com | Akamai "Access Denied". The Chrome fingerprint passes. | 2026-10-02 |
| Global | power-technology.com, nsenergybusiness.com, offshore-technology.com | Bare 403. The Chrome fingerprint passes. | 2026-10-02 |

## Archive tips

- The archive's index (CDX) lists every saved copy: `http://web.archive.org/cdx/search/cdx?url=<address>&filter=statuscode:200&collapse=digest&fl=timestamp,original`. Add `&matchType=prefix` to list every saved page under a folder, which finds moved or renamed documents on a dead site.
- A saved copy is read at `https://web.archive.org/web/<timestamp>/<address>`. Adding `id_` after the timestamp gives the raw file without the archive's toolbar.
- The archive throttles and goes offline for minutes at a time. `url_verifier.py` takes turns with other processes and retries; a refused lookup is reported as "try again later", never as "no copy".

## When a new country starts

1. Run the batch as usual. The ladder handles most sites without help.
2. At the end, run `access_audit.py --retry` on the batch and read the table.
3. Add every host that needed something special to the table above and to the country note.
4. A host that throttles everything gets a paced-host entry in `fetch.py` and a harvest step, like the German register.
5. A sign-in wall goes to the user with the site name and what it holds. Signing up is their decision.
