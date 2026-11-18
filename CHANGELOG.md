# Changelog

## 0.1.0 (2026-11-18)

First release.

- Call format: JSON Schema and dataclasses (`Call`, `Rule`, `Transform`, `Forecast`, `Resolution`).
- Resolver with written, tested rules for late or missing readings, revisions (the first resolution stands) and series that end.
- Scoring: Brier, log score, calibration bins, hit rate; no-change and base-rate baselines; number calls with scaled error and quantile loss. Unresolved calls are never scored.
- Public question set from 27 U.S. federal series (public domain): 216 live questions made 2026-11-18 (30- and 90-day deadlines) and 2,312 resolved-history questions made quarterly from January 2024.
- Adapters: Inspect AI task and scorer, Harbor dataset exporter (plus a 51-task sample), OpenEnv environment and server.
- Data client: shipped files with no key, or Palanor's public API with a key.
- Example: a fictional company's private calls scored end to end.
