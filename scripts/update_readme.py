"""Update Profile README with live statistics from GitHub, Kaggle APIs,
and oss-contributions README (single source of truth for OSS stats)."""

import base64
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

import requests

import dashboard

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CONFIG = ROOT / "config.json"

TEAM_MIRAI_REPOS = {
    "team-mirai-volunteer/action-board": "action-board",
    "team-mirai-volunteer/fact-checker": "fact-checker",
    "team-mirai/marumie": "marumie",
    "team-mirai/mirai-gikai": "mirai-gikai",
    "team-mirai-volunteer/post-checker": "post-checker",
}

COMPETITIONS_REPO = "yasumorishima/kaggle-competitions"

# Filled in by sync_oss_stats() so the dashboard reuses the same numbers.
OSS_TOTALS: dict[str, int] = {}


def gh_env() -> dict:
    """Cross-repo reads need the PAT: the workflow token only sees this repo."""
    env = dict(os.environ)
    pat = env.get("CROSS_REPO_PAT")
    if pat:
        env["GH_TOKEN"] = pat
    return env


def run_env(cmd: list[str], env: dict) -> str | None:
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120, env=env
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.stdout.strip()


# ---------- OSS stats from oss-contributions README ----------


def fetch_oss_readme() -> str | None:
    """Fetch oss-contributions README.md via GitHub API."""
    output = run([
        "gh", "api",
        "repos/yasumorishima/oss-contributions/contents/README.md",
        "--jq", ".content",
    ])
    if not output:
        return None
    try:
        return base64.b64decode(output).decode("utf-8")
    except Exception as e:
        print(f"Failed to decode oss-contributions README: {e}", file=sys.stderr)
        return None


def parse_oss_summary(text: str) -> list[dict]:
    """Parse the summary table from oss-contributions README."""
    entries = []
    for m in re.finditer(
        r"\| \[([^]]+)\]\(https://github\.com/([^)]+)\) \|"
        r" ([^|]+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|",
        text,
    ):
        entries.append({
            "short": m.group(1),
            "repo": m.group(2),
            "total": int(m.group(4)),
            "merged": int(m.group(5)),
            "open": int(m.group(6)),
            "closed": int(m.group(7)),
        })
    return entries


def parse_oss_pr_statuses(text: str) -> dict[str, str]:
    """Build URL -> status mapping from all PR rows."""
    statuses = {}
    for m in re.finditer(
        r"\[#\d+\]\((https://github\.com/[^)]+/pull/\d+)\)"
        r" \| (Merged|Open|Closed|Done)",
        text,
    ):
        statuses[m.group(1)] = m.group(2)
    return statuses


def parse_oss_team_mirai_prs(text: str) -> list[dict]:
    """Extract team-mirai PRs (not issue comments) from oss-contributions README."""
    prs = []
    current_repo = None
    for line in text.splitlines():
        hdr = re.match(r"### \[([^\]]+)\]", line)
        if hdr:
            current_repo = hdr.group(1)
            continue
        if current_repo not in TEAM_MIRAI_REPOS:
            continue
        pr_m = re.match(
            r"\| \d+ \| \[#(\d+)\]\((https://github\.com/[^)]+/pull/\d+)\)"
            r" \| (Merged|Open|Closed) \| (.+?) \|",
            line,
        )
        if pr_m:
            prs.append({
                "pr_number": pr_m.group(1),
                "url": pr_m.group(2),
                "repo_short": TEAM_MIRAI_REPOS[current_repo],
                "status": pr_m.group(3),
                "desc": pr_m.group(4).strip(),
            })
    return prs


