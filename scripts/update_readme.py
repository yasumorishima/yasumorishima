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
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.stdout.strip()


def search_prs(repos: list[str]) -> dict[str, int]:
    """Get PR counts using gh search prs (GitHub Search API), one repo at a time."""
    all_prs = []
    for repo in repos:
        output = run([
            "gh", "search", "prs",
            "--author", AUTHOR,
            "--repo", repo,
            "--limit", "200",
            "--json", "state",
        ])
        if not output:
            continue
        all_prs.extend(json.loads(output))

    merged = sum(1 for p in all_prs if p["state"].upper() == "MERGED")
    open_count = sum(1 for p in all_prs if p["state"].upper() == "OPEN")
    closed = sum(1 for p in all_prs if p["state"].upper() == "CLOSED")
    return {
        "total": len(all_prs),
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


def get_mlb_analysis_count() -> int | None:
    """Count notebook files in mlb-statcast-visualization repo. Returns None on failure."""
    output = run([
        "gh", "api",
        "repos/yasumorishima/mlb-statcast-visualization/contents",
        "--jq", '[.[] | select(.name | endswith(".ipynb"))] | length',
    ])
    try:
        count = int(output)
        return count if count > 0 else None
    except ValueError:
        return None


def replace_marker(text: str, marker: str, replacement: str) -> str:
    """Replace content between <!-- {marker}_START --> and <!-- {marker}_END -->."""
    pattern = rf"(<!-- {marker}_START -->).*?(<!-- {marker}_END -->)"
    return re.sub(
        pattern, lambda m: f"{m.group(1)}{replacement}{m.group(2)}", text, flags=re.DOTALL
    )


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))

    print("Fetching OSS PR stats (all repos)...")
    oss_all = search_prs(REPOS)
    print(f"  All OSS: {oss_all}")

    print("Fetching team-mirai PR stats...")
    mirai = search_prs(TEAM_MIRAI_REPOS)
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

    # team-mirai stats
    if mirai["total"] > 0:
        mirai_text = (
            f"{mirai['total']} PRs "
            f"({mirai['merged']} Merged / {mirai['open']} Open / {mirai['closed']} Closed)"
        )
        readme = replace_marker(readme, "TEAM_MIRAI_STATS", mirai_text)
    else:
        print("  Skipping team-mirai update (API returned 0)")

    # OSS total stats
    if oss_all["total"] > 0:
        oss_text = f"({oss_all['total']} PRs / {oss_all['merged']} Merged)"
        readme = replace_marker(readme, "OSS_STATS", oss_text)
    else:
        print("  Skipping OSS stats update (API returned 0)")

    # Kaggle datasets (skip if API failed)
    if dataset_count is not None:
        kaggle_ds_text = f"{dataset_count} published MLB datasets"
        readme = replace_marker(readme, "KAGGLE_DS_STATS", kaggle_ds_text)
    else:
        print("  Skipping Kaggle dataset update (API unavailable)")

    # Kaggle competitions
    kaggle_comp_text = f"{kaggle_title} | 🥉 {kaggle_bronze} Bronze Notebook Medals"
    readme = replace_marker(readme, "KAGGLE_COMP_STATS", kaggle_comp_text)

    # MLB analysis count
    if mlb_count is not None:
        mlb_text = f"{mlb_count} analyses"
        readme = replace_marker(readme, "MLB_STATS", mlb_text)
    else:
        print("  Skipping MLB analysis update (API unavailable)")

    README.write_text(readme, encoding="utf-8")
    print("README.md updated.")


if __name__ == "__main__":
    main()
