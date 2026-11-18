# skills.sh

Not sent. skills.sh has no submission form: "Skills appear on the leaderboard automatically through anonymous
telemetry when users run `npx skills add <owner/repo>`." The Hermes Marketplace crawls skills.sh twice a day and
keeps only entries whose `SKILL.md` it can find on GitHub.

## Before sending

A decision whether Palanor installs the skill once itself to seed the listing. That would be the first and only
telemetry event behind the listing, which some would read as self-promotion. The safe default is to let it appear
when someone outside installs it.

## The command a user runs

```bash
npx skills add palanorinc/outcome-evals
```

The repo holds four copies of the skill (one per harness) under `skills/palanor/dist/`. The `agentskills` copy is
the one to point skills.sh users at.
