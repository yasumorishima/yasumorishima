"""Update Profile README with live statistics from GitHub and Kaggle APIs."""

import json
import os
import re
import subprocess
import sys
import tempfile
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
COMPETITIONS_REPO = "yasumorishima/kaggle-competitions"


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


def update_bronze_in_text(text: str, bronze: int) -> str:
    """Update all bronze medal count patterns in a text."""
    # "12 Bronze Notebook Medals" -> "13 Bronze Notebook Medals"
    text = re.sub(r"\d+ Bronze Notebook Medals", f"{bronze} Bronze Notebook Medals", text)
    # "Bronze Medal Notebooks (12)" -> "Bronze Medal Notebooks (13)"
    text = re.sub(
        r"Bronze Medal Notebooks \(\d+\)", f"Bronze Medal Notebooks ({bronze})", text
    )
    return text


def update_competitions_readme(bronze: int) -> None:
    """Clone kaggle-competitions, update README, commit & push."""
    token = os.environ.get("CROSS_REPO_PAT", "")
    if not token:
        print("  CROSS_REPO_PAT not set, skipping kaggle-competitions update")
        return

    tmpdir = tempfile.mkdtemp()
    repo_url = f"https://x-access-token:{token}@github.com/{COMPETITIONS_REPO}.git"

    print(f"  Cloning {COMPETITIONS_REPO}...")
    result = subprocess.run(
        ["git", "clone", "--depth=1", repo_url, tmpdir],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        print(f"  Clone failed: {result.stderr}", file=sys.stderr)
        return

    readme_path = Path(tmpdir) / "README.md"
    original = readme_path.read_text(encoding="utf-8")
    updated = update_bronze_in_text(original, bronze)

    if updated == original:
        print("  No change in kaggle-competitions README")
        return

    readme_path.write_text(updated, encoding="utf-8")

    subprocess.run(
        ["git", "config", "user.name", "github-actions[bot]"], cwd=tmpdir, check=True
    )
    subprocess.run(
        ["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"],
        cwd=tmpdir, check=True,
    )
    subprocess.run(["git", "add", "README.md"], cwd=tmpdir, check=True)
    subprocess.run(
        ["git", "commit", "-m", f"docs: update bronze medal count to {bronze}"],
        cwd=tmpdir, check=True,
    )
    subprocess.run(["git", "push"], cwd=tmpdir, check=True)
    print(f"  Pushed kaggle-competitions README (bronze={bronze})")


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    bronze = config.get("notebook_bronze", 0)

    print("Fetching OSS PR stats (all repos)...")
    oss_all = search_prs(REPOS)
    print(f"  All OSS: {oss_all}")

    print("Fetching team-mirai PR stats...")
    mirai = search_prs(TEAM_MIRAI_REPOS)
    print(f"  team-mirai: {mirai}")

    print("Fetching Kaggle dataset count...")
    dataset_count = get_kaggle_dataset_count()
    print(f"  Datasets: {dataset_count}")

    print("Fetching MLB analysis count...")
    mlb_count = get_mlb_analysis_count()
    print(f"  MLB analyses: {mlb_count}")

    kaggle_title = config.get("kaggle_title", "Notebooks Expert")
    print(f"  Bronze notebooks (from config.json): {bronze}")

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

    # Kaggle competitions — from config.json
    kaggle_comp_text = f"{kaggle_title} | 🥉 {bronze} Bronze Notebook Medals"
    readme = replace_marker(readme, "KAGGLE_COMP_STATS", kaggle_comp_text)

    # Sync the <summary> count
    readme = re.sub(
        r"<summary>All Bronze Medal Notebooks \(\d+\)</summary>",
        f"<summary>All Bronze Medal Notebooks ({bronze})</summary>",
        readme,
    )

    # MLB analysis count
    if mlb_count is not None:
        mlb_text = f"{mlb_count} analyses"
        readme = replace_marker(readme, "MLB_STATS", mlb_text)
    else:
        print("  Skipping MLB analysis update (API unavailable)")

    README.write_text(readme, encoding="utf-8")
    print("Profile README.md updated.")

    # Cross-repo: kaggle-competitions
    print("\nUpdating kaggle-competitions README...")
    update_competitions_readme(bronze)


if __name__ == "__main__":
    main()