def sync_oss_stats(readme: str, oss_text: str) -> str:
    """Sync all OSS stats from oss-contributions README into profile README."""
    summary = parse_oss_summary(oss_text)
    if not summary:
        print("  WARNING: Could not parse oss-contributions summary table")
        return readme

    # 1. OSS_STATS + repo count
    total_prs = sum(e["total"] for e in summary)
    total_merged = sum(e["merged"] for e in summary)
    repo_count = len(summary)

    OSS_TOTALS.update(prs=total_prs, merged=total_merged, repos=repo_count)

    oss_marker_text = f"({total_prs} PRs / {total_merged} Merged)"
    readme = replace_marker(readme, "OSS_STATS", oss_marker_text)
    readme = re.sub(
        r"across \d+ repositories",
        f"across {repo_count} repositories",
        readme,
    )
    print(f"  OSS: {total_prs} PRs / {total_merged} Merged / {repo_count} repos")

    # 2. TEAM_MIRAI_STATS
    tm = {"total": 0, "merged": 0, "open": 0, "closed": 0}
    for e in summary:
        if e["repo"] in TEAM_MIRAI_REPOS:
            for k in tm:
                tm[k] += e[k]

    mirai_text = (
        f"{tm['total']} PRs "
        f"({tm['merged']} Merged / {tm['open']} Open / {tm['closed']} Closed)"
    )
    readme = replace_marker(readme, "TEAM_MIRAI_STATS", mirai_text)
    print(f"  team-mirai: {mirai_text}")

    # 3. Update PR statuses
    pr_statuses = parse_oss_pr_statuses(oss_text)
    status_changes = 0
    for url, new_status in pr_statuses.items():
        for old_status in ["Open", "Closed", "Merged", "Done"]:
            if old_status != new_status:
                old = f"]({url}) | {old_status} |"
                new = f"]({url}) | {new_status} |"
                if old in readme:
                    readme = readme.replace(old, new)
                    status_changes += 1
    if status_changes:
        print(f"  Updated {status_changes} PR status(es)")

    # 4. Add missing team-mirai PRs
    oss_tm_prs = parse_oss_team_mirai_prs(oss_text)
    existing_urls = set(
        re.findall(r"https://github\.com/team-mirai[^)]+/pull/\d+", readme)
    )
    new_prs = [p for p in oss_tm_prs if p["url"] not in existing_urls]
    if new_prs:
        lines = readme.splitlines()
        insert_idx = None
        max_num = 0
        for i, line in enumerate(lines):
            rm = re.match(r"\| (\d+) \| \*\*", line)
            if rm and any(repo in line for repo in TEAM_MIRAI_REPOS.values()):
                if insert_idx is None:
                    insert_idx = i
                num = int(rm.group(1))
                if num > max_num:
                    max_num = num
        if insert_idx is not None:
            new_prs.sort(key=lambda p: int(p["pr_number"]), reverse=True)
            for pr in new_prs:
                max_num += 1
                row = (
                    f"| {max_num} | **{pr['repo_short']}** "
                    f"| [#{pr['pr_number']}]({pr['url']}) "
                    f"| {pr['status']} | {pr['desc']} |"
                )
                lines.insert(insert_idx, row)
            readme = "\n".join(lines)
            print(f"  Added {len(new_prs)} new team-mirai PR(s)")

    return readme


# ---------- Kaggle / MLB ----------


def kaggle_cmd() -> list[str]:
    """Return the kaggle CLI command."""
    try:
        subprocess.run(["kaggle", "--version"], capture_output=True, timeout=10)
        return ["kaggle"]
    except FileNotFoundError:
        return [sys.executable, "-m", "kaggle"]


def kaggle_auth() -> tuple[str, str] | None:
    """Credentials from ~/.kaggle/kaggle.json, falling back to env vars."""
    creds = Path.home() / ".kaggle" / "kaggle.json"
    if creds.exists():
        data = json.loads(creds.read_text(encoding="utf-8"))
        return data["username"], data["key"]
    user = os.environ.get("KAGGLE_USERNAME")
    key = os.environ.get("KAGGLE_KEY")
    return (user, key) if user and key else None


def get_kaggle_dataset_count() -> int | None:
    """Count *public* datasets only.

    The CLI listing returns private datasets as well, which is how the README
    came to claim 28 "published" datasets while only 8 of them were public.
    """
    auth = kaggle_auth()
    if auth is None:
        print("  No credentials, skipping dataset count", file=sys.stderr)
        return None
    try:
        resp = requests.get(
            "https://www.kaggle.com/api/v1/datasets/list",
            params={"user": "yasunorim", "pageSize": 100},
            auth=auth,
            timeout=60,
        )
        resp.raise_for_status()
        items = resp.json()
    except Exception as exc:
        print(f"  Dataset list failed: {exc}", file=sys.stderr)
        return None
    count = sum(1 for d in items if not d.get("isPrivate", False))
    return count if count > 0 else None


def get_actions_activity() -> dict | None:
    """Count the automation that actually runs: workflows, cron, runs per month.

    Everything here is measured, not declared: a workflow counts as scheduled
    only if it really fired on `schedule` in the window, and disabled workflows
    are left out.
    """
    env = gh_env()
    since = (date.today() - timedelta(days=30)).isoformat()

    repos = []
    page = 1
    while True:
        out = run_env([
            "gh", "api",
            f"user/repos?per_page=100&affiliation=owner&page={page}",
            "--jq", '.[] | [.full_name, (.private|tostring),'
                    ' (.fork|tostring), (.archived|tostring)] | @tsv',
        ], env)
        if out is None:
            return None
        rows = [x.split("\t") for x in out.split("\n") if x]
        # Page on the raw count: filtering first would end the loop early.
        # Public only: the counts must not depend on which private repositories
        # a given token happens to reach, and a visitor cannot see them anyway.
        repos += [
            r[:2] for r in rows
            if r[1] == "false" and r[2] == "false" and r[3] == "false"
        ]
        if len(rows) < 100:
            break
        page += 1

    if not repos:
        print("  Repo listing empty, skipping activity stats", file=sys.stderr)
        return None

    active = scheduled = runs = 0
    for full, _private in repos:
        out = run_env([
            "gh", "api", f"repos/{full}/actions/workflows?per_page=100",
            "--jq", '.workflows[] | select(.state == "active") | .id',
        ], env)
        ids = [x for x in (out or "").split("\n") if x]
        active += len(ids)

        n = run_env([
            "gh", "api",
            f"repos/{full}/actions/runs?created=%3E%3D{since}&per_page=1",
            "--jq", ".total_count",
        ], env)
        if n and n.isdigit():
            runs += int(n)

        for wid in ids:
            c = run_env([
                "gh", "api",
                f"repos/{full}/actions/workflows/{wid}/runs"
                f"?event=schedule&created=%3E%3D{since}&per_page=1",
                "--jq", ".total_count",
            ], env)
            if c and c.isdigit() and int(c) > 0:
                scheduled += 1

    return {
        "repos": len(repos),
        "active_workflows": active,
        "scheduled": scheduled,
        "runs_30d": runs,
    }


