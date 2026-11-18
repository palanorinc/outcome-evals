# Palanor skill for agents

A skill that teaches an agent to use the [Palanor MCP server](https://palanor.com/mcp) (`https://mcp.palanor.com`).
It covers finding a data series, saying where it stands with dated changes, reading Palanor Custom Indices and
Currents, making a chart or an embed, and citing the source and licence from the `provenance` block on every
result. It also teaches the agent to treat display-only data as display-only. The skill adds no capability of its
own: everything it does is a call to the server's existing tools.

You need a Palanor API key (free, 1,000 requests a month: <https://palanor.com/developers/keys>). Keep it in an
environment variable named `PALANOR_API_KEY`, never in a chat.

| Harness | Folder | Tested with |
|---|---|---|
| Any harness that reads the [Agent Skills](https://agentskills.io) standard | [`dist/agentskills/palanor`](dist/agentskills/palanor) | skills-ref 0.1.1 (`agentskills validate`) |
| OpenClaw | [`dist/openclaw/palanor`](dist/openclaw/palanor) | openclaw 2026.11.5 |
| Hermes Agent | [`dist/hermes/palanor`](dist/hermes/palanor) | hermes-agent 0.23.2 |
| Goose | [`dist/goose/palanor`](dist/goose/palanor) and [`dist/goose/palanor.recipe.yaml`](dist/goose/palanor.recipe.yaml) | goose 1.60.1 |

All four steps below start from a clone:

```bash
git clone --depth 1 https://github.com/palanorinc/outcome-evals.git
cd outcome-evals/skills/palanor/dist
```

## Agent Skills standard (any harness that reads it)

Copy the folder into your harness's skills directory and connect the MCP server there. For example, in Claude Code:

```bash
mkdir -p ~/.claude/skills && cp -r agentskills/palanor ~/.claude/skills/
claude mcp add --transport http palanor https://mcp.palanor.com --header "Authorization: Bearer $PALANOR_API_KEY"
```

## OpenClaw

```bash
openclaw skills install ./openclaw/palanor --global
echo "PALANOR_API_KEY=<your key>" >> ~/.openclaw/.env
openclaw mcp add palanor --url https://mcp.palanor.com --transport streamable-http \
  --header 'Authorization=Bearer ${PALANOR_API_KEY}'
openclaw skills info palanor        # Ready, with PALANOR_API_KEY found
```

OpenClaw installs from git only when `SKILL.md` sits at the repository root, so install from the clone's folder as
shown. Tools appear to the agent as `palanor__<tool>`; the skill says so.

## Hermes Agent

```bash
mkdir -p ~/.hermes/skills && cp -r hermes/palanor ~/.hermes/skills/
# or, without a clone: hermes skills install palanorinc/outcome-evals/skills/palanor/dist/hermes/palanor --yes
```

Add the server to `~/.hermes/config.yaml`, put the key in `~/.hermes/.env`, then check it:

```yaml
mcp_servers:
  palanor:
    url: "https://mcp.palanor.com"
    headers:
      Authorization: "Bearer ${PALANOR_API_KEY}"
```

```bash
echo "PALANOR_API_KEY=<your key>" >> ~/.hermes/.env
hermes skills list | grep palanor
hermes mcp test palanor             # connects and lists the server's tools
```

Keep the server key `palanor`: Hermes names tools `mcp__palanor__<tool>`, and the skill tells the agent so.

## Goose

```bash
mkdir -p ~/.agents/skills && cp -r goose/palanor ~/.agents/skills/
export PALANOR_API_KEY=<your key>
goose session --recipe goose/palanor.recipe.yaml
```

The recipe turns on the Palanor extension (the header comes from `PALANOR_API_KEY`) and the extension that loads
skills. To use the server in every session instead, add it in `goose configure` as a Remote Extension (Streamable
HTTP) with an `Authorization: Bearer <key>` header. Tools appear as `palanor__<tool>`.

## How it is built

There is one source, `source/`, and every folder under `dist/` is generated from it. Don't edit `dist/` by hand.

| Path | What |
|---|---|
| `source/skill.json` | Name, description, metadata, the tools the skill teaches, and each harness's additions |
| `source/SKILL.body.md` | The instructions every variant shares |
| `source/references/` | Hand-written reference pages |
| `source/flows.json` | The worked examples: rendered into `references/examples.md` and run against the live server |
| `tools/tools.lock.json` | The server's `tools/list`, captured; `references/tools.md` is generated from it |
| `tools/build.py` | Writes `dist/`; `--check` fails when `dist/` differs from what the source generates |
| `tools/check.py` | Drift check; checks every tool name and argument in every variant against the live server's `tools/list`; spec limits |
| `tools/flows.py` | Runs every example call against the live server (needs `PALANOR_API_KEY`) |
| `tools/refresh_lock.py` | Re-captures `tools/list` and rebuilds |

```bash
python skills/palanor/tools/build.py          # after editing source/
python skills/palanor/tools/check.py          # what CI runs (plus the validators below)
PALANOR_API_KEY=... python skills/palanor/tools/flows.py
```

CI (`.github/workflows/skill.yml`) runs the drift check and the tool check on every change and weekly, so a tool
renamed on the server shows up within a week. It also runs `agentskills validate` on the standard, OpenClaw and
Goose folders, Hermes' own skill linter on the Hermes folder, and `goose recipe validate` on the recipe. The Hermes
folder adds Hermes fields (`version`, `author`, `required_environment_variables`) that the standard's validator
rejects, so only Hermes' linter checks it.

MIT licensed. Data reached through the skill keeps its own licence, given in each result's `provenance` block.
