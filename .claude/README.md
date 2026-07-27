# `.claude/` — Claude Code configuration

This repo intentionally commits **no** `settings.json` permission baseline.
Permissions inherit from the user-global Claude Code settings
(`~/.claude*/settings.json`), the same as the sibling researcher repos
(lng-terminals, lng-carriers, pipelines, refineries) — kept identical on
purpose so no repo prompts differently from the others.

Personal per-machine overrides go in `.claude/settings.local.json`
(gitignored, never committed). Settings layer as: enterprise policy → CLI
flags → `settings.local.json` → this repo's `settings.json` (absent) →
user-global.

The guardrails that matter for this project are not permission rules: the
"never write to the live GEM database" rule and the staging-deliverable
workflow live in `CLAUDE.md`. Secrets (`GEM_READONLY_DB_URL`, GEM auth
cookies) live in `.env`, which is gitignored and denied to Claude's Read
tool at the user-global layer.
