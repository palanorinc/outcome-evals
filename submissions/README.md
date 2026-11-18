# Prepared submissions (not sent)

Nothing in this folder has been submitted anywhere. Each subfolder holds the exact file and text a
submission needs, pinned to commit `129c05a38fb819e074d1e268e4705ab12732d542`. Each register needs a person or an
account to act, listed under "Before sending".

| Where | What it takes | Before sending |
|---|---|---|
| Inspect Evals Register | An issue on UKGovernmentBEIS/inspect_evals (form below); a bot opens the PR from `eval.yaml` | The submitter needs a GitHub account with a commit in this repo. The form needs an arXiv paper (none exists; the guide says to note this in the issue and a maintainer handles it). After the PR opens: log files of two models' full runs, which need model calls. |
| Harbor | Either `harbor publish harbor/outcome-evals-resolved-sample --public` (Harbor Hub) or a PR adding `registry-entry.json` to harbor-framework/harbor's `registry.json` | A Harbor Hub login, or a GitHub account for the PR. Works today with no registry: `harbor run --repo palanorinc/outcome-evals -d outcome-evals-resolved-sample -a <agent>`. |
| OpenEnv | `openenv push openenv-env --repo-id <hf-org>/outcome-evals` (a Hugging Face Space tagged `openenv`), optionally a PR adding `envs/outcome_evals_env` to openenv/OpenEnv | A Hugging Face organization and token; the in-tree PR needs the Meta CLA signed. |
