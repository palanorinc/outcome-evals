Title: [Register Submission] Outcome Evals

arXiv URL:
(none: see the note below)

Source URL:
https://github.com/palanorinc/outcome-evals/blob/129c05a38fb819e074d1e268e4705ab12732d542/src/outcome_evals/adapters/inspect_task.py#L209

Maintainers:
(the submitting account)

Note for the maintainers:
This eval has no arXiv paper. It is a forecasting eval whose method is written out in the repository README
("How a call resolves", "Scoring") and in the resolver's docstring, with a test for each rule. Per the
Submission Guide ("What if the standard issue workflow doesn't work for me?"), we'd ask a maintainer to
create the entry from the prepared eval.yaml below rather than from a paper.

- Task: `outcome_evals` (`@task` in src/outcome_evals/adapters/inspect_task.py); `uv sync` installs
  inspect-ai through the default dependency group.
- Data ships in the repository at the pinned commit (no external assets). Every series is a U.S. Government
  work in the public domain; DATA-LICENSES.md quotes each source's terms.
- The default split (resolved history) is labelled as not a forecasting test for models trained after the
  outcomes. The live split (-T split=live) leaves unresolved questions unscored: their scores are all None and
  the metrics skip them.
- A no-model baseline: `inspect eval outcome_evals/outcome_evals -T fixed_probability=0.5 --model mockllm/model`
  gives Brier 0.250 on the resolved split.

(Then paste eval.yaml.)
