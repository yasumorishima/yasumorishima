# CLAUDE.md

GitHub profile repository. `README.md` is what appears on https://github.com/yasumorishima.

## Editing README.md

- **Never remove visuals**: images, GIFs, tables, badges, the dashboard SVG and `<details>` sections stay. People judge the page by how it looks.
- **Never remove project links**: the README is the owner's index of their projects. When text is too long, shorten it or move it into a `<details>` block; do not drop the project.
- Text can be cut hard. Put long explanations inside `<details>` rather than in the visible page.
- Keep every auto-update marker and the text the scripts rewrite:
  - `<!-- NAME_START -->…<!-- NAME_END -->`: `CAREER_YEARS`, `OSS_STATS`, `TEAM_MIRAI_STATS`, `KAGGLE_COMP_STATS`, `KAGGLE_DS_STATS`, `MLB_STATS`, `MATHCAT_JA`, and every `RANK_*` listed in `config.json`
  - `<!--ob:*-->` / `<!--fn:*-->` (written from the baseball site repos)
  - The phrases `across N repositories`, `N Bronze Notebook Medals`, `Bronze Medal Notebooks (N)` and `All N notebooks`
- After editing, check that no link from the old README went missing and that each marker is still present.

## Automation

- `.github/workflows/update-profile.yml` runs `scripts/update_readme.py` daily and whenever `config.json` is pushed. It updates the stats in `README.md` and commits them to `main`.
- `scripts/dashboard.py` generates `assets/dashboard-{light,dark}.svg`.
- Competition ranks: add an entry to `competition_ranks` in `config.json`, and put the matching `RANK_*` marker in the README.

## Workflow

- Only `main` appears on the profile. When a change is meant to be shown, go all the way: branch, PR, then merge. Do not stop at a pushed branch.
- Reply to the owner in Japanese.
- Do not force-push from a cloud session; the permission check blocks it. To restart a branch whose PR was already merged, merge the old remote branch into the new one and push normally.
