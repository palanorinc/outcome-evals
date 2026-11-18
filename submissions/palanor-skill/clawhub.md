# ClawHub listing (OpenClaw)

Not sent. Checked against openclaw/clawhub `docs/publishing.md` and `clawhub skill publish --help` (clawhub 0.26.0)
on 2026-11-18.

## Before sending

- **Licence.** ClawHub publishes every skill under **MIT-0** and does not allow a per-skill licence. This repo is
  MIT. MIT-0 drops the attribution clause. Publishing there means accepting MIT-0 for the copy on ClawHub.
- **Account.** `clawhub login` signs in with a GitHub account (or `clawhub login --token clh_...`). Use an account
  that represents Palanor, not a person.
- ClawHub scans each release before it goes live; the skill declares its key under `metadata.openclaw.primaryEnv`
  and `requires.env`, which the scan checks for.

## Command (run from a clone of this repo)

```bash
clawhub skill publish skills/palanor/dist/openclaw/palanor \
  --slug palanor \
  --name "Palanor" \
  --version 1.0.0 \
  --changelog "First release: find and read Palanor signals, Custom Indices and Currents through the Palanor MCP server, with dated changes, sourced charts and embeds, and citations from each result's provenance block." \
  --tags latest \
  --categories finance,research,integrations \
  --topics economic-data,mcp,citations,charts,macro
```

Try it first with `--dry-run --json`; it should report `"status": "would-publish"`.

## Listing text

> **Palanor**: sourced economic data, indices and charts from the Palanor MCP server. Finds a U.S. or world data
> series, says where it stands in its own record with dated changes, reads Palanor Custom Indices and Currents,
> makes a checked chart or a live embed, and cites the source and licence from each result's provenance block.
> Treats display-only data as display-only. Needs a Palanor API key (free: palanor.com/developers/keys) and the
> server added with `openclaw mcp add palanor --url https://mcp.palanor.com --transport streamable-http --header 'Authorization=Bearer ${PALANOR_API_KEY}'`.
