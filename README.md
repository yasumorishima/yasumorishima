# Yasunori Morishima (盛島康徳)
Manufacturing Engineer & Data Analyst with <!-- CAREER_YEARS_START -->18<!-- CAREER_YEARS_END --> years of experience, specializing in data analysis, open source contribution, and business automation.

[![Findy Skill Deviation](https://img.shields.io/badge/Findy_Skill_Deviation-73.0-blue)](https://findy-code.io/skills-share/f6fUT0vdoVeI4) <sub>2026-06-01時点: 73.0</sub>

[![Kaggle](https://img.shields.io/badge/Kaggle-Notebooks%20Expert-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/yasunorim)
[![Zenn](https://img.shields.io/badge/Zenn-JP%20articles-3EA8FF?logo=zenn&logoColor=white)](https://zenn.dev/shogaku)
[![DEV.to](https://img.shields.io/badge/DEV.to-EN%20articles-0A0A0A?logo=devdotto&logoColor=white)](https://dev.to/yasumorishima)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/morishima-yasunori-b70229241)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yasumorishima/yasumorishima/main/assets/dashboard-dark.svg">
  <img alt="At a glance: open-source, GitHub Actions automation, Kaggle and package metrics" src="https://raw.githubusercontent.com/yasumorishima/yasumorishima/main/assets/dashboard-light.svg">
</picture>

**Jump to** — [Robotics](#-robotics--embedded) · [Baseball websites](#-baseball-websites) · [Baseball analytics](#-baseball-analytics) · [Realtime open data](#-realtime-open-data) · [Document OCR](#-document-ocr) · [Open source](#-open-source-contributions) · [Competitions](#-data--competitions) · [Mobile and web apps](#-mobile--web-apps) · [PyPI](#-pypi-packages) · [Learning projects](#-learning-projects) · [Tech stack](#️-tech-stack) · [Career](#-career) · [Patents](#-patents) · [Contact](#-contact--blog)

## 🤖 Robotics / Embedded

### [stackchan-lab](https://github.com/yasumorishima/stackchan-lab) — M5 Stack-chan Development Log (Active)

<details>
<summary>How the voice loop runs</summary>

Stack-chan (`M5STACK-K151`) on a self-hosted Raspberry Pi 5 server — 19 server tools · 11 device tools over MCP · sings 16 cheer songs · stock firmware

| Stage | |
| --- | --- |
| Speech in | sherpa-onnx / ReazonSpeech, on the Pi |
| Reply | hosted 120B model, free tier |
| Speech out | Open JTalk on the Pi (0.27s / sentence), tuned for a small speaker |
| Tools | weather, markets, news, quake / typhoon, trains, baseball, cheer songs, … |
| Device tools | camera, head, LED, volume, screen, battery |
| Interrupting | server stops audio and listens at a silent point |
| Latency | spoken sentence by sentence while the reply streams |
| Shipping | Pi polls `main`, tests on staging, swaps in, rolls back on failure |

</details>

<details>
<summary>What went wrong, and what it turned out to be</summary>

| Symptom | Cause |
| --- | --- |
| Pairing failed (`No devices found`) | factory firmware nine releases behind; USB was the only way in |
| Kept talking to the stock server | hand-written NVS key padded with `0xFF` instead of `0x00` |
| OOM-killed at 7GB, twice | VAD never fired on an always-streaming mic |
| Speech in slow motion | some real sentences synthesise slow; the server re-splits them |
| Rhythm would not come back | the measuring method was the limit; timed against note onsets, it sings |
| Speech quieter than singing | speech energy sits below 500Hz, which the speaker cannot play |

More in the [server notes](https://github.com/yasumorishima/stackchan-lab/tree/main/server#readme).

</details>

Write-up: [stackchan-lab](https://github.com/yasumorishima/stackchan-lab#readme) · Private: [stackchan-logs](https://github.com/yasumorishima/stackchan-logs) 🔒 · [stackchan-cache](https://github.com/yasumorishima/stackchan-cache) 🔒

`M5Stack CoreS3 (ESP32-S3) / Raspberry Pi 5 / Python (aiohttp, WebSocket) / sherpa-onnx + ReazonSpeech / Open JTalk / MCP / Opus`

### [rpi5-infra](https://github.com/yasumorishima/rpi5-infra) 🔒 *(private, config record)*

<details>
<summary>What it records, and what it leaves out</summary>

Config record for the robot's Pi 5, so it can be rebuilt after an SD failure.

| | |
| --- | --- |
| Recorded | firewall, systemd units, cron, listening ports, running services |
| Left out | secrets and credential files |

</details>

`Raspberry Pi OS / systemd / ufw / cron / Tailscale`

---

## ⚾ Baseball Websites

### [Minami Baseball OB](https://minami-baseball-ob.vercel.app/) — Alumni Association Site (In Production)

<table>
<tr>
<td align="center"><b>PC (Light)</b></td>
<td align="center"><b>Game Results</b></td>
</tr>
<tr>
<td><a href="https://minami-baseball-ob.vercel.app/"><img src="https://raw.githubusercontent.com/yasumorishima/minami-baseball-ob-docs/main/screenshots/top-pc.png" width="420"></a></td>
<td><img src="https://raw.githubusercontent.com/yasumorishima/minami-baseball-ob-docs/main/screenshots/results.png" width="420"></td>
</tr>
</table>

<details>
<summary>Architecture & features</summary>

<!--ob:active_users-->11<!--/ob--> active users · <!--ob:pages-->44<!--/ob--> pages · <!--ob:db_tables-->23<!--/ob--> DB tables · <!--ob:e2e_tests-->19<!--/ob--> e2e tests · <!--ob:cost-->¥0<!--/ob-->/mo (<!--ob:ts_files-->159<!--/ob--> files, <!--ob:loc-->~22500<!--/ob--> LOC)

- **5-tier RBAC**: Next.js Middleware + Supabase RLS
- **Member pipeline**: Google Form → Apps Script → GitHub Actions → Supabase; no names in Git
- **Custom CMS**: editors, soft delete, change history, audit logs
- **<!--ob:senseki-->686<!--/ob--> match records** (1955–present)
- **Security**: RLS on all tables, CODEOWNERS, secret scanning
- **Silent-fail monitoring**: hourly health check, auto-opened issues, email alerts

</details>

**[Technical Documentation](https://github.com/yasumorishima/minami-baseball-ob-docs)**

`Next.js 15 / TypeScript 5.8 / Tailwind CSS 4 / Supabase / Vercel / GitHub Actions / Google Apps Script / GA4`

### [Yokohama Funnies](https://yokohama-funnies.vercel.app/) — Amateur Baseball Team Site (In Production)

<details>
<summary>Architecture & features</summary>

Forked from Minami Baseball OB — <!--fn:players-->23<!--/fn-->-player roster · <!--fn:pages-->48<!--/fn--> pages · <!--fn:db_tables-->32<!--/fn--> DB tables · <!--fn:e2e_tests-->19<!--/fn--> e2e tests · <!--fn:cost-->¥0<!--/fn-->/mo (<!--fn:ts_files-->175<!--/fn--> files, <!--fn:loc-->~24700<!--/fn--> LOC)

- **5-tier RBAC** with Google OAuth
- **Approve by merge**: a form request becomes a PR; merging grants the role
- **Stats schema**: per-game batting / pitching / attendance → 打率 / OPS / ERA / WHIP
- **Stat input**: spreadsheet migration + manual input beside the scorebook image
- **Security & monitoring**: RLS, gitleaks, hourly health check

</details>

**[Technical Documentation](https://github.com/yasumorishima/yokohama-funnies-docs)**

`Next.js 15 / TypeScript 5.8 / Tailwind CSS 4 / Supabase / Vercel / GitHub Actions / Google Apps Script`

---

## ⚾ Baseball Analytics

<details>
<summary>About this section</summary>

Organised like a club's data-science group. MLB Statcast and public NPB stats, free tiers only; forecasts are pre-registered.

</details>

### 1. Strategy & In-Game Decisions

| Project | What it answers | Links |
|---|---|---|
| **[MLB Win Probability Engine](https://github.com/yasumorishima/mlb-win-probability)** | Win probability from 915K plate appearances + a Claude bench coach | [Live](https://mlb-wp-engine.streamlit.app/) · [Result](https://github.com/yasumorishima/mlb-win-probability/blob/master/research/steal_claude/RESULTS.md) |
| **[NPB Team Simulation](https://github.com/yasumorishima/npb-prediction)** | Monte Carlo season simulation | [Live](https://npb-prediction.streamlit.app/) · [Result](https://github.com/yasumorishima/npb-prediction/blob/main/data/backtest/2026_team_result.md) |
| **[Next-Pitch Forecast](https://github.com/yasumorishima/mlb-pitch-forecast)** | Which pitch type comes next? Beats usage tables for 97.5% of pitchers | [Results](https://github.com/yasumorishima/mlb-pitch-forecast/blob/main/RESULTS.md) |
| **[Pitch Shape × Swing Shape](https://github.com/yasumorishima/kaggle-datasets/tree/matchup-diag/pitch-swing-matchup)** *(in progress)* | Does pitch shape vs swing shape change the outcome? | [Plan & results](https://github.com/yasumorishima/kaggle-datasets/tree/matchup-diag/pitch-swing-matchup) |

**Tracking-data player evaluation** — <!-- MLB_STATS_START -->11 analyses<!-- MLB_STATS_END --> of Japanese MLB pitchers and Ohtani.

<details>
<summary>All analyses</summary>

| Analysis | Key Finding | Article |
|----------|-------------|---------|
| **Kikuchi Slider Revolution (2019-2025)** | SL 17%→37% after Astros trade | [Zenn](https://zenn.dev/shogaku/articles/kikuchi-slider-revolution-2019-2025) / [DEV.to](https://dev.to/yasumorishima/yusei-kikuchis-pitching-evolution-a-statcast-analysis-2019-2025-2a4a) / [Kaggle](https://www.kaggle.com/code/yasunorim/yusei-kikuchi-slider-revolution-2019-2025) |
| **Senga Ghost Fork (2023-2025)** | FO whiff rate 58%→39% | [Zenn](https://zenn.dev/shogaku/articles/senga-ghost-fork-analysis-2023-2025) / [DEV.to](https://dev.to/yasumorishima/kodai-sengas-ghost-fork-analyzed-with-statcast-data-2023-2025-1k1d) / [Kaggle](https://www.kaggle.com/code/yasunorim/kodai-senga-ghost-fork-analysis-2023-2025) |
| **Imanaga 2nd Year (2024-2025)** | 3-pitch concentration (97%) | [Zenn](https://zenn.dev/shogaku/articles/imanaga-2nd-year-analysis-2024-2025) / [DEV.to](https://dev.to/yasumorishima/shota-imanagas-sophomore-year-what-statcast-data-reveals-2024-2025-235) / [Kaggle](https://www.kaggle.com/code/yasunorim/imanaga-rookie-to-sophomore-pitching) |
| **Darvish Evolution (2021-2025)** | SL/ST halved, CU became putaway pitch | [Zenn](https://zenn.dev/shogaku/articles/darvish-pitching-evolution-2021-2025) / [DEV.to](https://dev.to/yasumorishima/yu-darvishs-pitching-evolution-2021-2025-a-statcast-data-analysis-fij) / [Kaggle](https://www.kaggle.com/code/yasunorim/yu-darvish-pitching-evolution-2021-2025) |
| **Ohtani Spray Chart** | pybaseball's spraychart() in one line | [Zenn](https://zenn.dev/shogaku/articles/pybaseball-spraychart-builtin) |
| **Ohtani Heatmap** | Stadium in matplotlib + hit density | [Zenn](https://zenn.dev/shogaku/articles/pybaseball-spraychart-matplotlib) |
| **2022-2024 analyses (5)** | WBC 2023, Ohtani 2022-2023, 2024 HR race | [Folder](https://github.com/yasumorishima/mlb-statcast-visualization/tree/main/analyses-2022-2024) |
| **2026 update** | Four pitchers' arsenals 2019-2026 as GIFs | [Folder](https://github.com/yasumorishima/mlb-statcast-visualization/tree/main/update-2026) |

</details>

### 2. Scouting & Player Development

| Project | What it answers | Links |
|---|---|---|
| **[NPB Season Prediction](https://github.com/yasumorishima/npb-prediction)** | Player projections: Bayesian ensemble (Marcel + Stan/Ridge + ML) | [Live](https://npb-prediction.streamlit.app/) · Article [JP](https://zenn.dev/shogaku/articles/npb-bayes-integration-production) / [EN](https://dev.to/yasumorishima/adding-bayesian-ensemble-monte-carlo-to-an-npb-prediction-app-58po) |
| **[NPB Foreign Player Study](https://github.com/yasumorishima/npb-foreign-statcast)** | Does MLB Statcast predict a foreign player's first NPB season? | [Repo](https://github.com/yasumorishima/npb-foreign-statcast) |
| **[Aging Curve & Development Tracker](https://github.com/yasumorishima/baseball-bayes)** | Stan aging model + each hitter against his expected band | [Repo](https://github.com/yasumorishima/baseball-bayes) · [Tracker](https://github.com/yasumorishima/baseball-bayes/tree/main/development) |
| **[Which KPIs Carry Over](https://github.com/yasumorishima/mlb-data-pipeline)** | Which numbers repeat next season? Skill does, luck does not | Article [JP](https://qiita.com/ussu_ussu_ussu/items/81b75c0020bf2e1d84f3) / [EN](https://dev.to/yasumorishima/does-a-pitchs-performance-carry-over-to-next-season-whiff-rate-vs-run-value-on-8022-mlb-pairs-bj) |
| **[Player Condition Monitoring](https://github.com/yasumorishima/kaggle-datasets#4-mlb-statcast--bat-tracking-2024-2026)** | Can an injury be seen early? Arm IL signal found (AUC 0.61) | [Ohtani](https://www.kaggle.com/code/yasunorim/ohtani-2026-could-the-slump-be-seen-early) / [All hitters](https://www.kaggle.com/code/yasunorim/ohtani-2026-pattern-across-every-mlb-hitter) / [Anomaly](https://www.kaggle.com/code/yasunorim/do-hitters-drift-from-normal-before-the-il) |
| **[Jev as a Baseball Prior](https://github.com/yasumorishima/jev-baseball)** | Can a decision-only AI forecast next-season wOBA zero-shot? | Article [JP](https://qiita.com/ussu_ussu_ussu/items/cc28f711396515c1fb31) / [EN](https://dev.to/yasumorishima/asking-a-decision-only-ai-typesafe-jev-to-forecast-next-seasons-hitting-worth-about-20-to-50-360k) |

<details>
<summary>Prediction accuracy & details</summary>

| System | Key Metric | Articles |
|--------|-----------|----------|
| **NPB 2026** | Out-of-sample: beats both floors, ≈ Marcel alone | [JP](https://zenn.dev/shogaku/articles/npb-bayes-integration-production) / [EN](https://dev.to/yasumorishima/adding-bayesian-ensemble-monte-carlo-to-an-npb-prediction-app-58po) |
| **NPB 2026 Teams** | Median-wins MAE 5.83; win ranges too narrow | [Result](https://github.com/yasumorishima/npb-prediction/blob/main/data/backtest/2026_team_result.md) |
| **NPB 2021 Backtest** | MAE **10.90W** | [Repo](https://github.com/yasumorishima/npb-prediction/tree/main/research/2021-backtest) |
| **MLB WP Engine** | Held-out 2026 Brier 0.158 | [Live](https://mlb-wp-engine.streamlit.app/) |
| **Baseball MLOps** | wOBA MAE .0287 (Marcel .0326) / xFIP MAE 0.483 (Marcel 0.558) | [Live](https://baseball-mlops.streamlit.app/) |

</details>

### 3. Delivery to Staff: Dashboards & Apps

| Tool | For whom / what | Links |
|---|---|---|
| **Scouting dashboards** | Leaderboards and pitch reliability on the dbt marts | [Looker](https://lookerstudio.google.com/reporting/9c1d9fa2-c796-45a0-85de-633a888c4fd9) · [Tableau](https://public.tableau.com/app/profile/y.m7878/viz/MLBScoutingDashboard/1) |
| **[WBC 2026 Scouting](https://github.com/yasumorishima/wbc-scouting)** | 37 Statcast apps, 19 countries, in the browser | [All 37](https://yasumorishima.github.io/wbc-scouting/) / [Japan Pitchers](https://yasumorishima.github.io/wbc-scouting/japan-pitchers.html) |
| **[MLB Bat Tracking Dashboard](https://github.com/yasumorishima/mlb-bat-tracking-dashboard)** | Leaderboard, comparison, lineup builder | [Live](https://yasumorishima-mlb-bat-tracking.streamlit.app/) |
| **Amateur team stats** | Real team stats read from paper scorebooks | [Site](https://yokohama-funnies.vercel.app/) · [How-to (JP)](https://github.com/yasumorishima/baseball-scorebook-ocr-docs/blob/main/stats-from-scorebook.md) · [Runbook](https://github.com/yasumorishima/yokohama-funnies/blob/main/docs/scorebook-to-stats.md) 🔒 |

### 4. MLOps & Data Platform

| Project | What it does | Links |
|---|---|---|
| **[MLB Data Pipeline](https://github.com/yasumorishima/mlb-data-pipeline)** | Public HF dataset, refreshed weekly + dbt / DuckDB marts | [HF Dataset](https://huggingface.co/datasets/yasumorishima/mlb-stats) |
| **[Next-Pitch Forecast API](https://github.com/yasumorishima/mlb-pitch-forecast#api)** | Free JSON API, refreshed daily in season | [API](https://mlb-pitch-forecast.vercel.app/api/predict) |
| **[Baseball MLOps Pipeline](https://github.com/yasumorishima/baseball-mlops)** | 5-model ensemble from the W&B registry | [Live](https://baseball-mlops.streamlit.app/) |
| **[savant-extras](https://github.com/yasumorishima/savant-extras)** | PyPI package for Baseball Savant leaderboards | [PyPI](https://pypi.org/project/savant-extras/) |
| **Gated Kaggle datasets** | Statcast + bat tracking (2.14M pitches), published only when checks pass | [Statcast](https://www.kaggle.com/datasets/yasunorim/mlb-statcast-bat-tracking-2024-2025) |

### 5. Unstructured Data: Vision & Language

**[Baseball Skeleton Analysis](https://github.com/yasumorishima/baseball-cv)** — 3D skeletons from Driveline OpenBiomechanics C3D data

<table>
<tr>
<td align="center"><b>Pitching Skeleton (3D C3D)</b></td>
<td align="center"><b>Hitting Skeleton (3D C3D)</b></td>
</tr>
<tr>
<td><img src="https://raw.githubusercontent.com/yasumorishima/baseball-cv/master/data/output/skeleton_pitching_anim.gif" width="400"></td>
<td><img src="https://raw.githubusercontent.com/yasumorishima/baseball-cv/master/data/output/skeleton_hitting_anim.gif" width="400"></td>
</tr>
</table>

<details>
<summary>Finding & articles</summary>

Trunk rotation vs pitch speed: r=0.425. Bug fix [PR #384](https://github.com/pyomeca/ezc3d/pull/384) to ezc3d. [Article (JP)](https://zenn.dev/shogaku/articles/baseball-cv-skeleton-biomechanics) / [Article (EN)](https://dev.to/yasumorishima/3d-skeleton-detection-from-baseball-motion-capture-data-with-driveline-c3d-29ja)

</details>

- **[One-camera pitching pose](https://github.com/yasumorishima/pitching-pose-one-camera)** — what one camera can measure (in progress)
- **Handwritten scorebook reading** — see [Document OCR](#-document-ocr)
- **[Ask the marts in Japanese](https://github.com/yasumorishima/stackchan-lab/blob/main/server/mlb_ask.py)** — spoken MLB questions → DuckDB, on Stack-chan

---

## 🌍 Realtime Open Data

<table>
<tr>
<td align="center"><a href="https://github.com/yasumorishima/japan-geohazard-monitor"><b>Japan Geohazard Monitor</b></a></td>
<td align="center"><a href="https://github.com/yasumorishima/hormuz-ship-tracker"><b>Persian Gulf Ship Tracker</b></a></td>
</tr>
<tr>
<td><a href="https://github.com/yasumorishima/japan-geohazard-monitor"><img src="https://raw.githubusercontent.com/yasumorishima/japan-geohazard-monitor/master/docs/screenshot.png" width="420"></a></td>
<td><a href="https://github.com/yasumorishima/hormuz-ship-tracker"><img src="https://raw.githubusercontent.com/yasumorishima/hormuz-ship-tracker/master/docs/screenshot.png" width="420"></a></td>
</tr>
<tr>
<td>31 geophysical sources → ML earthquake prediction (AUC 0.907) + monitoring dashboard</td>
<td>Vessel tracking via AIS + Sentinel-1 radar, all on GitHub Actions · <a href="https://yasumorishima.github.io/hormuz-ship-tracker/">map</a></td>
</tr>
</table>

`Real-time API / WebSocket → SQLite → FastAPI + Leaflet.js` — [All projects](https://github.com/yasumorishima/realtime-open-data)

**[Earth Vital Signs](https://github.com/yasumorishima/earth-vital-signs)** — sea ice, CO2, temperature, El Niño, rebuilt daily

**[Japan Road Traffic](https://github.com/yasumorishima/japan-road-traffic)** — ~2,000 highway counters, archived daily before the source drops them

**[Japan Geohazard Monitor](https://github.com/yasumorishima/japan-geohazard-monitor)** — Earthquake prediction research

<details>
<summary>Evaluation and the Kumamoto InSAR result</summary>

| Where the 0.907 comes from | Arm over its climatology, per window |
| --- | --- |
| aftershock-driven positives (39%) | +0.018 |
| isolated mainshocks (61%) | +0.007 |
| strict 11% (no M≥4 within 50 km in prior year) | +0.010 |

- **Evaluation**: walk-forward, 37 windows, 1989–2026; climatology alone reaches 0.902
- **Rules**: pre-registered, frozen scripts, compared against permutation floors — [RESEARCH-LOG.md](https://github.com/yasumorishima/japan-geohazard-monitor/blob/master/RESEARCH-LOG.md)
- **Data**: public HF dataset, weekly CI; licensed inputs in [geohazard-restricted-inputs](https://github.com/yasumorishima/geohazard-restricted-inputs) 🔒
- **InSAR**: 2026 Kumamoto M7.1 displacement from Sentinel-1 ([details](https://github.com/yasumorishima/japan-geohazard-monitor/tree/master/research/kumamoto2026_insar))

</details>

**[Japan Wildlife Sightings](https://github.com/yasumorishima/japan-wildlife-sightings)** — Bear and wildlife sighting open data, normalized · [map](https://yasumorishima.github.io/japan-wildlife-sightings/)

<details>
<summary>What is collected, and what is withheld</summary>

- **27 sources, 79,394 records** in one schema, rebuilt daily
- **Only what licences allow is published** (40,241 records) — [docs/licenses.md](https://github.com/yasumorishima/japan-wildlife-sightings/blob/main/docs/licenses.md)
- **Map**: MapLibre GL JS over GSI tiles, no external CDN

</details>

---

## 🧾 Document OCR

<details>
<summary>Approach</summary>

No cloud OCR, no generative model; the same page always reads the same.

</details>

### [Handwritten Scorebook OCR](https://github.com/yasumorishima/baseball-scorebook-ocr) 🔒 *(private R&D, active)*

<details>
<summary>Where it stands</summary>

Paper scorebook photos → at-bat data · OpenCV on a Raspberry Pi 5 · constraint solver · 33 graded sheets

| Configuration | Score |
| --- | --- |
| Shipped default | 366 / 396 = **92%** |
| No grid facts handed over | 363 / 396 = 92% |
| Every recognition in-house | 321 / 396 = 81% (with ledger), **283 / 396 = 71%** (none) |
| Hardest mark class: template → + solver | 76% → **93%** |
| Consecutive held-out sheets | 31 |
| Paid vision model on the same corners | 370 / 396 = 93% |
| Real output | my team's 2026 batting stats |

</details>

<details>
<summary>What the last rounds changed</summary>

| Change | Result |
| --- | --- |
| Inning columns read off the paper, not the ledger | truth reachable on all 31 sheets (was 3) |
| "Max three outs per inning" made a price, not a gate | +36 corners in-house |
| Adversarial review of that claim | first run was mis-flagged; re-measured |
| Nine fixes for spurious marks | all null |

</details>

Public write-up: [baseball-scorebook-ocr-docs](https://github.com/yasumorishima/baseball-scorebook-ocr-docs) (JP)

### [Business-Form PDF Extraction](https://github.com/yasumorishima/form-ocr-lab) 🔒 *(private R&D, active)*

<details>
<summary>Why not a generative OCR</summary>

Supplier PDFs → spreadsheet, **no generative model** · same input, same bytes out · reconciled against the printed total

| Check | Result |
| --- | --- |
| Same number, two passes | characters swap between runs |
| Two-pass agreement, worst page | about half — **voting does not converge** |
| Where the methods disagreed | **always the generative side** |
| Duplicates it reported | 14, true duplicates **0** |

</details>

<details>
<summary>Rebuilding it from the write-up</summary>

| Check | Result |
| --- | --- |
| Suites on the rebuild | **785 checks, 0 failures** |
| Do the tests have teeth | **42** hand mutations + **98** swept mutants, none surviving |
| What a sweep cannot measure | outside review still found **3**, then **6** more issues |
| The worst of them | the file was written, but the screen said it was not |

</details>

---

## 🌐 Open Source Contributions

<!-- OSS_STATS_START -->(140 PRs / 93 Merged)<!-- OSS_STATS_END --> across 49 repositories. See [oss-contributions](https://github.com/yasumorishima/oss-contributions) for full details.

PR review: CodeRabbit, with one central config in [coderabbit](https://github.com/yasumorishima/coderabbit) 🔒 (docs-only PRs stay quiet), and CodeQL on public repos and forks, with coverage and triage notes in [codeql](https://github.com/yasumorishima/codeql) 🔒.

<details>
<summary>PR highlights (click to expand)</summary>

| Repository | PR | Description |
|---|---|---|
| **dfinity/icp-js-core** | [#1270](https://github.com/dfinity/icp-js-core/pull/1270) | Candid decode error messages |
| **line/line-bot-mcp-server** | [#369](https://github.com/line/line-bot-mcp-server/pull/369) | Add get_follower_ids tool |
| **pyomeca/ezc3d** | [#384](https://github.com/pyomeca/ezc3d/pull/384) | Fix `__eq__` early return bug |
| **codeforjapan/mapprint** | [#556](https://github.com/codeforjapan/mapprint/pull/556) | Share buttons on the disaster print map |
| **codeforjapan/mapprint** | [#564](https://github.com/codeforjapan/mapprint/pull/564) | Deterministic list order |
| **codeforjapan/mapprint** | [#563](https://github.com/codeforjapan/mapprint/pull/563) | 2026 Kumamoto earthquake paper map |
| **codeforjapan/BirdXplorer** | [#281](https://github.com/codeforjapan/BirdXplorer/pull/281) | Statement timeouts for the API |
| **hotosm/openaerialmap** | [#289](https://github.com/hotosm/openaerialmap/pull/289) | STAC ingester dropping the wrong record |
| **apache/fineract-backoffice-ui** | [#321](https://github.com/apache/fineract-backoffice-ui/pull/321) | Accounting screen translations |
| **daisy/MathCAT** | [#665](https://github.com/daisy/MathCAT/pull/665) | Chemistry assertions that could never fail |
| **daisy/MathCAT** | [#720-929](https://github.com/daisy/MathCAT/pull/929) | Japanese speech rules, 25 merged PRs, now in main ([#936](https://github.com/daisy/MathCAT/pull/936)) |
| **daisy/MathCAT** | [#746](https://github.com/daisy/MathCAT/pull/746) | Japanese navigation announcements for blind readers |
| **PHPOffice/PHPPresentation** | [#897](https://github.com/PHPOffice/PHPPresentation/pull/897) | PHP 8.4/8.5 static analysis, 144 findings fixed |
| **project-inclusive/OpenFisca-Japan** | [#479-484](https://github.com/project-inclusive/OpenFisca-Japan/pull/479) | Six welfare benefits added |
| **MobilityData/gtfs-validator** | [#2177](https://github.com/MobilityData/gtfs-validator/pull/2177) | Require stop IDs on transfers |
| **sugarlabs/musicblocks-v4** | [#774](https://github.com/sugarlabs/musicblocks-v4/pull/774) | Palette interactions with tests |
| **AtsushiSakai/PythonRobotics** | [#1408](https://github.com/AtsushiSakai/PythonRobotics/pull/1408) | CI on Python 3.14 |
| **optuna/optuna** | — | Hyperparameter optimization framework |
| **pandas-dev/pandas** | — | Data analysis library |
| **jldbc/pybaseball** | [#514](https://github.com/jldbc/pybaseball/pull/514) | Bug fixes & pandas 3 compatibility |

<details>
<summary>team-mirai — Civic Tech OSS (<!-- TEAM_MIRAI_STATS_START -->26 PRs (14 Merged / 4 Open / 8 Closed)<!-- TEAM_MIRAI_STATS_END -->)</summary>

| Repository | Highlights |
|---|---|
| **action-board** | [48 unit tests](https://github.com/team-mirai-volunteer/action-board/pull/1969), [RPC tests](https://github.com/team-mirai-volunteer/action-board/pull/1869), [breadcrumb nav](https://github.com/team-mirai-volunteer/action-board/pull/1849), [cache fix](https://github.com/team-mirai-volunteer/action-board/pull/1845) + 5 more |
| **mirai-gikai** | [seed permission fix](https://github.com/team-mirai/mirai-gikai/pull/930), [Safari/iOS ruby spacing](https://github.com/team-mirai/mirai-gikai/pull/932) |
| **fact-checker** | [X API investigation](https://github.com/team-mirai-volunteer/fact-checker/issues/69#issuecomment-3811711591) + 5 PRs |

</details>

</details>

---

## 📊 Data & Competitions

### Kaggle

<!-- KAGGLE_COMP_STATS_START -->Notebooks Expert | 🥉 14 Bronze Notebook Medals<!-- KAGGLE_COMP_STATS_END -->

**Finished 2026:** [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) ([agent](https://github.com/yasumorishima/kaggle-competitions/tree/main/kaggriculture), <!-- RANK_KAGGRICULTURE_START -->6047/10148<!-- RANK_KAGGRICULTURE_END -->) · [ROGII Wellbore Geology](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) (<!-- RANK_ROGII_START -->2545/6125<!-- RANK_ROGII_END -->) · [PS S6E6](https://www.kaggle.com/competitions/playground-series-s6e6) (F1 0.95939) · [Stanford RNA 3D Folding 2](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2) · [BirdCLEF+ 2026](https://www.kaggle.com/competitions/birdclef-2026)

<details>
<summary>Bronze Medal Notebooks (14)</summary>

| Notebook | Topic |
|----------|-------|
| [savant-extras Defense & Pitching Quality](https://www.kaggle.com/code/yasunorim/savant-extras-defense-pitching-quality) | Defense & pitching quality |
| [MLB Statcast Spray Charts for WBC 2026](https://www.kaggle.com/code/yasunorim/mlb-statcast-spray-charts-for-wbc-2026-players) | WBC 2026 spray + zone charts |
| [March Machine Learning Mania 2026](https://www.kaggle.com/code/yasunorim/march-machine-learning-mania-2026-baseline) | NCAA prediction (LightGBM) |
| [NFL Geometric Rules Baseline](https://www.kaggle.com/code/yasunorim/geometric-rules-baseline-2-921-rmse-no-ml) | Rules only, RMSE 2.921 |
| [CAFA 6 Baseline](https://www.kaggle.com/code/yasunorim/baseline-with-regularization) | Protein function (PyTorch MLP) |

[All 14 notebooks →](https://www.kaggle.com/yasunorim/code)

</details>

### Kaggle Datasets

<!-- KAGGLE_DS_STATS_START -->11 public datasets<!-- KAGGLE_DS_STATS_END -->

| Dataset | Description |
|---------|-------------|
| 🥈 [MLB Bat Tracking Leaderboard (2024-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-bat-tracking-2024-2025) | 452 batters, 19 swing metrics |
| 🥈 [WBC 2026 Scouting](https://www.kaggle.com/datasets/yasunorim/wbc-2026-scouting) | 306 players, 20 countries |

<details>
<summary>Other datasets (9)</summary>

| Dataset | Description |
|---------|-------------|
| [Earth Vital Signs - Daily Climate Indicators](https://www.kaggle.com/datasets/yasunorim/earth-vital-signs-daily) | Climate indicators, rebuilt daily ([repo](https://github.com/yasumorishima/earth-vital-signs)) |
| [Japan Road Traffic Volume (Hourly Archive)](https://www.kaggle.com/datasets/yasunorim/japan-road-traffic-volume) | ~2,000 highway counters ([repo](https://github.com/yasumorishima/japan-road-traffic) · [starter](https://www.kaggle.com/code/yasunorim/japan-road-traffic-a-forecasting-starter)) |
| [ABS Challenges: Triple-A 2025 to MLB 2026](https://www.kaggle.com/datasets/yasunorim/mlb-abs-challenges-aaa-2025-to-mlb-2026) | 15 challenge boards · [JP](https://qiita.com/ussu_ussu_ussu/items/57c5760b3f9917b3883f) / [EN](https://dev.to/yasumorishima/abs-challenges-from-triple-a-to-mlb-catchers-win-most-and-batters-who-dont-chase-win-more-499a) |
| [Baseball Savant Leaderboards (2024-2026)](https://www.kaggle.com/datasets/yasunorim/baseball-savant-leaderboards-2024) | 20 leaderboards |
| [Japanese MLB Players Statcast (2015-2026)](https://www.kaggle.com/datasets/yasunorim/japan-mlb-pitchers-batters-statcast) | 38 players, 198k pitches |
| [MLB Pitcher Arsenal (2020-2026)](https://www.kaggle.com/datasets/yasunorim/mlb-pitcher-arsenal-2020-2025) | 5,716 pitcher-seasons · [notebook](https://www.kaggle.com/code/yasunorim/pitcher-arsenal-analysis) |
| [MLB Statcast + Bat Tracking (2024-2026)](https://www.kaggle.com/datasets/yasunorim/mlb-statcast-bat-tracking-2024-2025) | Every pitch 2024-2026 (2.14M) |
| [XC BirdCLEF 2026 Target Recordings (URLs)](https://www.kaggle.com/datasets/yasunorim/xc-birdclef-2026-target-urls) | Xeno-canto URLs |
| [BEATs iter3+ AS2M Pretrained](https://www.kaggle.com/datasets/yasunorim/beats-pretrained) | Audio checkpoint for offline notebooks |

</details>

### SIGNATE

**Active:** 5th Air Combat AI Challenge (to 2026-12-04)

**Finished 2026:** NEDO Baggage-Loading Optimization (<!-- RANK_NEDO_START -->167/591<!-- RANK_NEDO_END -->) · NIR Moisture Prediction

### DrivenData

**[DrivenData Competitions](https://github.com/yasumorishima/drivendata-comp)** — GitHub Actions + GPU pipeline · latest: [On Top of Pasketti](https://www.drivendata.org/competitions/309/)

---

## 📱 Mobile & Web Apps

| App | Description | Link |
|---|---|---|
| **[Daily Diary](https://github.com/yasumorishima/diary-app-flutter)** | Flutter, 10 languages, offline-first, screen-reader checked in CI | [Google Play](https://play.google.com/store/apps/details?id=com.diary.daily) |
| **[Fire Tablet Google Play Helper](https://github.com/yasumorishima/yasumorishima.github.io/tree/main/fire-gapps)** | Step-by-step APK install guide for Fire OS | [Live](https://yasumorishima.github.io/fire-gapps/) |

### [icrc167-android](https://github.com/yasumorishima/icrc167-android) — Internet Identity login for native Android (Active)

<details>
<summary>Seven things that were measured rather than assumed</summary>

ICRC-167 for Android: sign in with Internet Identity and call canisters directly, no backend.

| Question | What the measurement said |
| --- | --- |
| Does the URL fragment survive an App Link? | Yes, byte-exact |
| Does the device test prove anything? | Only the negative cases do |
| Is the hash right? | Now pinned to the spec's worked example |
| Do negative tests reach their check? | Not at first; now pinned with a mutation in CI |
| Testable before Internet Identity? | Yes, with a locally signed chain |
| Do published vectors settle the rules? | No, they predate the subnet-type rule |
| Does the certificate bind to the canister? | Not on its own |

Demo passed on a real phone (2026-09-14) · passkey issue [dfinity/internet-identity#4334](https://github.com/dfinity/internet-identity/issues/4334)

</details>

`Kotlin / Android / BLS12-381 · Ed25519 · ECDSA P-256 / CBOR / GitHub Actions`

---

## 📦 PyPI Packages

<details>
<summary>6 packages (click to expand)</summary>

| Package | Description |
|---------|-------------|
| [savant-extras](https://github.com/yasumorishima/savant-extras) | 17 Baseball Savant leaderboards |
| [baseball-field-viz](https://github.com/yasumorishima/baseball-field-viz) | Field drawing, spray and zone charts |
| [kaggle-notebook-deploy](https://github.com/yasumorishima/kaggle-notebook-deploy) | Deploy Kaggle Notebooks via `git push` |
| [kaggle-wandb-sync](https://github.com/yasumorishima/kaggle-wandb-sync) | Sync W&B offline runs from Kaggle |
| [signate-deploy](https://github.com/yasumorishima/signate-deploy) | SIGNATE workflow via GitHub Actions |
| [signate-wandb-sync](https://github.com/yasumorishima/signate-wandb-sync) | SIGNATE scores to W&B |

</details>

---

## 🔬 Learning Projects

| Project | Description |
|---|---|
| **[Sansuu, Shogi & Sora](https://github.com/yasumorishima/icp-counter-learning)** | Arithmetic, shogi, planetarium, toddler games · usable without sight · [Live](https://iqjbc-7aaaa-aaaaj-qnnsa-cai.icp0.io/) |
| **[OpenClaw Twitter Bot](https://github.com/yasumorishima/raspi-baseball-bot)** | Pi 5 + Gemini auto-tweet bot (stopped) · [Article (JP)](https://zenn.dev/shogaku/articles/raspi-baseball-bot-openclaw-gemini) |
| **[alexa-rpi5](https://github.com/yasumorishima/alexa-rpi5)** 🔒 | Pi 5 → Fire TV Cube control hub |
| **[Slide Decks with Claude Code](https://github.com/yasumorishima/slide-deck-with-claude-code)** 🔒 | Notes on HTML / PDF slides with Claude Code |

<details>
<summary>Past Projects</summary>

| Project | Description |
|---|---|
| [GAS Calendar Tool](https://github.com/yasumorishima/gas-calendar-tool) | Batch calendar registration |
| [Dune Analytics](https://github.com/yasumorishima/dune-analytics) | [JPYC Stablecoin Dashboard](https://dune.com/shogaku_toushi/jpyc-date) |
| **[selenium-to-playwright](https://github.com/yasumorishima/selenium-to-playwright)** 🔒 | Playwright automation + night batch |
| [Archived Projects](https://github.com/yasumorishima/archived-projects) | Selenium, business tools, etc. |

</details>

---

## 🛠️ Tech Stack
| Category | Technologies |
| --- | --- |
| **Data Analysis & ML** | Python, pandas, scikit-learn, LightGBM, XGBoost, CatBoost, PyTorch, DuckDB, W&B |
| **Data Platform** | Hugging Face Datasets, SQLite, BigQuery sandbox (dbt) |
| **Data Sources** | Baseball Savant (Statcast), pybaseball, USGS, NASA Earthdata, AIS |
| **Web & Dashboards** | Streamlit, Next.js, TypeScript, Supabase, Vercel |
| **Mobile App** | Flutter, Dart |
| **Automation & DevOps** | GitHub Actions, Google Apps Script, VBA, Power Query |
| **Tools** | Claude Code, Kaggle, Colab, Excel, Looker Studio, Tableau Public |
| **Manufacturing** | Statistical Quality Control, Process Engineering |

---

## 📈 Career
* **2024 - Present:** Quality Management @ a semiconductor distributor
* **2008 - 2024:** Semiconductor Manufacturing Process Engineer
  * **2008 - 2014:** Toppan Printing
  * **2014 - 2017:** Toshiba → Toshiba Memory (now Kioxia)

---

## 🏆 Patents
**Stencil mask and manufacturing method thereof** — Patent No. 6307851, Inventor · [Google Patents (JP6307851B2)](https://patents.google.com/patent/JP6307851B2/ja)

---

## 📫 Contact & Blog
* **Site:** [https://yasumorishima.github.io](https://yasumorishima.github.io)
* **Blog:** [DEV.to (EN)](https://dev.to/yasumorishima) / [Zenn (JP)](https://zenn.dev/shogaku) / [Quarto Blog (EN)](https://yasumorishima.github.io/quarto-blog/)
* **Kaggle:** [https://www.kaggle.com/yasunorim](https://www.kaggle.com/yasunorim)
* **Wantedly:** [https://www.wantedly.com/id/yasunori_morishima_b](https://www.wantedly.com/id/yasunori_morishima_b)
* **LinkedIn:** [https://www.linkedin.com/in/morishima-yasunori-b70229241](https://www.linkedin.com/in/morishima-yasunori-b70229241?trk=contact-info)
