# Hermes Agent listing

Not sent. Checked against NousResearch/hermes-agent v0.23.2 (`tools/skills_hub_github.py`, `CONTRIBUTING.md`) on
2026-11-18.

Hermes users can already install the skill without any listing:

```bash
hermes skills install palanorinc/outcome-evals/skills/palanor/dist/hermes/palanor --yes
```

Hermes has no submission form. Its Marketplace is built from skills.sh, ClawHub, LobeHub and the default GitHub
taps. Vendors that maintain skills for their own products (wandb, qdrant, pinecone-io, Notion, Airtable) are listed
as default taps. Third-party integrations are otherwise promoted in the Nous Research Discord,
`#plugins-skills-and-skins`.

## Option A: a pull request to NousResearch/hermes-agent

**Before sending:** a GitHub account to open it from, not a person's.

Change, in `tools/skills_hub_github.py`, `DEFAULT_TAPS`, after the other vendor-maintained entries:

```python
        {"repo": "palanorinc/outcome-evals", "path": "skills/palanor/dist/hermes/"},
```

Title: `skills: add Palanor's vendor-maintained skill repo to the default taps`

Body:

> Adds `palanorinc/outcome-evals` (path `skills/palanor/dist/hermes/`) to `DEFAULT_TAPS`, next to the other
> vendor-maintained skill repos. It holds one skill, `palanor`, which teaches the agent to use Palanor's public
> MCP server (`https://mcp.palanor.com`): finding economic data series, reading where they stand with dated
> changes, Palanor's indices, charts and embeds, and citing the source and licence from each result's provenance
> block.
>
> - Frontmatter follows the Hermes standard: `version`, `author`, `license: MIT`, `required_environment_variables`
>   (`PALANOR_API_KEY`), and `metadata.hermes.tags` / `category`.
> - `tools/skill_linter.py` at v0.23.2 reports no findings, and the repo's CI runs that linter on every change.
> - Tools are referred to as `mcp__palanor__<tool>`, matching `mcp_prefixed_tool_name()` with the server named
>   `palanor`.
> - The skill adds no code and no scripts: only `SKILL.md` and three linked reference pages.
>
> Maintained by Palanor; MIT licensed.

## Option B: a Discord post (#plugins-skills-and-skins)

> Palanor skill for Hermes: sourced economic data, indices and charts from Palanor's public MCP server, with
> dated changes and a source and licence line on every value.
> `hermes skills install palanorinc/outcome-evals/skills/palanor/dist/hermes/palanor`
> Setup (server entry for config.yaml and a free key): https://github.com/palanorinc/outcome-evals/tree/main/skills/palanor
