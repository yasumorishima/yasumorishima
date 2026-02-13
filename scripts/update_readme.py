"""Update Profile README with live statistics from GitHub and Kaggle APIs."""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONFIG = ROOT / "config.json"

REPOS = [
    "team-mirai-volunteer/action-board",
    "team-mirai/marumie",
    "team-mirai-volunteer/post-checker",
    "team-mirai-volunteer/fact-checker",
    "jldbc/pybaseball",
    "line/line-bot-mcp-server",
    "dfinity/icp-js-core",
    "dfinity/icp-js-canisters",
    "optuna/optuna",
    "pandas-dev/pandas",
    "pyomeca/ezc3d",
    "dfinity/pic-js",
]

TEAM_MIRAI_REPOS = [
    "team-mirai-volunteer/action-board",
    "team-mirai/marumie",
    "team-mirai-volunteer/post-checker",
    "team-mirai-volunteer/fact-checker",
]

AUTHOR = "yasumorishima"


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.stdout.strip()


def get_pr_stats(repos: list[str]) -> dict[str, int]:
    """Get PR counts by state for given repos using gh CLI."""
    total = merged = open_count = closed = 0
    for repo in repos:
        output = run([
            "gh", "pr", "list",
            "--repo", repo,
            "--author", AUTHOR,
            "--state", "all",
            "--json", "state",
            "--limit", "200",
        ])
        if not output:
            continue
        prs = json.loads(output)
        for pr in prs:
            state = pr["state"]
            total += 1
            if state == "MERGED":
                merged += 1
            elif state == "OPEN":
                open_count += 1
            elif state == "CLOSED":
                closed += 1
    return {
        "total": total,
        "merged": merged,
        "open": open_count,
        "closed": closed,
    }


def kaggle_cmd() -> list[str]:
    """Return the kaggle CLI command (tries 'kaggle', falls back to 'python -m kaggle')."""
    try:
        subprocess.run(["kaggle", "--version"], capture_output=True, timeout=10)
        return ["kaggle"]
    except FileNotFoundError:
        return [sys.executable, "-m", "kaggle"]


def get_kaggle_dataset_count() -> int | None:
    """Count published Kaggle datasets. Returns None on failure."""
    output = run([*kaggle_cmd(), "datasets", "list", "--user", "yasunorim", "--csv"])
    if not output:
        return None
    lines = output.strip().split("\n")
    count = len(lines) - 1  # subtract header
    return count if count > 0 else None


def get_kaggle_notebook_count() -> int | None:
    """Count published Kaggle notebooks. Returns None on failure."""
    output = run([*kaggle_cmd(), "kernels", "list", "--user", "yasunorim", "--csv"])
    if not output:
        return None
    lines = output.strip().split("\n")
    count = len(lines) - 1
    return count if count > 0 else None


def get_mlb_analysis_count() -> int:
    """Count notebook files in mlb-statcast-visualization repo."""
    output = run([
        "gh", "api",
        "repos/yasumorishima/mlb-statcast-visualization/contents",
        "--jq", '[.[] | select(.name | endswith(".ipynb"))] | length',
    ])
    try:
        return int(output)
    except ValueError:
        return 0


def replace_marker(text: str, marker: str, replacement: str) -> str:
    """Replace content between <!-- {marker}_START --> and <!-- {marker}_END -->."""
    pattern = rf"(<!-- {marker}_START -->).*?(<!-- {marker}_END -->)"
    return re.sub(pattern, rf"\1{replacement}\2", text, flags=re.DOTALL)


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))

    print("Fetching OSS PR stats (all repos)...")
    oss_all = get_pr_stats(REPOS)
    print(f"  All OSS: {oss_all}")

    print("Fetching team-mirai PR stats...")
    mirai = get_pr_stats(TEAM_MIRAI_REPOS)
    print(f"  team-mirai: {mirai}")

    print("Fetching Kaggle dataset count...")
    dataset_count = get_kaggle_dataset_count()
    print(f"  Datasets: {dataset_count}")

    print("Fetching Kaggle notebook count...")
    notebook_count = get_kaggle_notebook_count()
    print(f"  Notebooks: {notebook_count}")

    print("Fetching MLB analysis count...")
    mlb_count = get_mlb_analysis_count()
    print(f"  MLB analyses: {mlb_count}")

    kaggle_title = config.get("kaggle_title", "Notebooks Expert")
    kaggle_bronze = config.get("kaggle_bronze_medals", 0)

    readme = README.read_text(encoding="utf-8")

    # team-mirai stats: "21 PRs (11 Merged / 2 Open / 8 Closed)"
    mirai_text = (
        f"**{mirai['total']} PRs "
        f"({mirai['merged']} Merged / {mirai['open']} Open / {mirai['closed']} Closed)**"
    )
    readme = replace_marker(readme, "TEAM_MIRAI_STATS", mirai_text)

    # OSS total stats: "(35 PRs / 14 Merged)"
    oss_text = f"({oss_all['total']} PRs / {oss_all['merged']} Merged)"
    readme = replace_marker(readme, "OSS_STATS", oss_text)

    # Kaggle datasets: "4 published MLB datasets" (skip if API failed)
    if dataset_count is not None:
        kaggle_ds_text = f"**{dataset_count} published MLB datasets**"
        readme = replace_marker(readme, "KAGGLE_DS_STATS", kaggle_ds_text)
    else:
        print("  Skipping Kaggle dataset update (API unavailable)")

    # Kaggle competitions: "Notebooks Expert | 8 Bronze Notebook Medals"
    kaggle_comp_text = f"**{kaggle_title}** | 🥉 **{kaggle_bronze} Bronze Notebook Medals**"
    readme = replace_marker(readme, "KAGGLE_COMP_STATS", kaggle_comp_text)

    # MLB analysis count: "6 analyses"
    mlb_text = f"**{mlb_count} analyses**"
    readme = replace_marker(readme, "MLB_STATS", mlb_text)

    README.write_text(readme, encoding="utf-8")
    print("README.md updated.")


if __name__ == "__main__":
    main()