def get_mlb_analysis_count() -> int | None:
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
    pattern = rf"(<!-- {marker}_START -->).*?(<!-- {marker}_END -->)"
    return re.sub(
        pattern, lambda m: f"{m.group(1)}{replacement}{m.group(2)}", text, flags=re.DOTALL
    )


def update_bronze_in_text(text: str, bronze: int) -> str:
    text = re.sub(r"\d+ Bronze Notebook Medals", f"{bronze} Bronze Notebook Medals", text)
    text = re.sub(
        r"Bronze Medal Notebooks \(\d+\)", f"Bronze Medal Notebooks ({bronze})", text
    )
    text = re.sub(r"All \d+ notebooks", f"All {bronze} notebooks", text)
    return text


def update_competitions_readme(bronze: int) -> None:
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


# ---------- Main ----------


def main():
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    bronze = config.get("notebook_bronze", 0)

    readme = README.read_text(encoding="utf-8")

    # OSS stats from oss-contributions (single source of truth)
    print("Fetching oss-contributions README...")
    oss_readme = fetch_oss_readme()
    if oss_readme:
        readme = sync_oss_stats(readme, oss_readme)
    else:
        print("  WARNING: Could not fetch oss-contributions README, skipping OSS sync")

    # Kaggle datasets
    print("Fetching Kaggle dataset count...")
    dataset_count = get_kaggle_dataset_count()
    print(f"  Datasets: {dataset_count}")
    if dataset_count is not None:
        readme = replace_marker(
            readme, "KAGGLE_DS_STATS", f"{dataset_count} public datasets"
        )
    else:
        print("  Skipping Kaggle dataset update (API unavailable)")

    # Kaggle competitions
    kaggle_title = config.get("kaggle_title", "Notebooks Expert")
    print(f"  Bronze notebooks (from config.json): {bronze}")
    kaggle_comp_text = f"{kaggle_title} | \U0001f949 {bronze} Bronze Notebook Medals"
    readme = replace_marker(readme, "KAGGLE_COMP_STATS", kaggle_comp_text)
    readme = update_bronze_in_text(readme, bronze)

    # MLB analysis count
    print("Fetching MLB analysis count...")
    mlb_count = get_mlb_analysis_count()
    print(f"  MLB analyses: {mlb_count}")
    if mlb_count is not None:
        readme = replace_marker(readme, "MLB_STATS", f"{mlb_count} analyses")
    else:
        print("  Skipping MLB analysis update (API unavailable)")

    # Career years (started 2008)
    career_years = date.today().year - 2008
    readme = replace_marker(readme, "CAREER_YEARS", str(career_years))
    print(f"  Career years: {career_years}")

    README.write_text(readme, encoding="utf-8")
    print("Profile README.md updated.")

    print("Measuring GitHub Actions activity...")
    activity = get_actions_activity()
    print(f"  Activity: {activity}")

    # At-a-glance dashboard (self-hosted SVG, no third-party badge service)
    # Fail closed: if a source was unreachable the README keeps its old numbers,
    # so the card must keep its old numbers too rather than publish zeros.
    if not OSS_TOTALS or activity is None:
        print("Skipping dashboard: incomplete stats this run")
        return

    print("Rendering dashboard...")
    tiles = [
        (str(OSS_TOTALS.get("prs", 0)), "open-source pull requests",
         f"{OSS_TOTALS.get('merged', 0)} merged"),
        (str(OSS_TOTALS.get("repos", 0)), "upstream repositories", "contributed to"),
        (str(config.get("pypi_packages", 0)), "PyPI packages", "published and maintained"),
        (f"{activity['active_workflows']:,}", "active workflows",
         f"across {activity['repos']} public repositories"),
        (f"{activity['scheduled']:,}", "of them on a schedule", "fired on cron this month"),
        (f"{activity['runs_30d']:,}", "workflow runs", "in the last 30 days"),
        (str(bronze), "Kaggle notebook medals", f"bronze, {kaggle_title}"),
        (str(config.get("dataset_silver", 0)), "Kaggle dataset medals", "silver"),
        (str(config.get("production_sites", 0)), "web apps in production",
         "on Vercel and the Internet Computer"),
    ]
    for path in dashboard.write(tiles, date.today().isoformat()):
        print(f"  Wrote {path.name}")

    # Cross-repo: kaggle-competitions
    print("\nUpdating kaggle-competitions README...")
    try:
        update_competitions_readme(bronze)
    except Exception as e:
        print(f"  WARNING: kaggle-competitions update failed: {e}", file=sys.stderr)
        print("  Continuing without kaggle-competitions update.")


if __name__ == "__main__":
    main()
