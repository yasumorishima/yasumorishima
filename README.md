# Yasunori Morishima (盛島康徳)
Manufacturing Engineer & Data Analyst with <!-- CAREER_YEARS_START -->18<!-- CAREER_YEARS_END --> years of experience, specializing in data analysis, open source contribution, and business automation.
(製造業にて<!-- CAREER_YEARS_JP_START -->18<!-- CAREER_YEARS_JP_END -->年の経験を持つエンジニア。データ分析・OSS貢献・業務自動化を専門としています)

[![Findy Skill Deviation](https://img.shields.io/badge/Findy_Skill_Deviation-73.0-blue)](https://findy-code.io/skills-share/f6fUT0vdoVeI4) <sub>2026-06-01時点: 73.0</sub>

[![Kaggle](https://img.shields.io/badge/Kaggle-Notebooks%20Expert-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/yasunorim)
[![Zenn](https://img.shields.io/badge/Zenn-JP%20articles-3EA8FF?logo=zenn&logoColor=white)](https://zenn.dev/shogaku)
[![DEV.to](https://img.shields.io/badge/DEV.to-EN%20articles-0A0A0A?logo=devdotto&logoColor=white)](https://dev.to/yasumorishima)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/morishima-yasunori-b70229241)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/yasumorishima/yasumorishima/main/assets/dashboard-dark.svg">
  <img alt="At a glance: open-source, GitHub Actions automation, Kaggle and package metrics" src="https://raw.githubusercontent.com/yasumorishima/yasumorishima/main/assets/dashboard-light.svg">
</picture>

**Jump to** — [Robotics](#-robotics--embedded) · [Baseball websites](#-baseball-websites) · [Realtime open data](#-realtime-open-data) · [Baseball analytics](#-baseball-analytics) · [Open source](#-open-source-contributions) · [Competitions](#-data--competitions) · [Dashboards and mobile](#-dashboards--mobile) · [PyPI](#-pypi-packages) · [Learning projects](#-learning-projects) · [Tech stack](#️-tech-stack) · [Career](#-career) · [Patents](#-patents) · [Contact](#-contact--blog)

## 🤖 Robotics / Embedded

### [stackchan-lab](https://github.com/yasumorishima/stackchan-lab) — M5 Stack-chan Development Log (Active)

Official M5Stack Stack-chan (`M5STACK-K151`) moved off its stock cloud assistant onto a self-hosted stack on a Raspberry Pi 5 - 19 server-side tools · 11 device tools over MCP · sings 16 cheer songs · speaks while the model is still writing · stock firmware, unmodified

<details>
<summary>How the voice loop runs</summary>

| Stage | |
| --- | --- |
| Speech in | sherpa-onnx / ReazonSpeech, on the Pi |
| Reply | hosted 120B model, free tier |
| Speech out | Open JTalk, on the Pi (0.27s per sentence), shaped for a speaker that cannot reproduce bass |
| Tools | weather, FX, indices, crypto, NHK headlines, JMA quake / warning / typhoon, heat index, train delays, on-this-day, moon and sun, fuel surcharge, travel advisories, baseball scores and standings, roster notices, cheer-song lyrics, singing a cheer song |
| Device tools | camera, head angles, LED, volume, screen, battery - called through the same function-call array |
| Interrupting | the device sends no mic while it is playing, so the server stops the audio and listens at a silent point |
| Latency | the reply is spoken sentence by sentence as it streams, and only the utterance that just ended is sent to the recogniser |

</details>

<details>
<summary>What went wrong, and what it turned out to be</summary>

| Symptom | Cause |
| --- | --- |
| Pairing failed as `No devices found` | Factory firmware nine releases behind. OTA needs Wi-Fi, Wi-Fi setup needs pairing - USB was the only way in |
| Device kept talking to the stock server | A hand-appended NVS entry padded its key with `0xFF` instead of `0x00`: valid CRC, invisible to my own parser, permanently missed by ESP-IDF |
| OOM-killed at 7GB RSS, twice | A VAD that starts counting at speech never fires on an always-streaming mic |
| Speech played in slow motion | Not length - the same 30 morae read fine as nonsense but break in a real sentence, and one comma puts it right. The server times each synthesis and re-splits what came out slow |
| The rhythm would not come back, whatever I changed | The wall was the ruler. Against a real recording, comparing sound to sound has a floor of 142-680ms: singing at the onsets of the recording itself, which cannot be wrong as rhythm, still reads that, and every difference I had been reading between methods sat inside it. Measured by times against times, with a random control beside it, the notes now land 20-60ms from the onsets against 55-105ms for random - and it sings |
| Conversation sounded quieter than the singing | Not level - band. The singing voice puts over 90% of its energy above 500Hz; the speaking voice puts 73-84% below it, where a speaker this small reproduces nothing. Matching the level in the band that is actually audible fixed what matching the overall level could not |

More of the same, with the measurements behind each, is in the [server notes](https://github.com/yasumorishima/stackchan-lab/tree/main/server#readme).

</details>

Write-up, measurements and tests: [stackchan-lab](https://github.com/yasumorishima/stackchan-lab#readme)

`M5Stack CoreS3 (ESP32-S3) / Raspberry Pi 5 / Python (aiohttp, WebSocket) / sherpa-onnx + ReazonSpeech / Open JTalk / MCP / Opus`

### [rpi5-infra](https://github.com/yasumorishima/rpi5-infra) 🔒 *(private, config record)*

Configuration record for the Raspberry Pi 5 that hosts the robot's server, kept so the box can be rebuilt after an SD failure and so a change like opening a port leaves a trace.

<details>
<summary>What it records, and what it deliberately leaves out</summary>

| | |
| --- | --- |
| Recorded | firewall rules, systemd units, cron entries, listening ports, an inventory of what is actually running |
| Left out | secrets - unit files reference their `EnvironmentFile` without containing values, and credential files are excluded |

</details>

`Raspberry Pi OS / systemd / ufw / cron / Tailscale`

---

## ⚾ Baseball Websites

### [Minami Baseball OB](https://minami-baseball-ob.vercel.app/) — Alumni Association Site (In Production)

Full-stack web app for a high school baseball alumni association — <!--ob:active_users-->11<!--/ob--> active users · <!--ob:pages-->44<!--/ob--> pages · <!--ob:db_tables-->23<!--/ob--> DB tables · <!--ob:e2e_tests-->19<!--/ob--> e2e tests · <!--ob:cost-->¥0<!--/ob-->/mo running cost (<!--ob:ts_files-->157<!--/ob--> files, <!--ob:loc-->~22000<!--/ob--> LOC). **[Technical Documentation](https://github.com/yasumorishima/minami-baseball-ob-docs)**

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

5-tier RBAC (Middleware + RLS), automated member pipeline (Form → GAS → Actions → Supabase), <!--ob:senseki-->686<!--/ob--> match records (1955–present)

<details>
<summary>Architecture & features</summary>

- **5-tier RBAC** (guest → admin): Next.js Middleware + Supabase RLS — authorization at route, row, and component level
- **Automated member pipeline**: Google Form → Apps Script → GitHub Actions auto-PR → Supabase role sync. Personal names never touch Git
- **Custom CMS**: 9 editor pages + 5 inline edit, soft delete (7-day trash + auto-purge), change history, audit logs
- **<!--ob:senseki-->686<!--/ob--> match records** (1955–present): cross-source verification, generation-based grouping, per-game photo management
- **UX**: Unsaved warning, Web Share + LINE fallback, Calendar registration, ripple feedback, Suspense skeleton UI, weather forecast (Open-Meteo, 10 venues), automated game detection (2 sources → auto-PR)
- **Security**: RLS on all 23 tables (17 main + 6 history), `server-only` admin, CODEOWNERS, branch protection, secret scanning, cookie consent, 60-min session timeout
- **Silent-fail monitoring** — built after a 1-month silent outage (a Form trigger silently lost its OAuth grant):
  - Hourly health-check probes the full member-request + feedback pipeline (Vercel proxy / dispatch chain / GAS time trigger / gas-issue-form secret match / role-sync recency)
  - Workflow-run failure + sync-roles liveness (cron-stall) detection auto-opens a tracking GitHub issue and auto-closes it on recovery
  - Dual-channel alerts: GitHub Actions email + GAS Gmail

</details>

`Next.js 15 / TypeScript 5.8 / Tailwind CSS 4 / Supabase (PostgreSQL + Auth + Storage) / Vercel / GitHub Actions / Google Apps Script / GA4`

### [Yokohama Funnies](https://yokohama-funnies.vercel.app/) — Amateur Baseball Team Site (In Production)

Companion site for an amateur baseball team, forked from Minami Baseball OB — <!--fn:players-->23<!--/fn-->-player roster · <!--fn:pages-->48<!--/fn--> pages · <!--fn:db_tables-->31<!--/fn--> DB tables · <!--fn:e2e_tests-->18<!--/fn--> e2e tests · <!--fn:cost-->¥0<!--/fn-->/mo running cost (<!--fn:ts_files-->165<!--/fn--> files, <!--fn:loc-->~23100<!--/fn--> LOC). **[Technical Documentation](https://github.com/yasumorishima/yokohama-funnies-docs)**

5-tier RBAC (Middleware + RLS), PR-based member approval (Form → GAS → Actions auto-PR → merge → role sync), custom amateur-baseball stats schema (per-game batting / pitching / attendance) with manual-input + spreadsheet-migration ingestion

<details>
<summary>Architecture & features</summary>

- **5-tier RBAC** (guest → admin): Next.js Middleware + Supabase RLS — authorization at route, row, and component level (Google OAuth)
- **PR-based member approval** (same topology as Minami): Google Form → Apps Script → Vercel proxy → GitHub App auto-creates an approval PR adding a per-member role file (`config/members/<uid>.yml`); merging triggers a polling role-sync to Supabase + an approval email to the member — approve by merge. Personal data stays minimal in Git
- **Amateur-baseball stats schema**: `players` (jersey / bats / throws / is_guest / photo / comment), per-game `game_player_batting` (14 cols) + `game_player_pitching`, `attendances` (○/△/×); aggregated views + client-side season filter compute 打率 / 出塁率 / 長打率 / OPS / ERA / WHIP / K9
- **Stat ingestion**: spreadsheet migration + editor manual-input UI (`/edit/game-stats`, scorebook image side-by-side + per-player grid); editors upload scorebook images straight from the result page
- **Custom CMS / UX**: dedicated + inline editor pages, soft delete (7-day trash + auto-purge), change history, audit logs, public No. 06 ROSTER section (photo + jersey + role + comment) via `players_public` view, Open-Meteo weather forecast with WBGT heat-stress display
- **Security**: Supabase RLS on all tables, anon-readable roster view with sensitive columns filtered, server-only admin, gitleaks secret scanning, notifications isolated on a separate public Actions repo
- **Silent-fail monitoring**:
  - Hourly health-check probes every notification path (Vercel proxy / dispatch ack / GAS heartbeat / feedback webhook secret)
  - Workflow-run failure + sync-roles liveness detection auto-opens/closes a GitHub issue, with email alerts on any silent failure

</details>

`Next.js 15 / TypeScript 5.8 / Tailwind CSS 4 / Supabase / Vercel / GitHub Actions / Google Apps Script`

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
<td>31 geophysical data sources → ML earthquake prediction (walk-forward AUC ~0.80 via ConvLSTM, CSEP Molchan 0.981) + real-time monitoring dashboard</td>
<td>AIS vessel tracking across the Persian Gulf & Gulf of Oman with land mask filtering<br><br>🛑 <b>Stopped</b> — RPi5 SSD failure (2026-05-16).</td>
</tr>
</table>

`Real-time API / WebSocket → SQLite → FastAPI + Leaflet.js (dark theme)` — [All projects](https://github.com/yasumorishima/realtime-open-data)

**[Japan Geohazard Monitor](https://github.com/yasumorishima/japan-geohazard-monitor)** — Earthquake prediction research

<details>
<summary>Data sources, evaluation and the Kumamoto InSAR result</summary>

- **85 features from 25+ sources** — USGS, NASA Earthdata, INTERMAGNET, NMDB, NOAA, IOC
- **Walk-forward evaluation** — HistGBT + elastic-net + ConvLSTM, best walk-forward AUC ~0.80 (Kaggle T4)
- **Open data & automation** — features published as a public Hugging Face dataset, weekly CI pipeline on GitHub Actions
- **Co-seismic InSAR** — 2026 Kumamoto M7.1 measured from open Sentinel-1 on ASF HyP3: line-of-sight displacement −21.7 to +15.0 cm and a coherence-change damage proxy ([method, figures and caveats](https://github.com/yasumorishima/japan-geohazard-monitor/tree/master/research/kumamoto2026_insar))

</details>

---

## ⚾ Baseball Analytics

### Prediction Systems

| Project | Description | Demo |
|---|---|---|
| **[NPB Season Prediction](https://github.com/yasumorishima/npb-prediction)** | Bayesian ensemble (Marcel 35% + Stan/Ridge 40% + ML 25%) + Monte Carlo team simulation + 24 foreign player individual projections | [Live](https://npb-prediction.streamlit.app/) |
| **[NPB 2021 Backtest](https://github.com/yasumorishima/npb-2021-backtest)** | Could Bayesian model predict Yakult & Orix last→champion? 25 foreign players with FanGraphs data | [Analysis](https://github.com/yasumorishima/npb-2021-backtest) |
| **[MLB Win Probability Engine](https://github.com/yasumorishima/mlb-win-probability)** | 3-engine ensemble WP (Normal + Empirical + LightGBM) + Gemini AI commentary | [Live](https://mlb-wp-engine.streamlit.app/) |
| **[Baseball MLOps Pipeline](https://github.com/yasumorishima/baseball-mlops)** | Statcast MLOps: 5-model ensemble — weekly auto-retrain paused (BigQuery retired 2026-04, data layer being rebuilt on Hugging Face) | [Live](https://baseball-mlops.streamlit.app/) |
| **[MLB Data Pipeline](https://github.com/yasumorishima/mlb-data-pipeline)** | Shared data platform — FanGraphs + Savant + Statcast published as a public Hugging Face dataset, weekly auto-refresh via GitHub Actions | [HF Dataset](https://huggingface.co/datasets/yasumorishima/mlb-stats) |

<details>
<summary>Prediction accuracy & details</summary>

| System | Key Metric | Articles |
|--------|-----------|----------|
| **NPB 2026** | 8-yr backtest wOBA MAE .0498, 97% prob. of beating Marcel. 10K Monte Carlo sims | [JP](https://zenn.dev/shogaku/articles/npb-bayes-integration-production) / [EN](https://dev.to/yasumorishima/adding-bayesian-ensemble-monte-carlo-to-an-npb-prediction-app-58po) |
| **NPB 2021 Backtest** | MAE 10.7W — Yakult & Orix last→champion driven by JP player breakouts, not foreign players | [Repo](https://github.com/yasumorishima/npb-2021-backtest) |
| **MLB WP Engine** | 3-engine ensemble, 367K+ play states (2015–2024), inverse-Brier weighted + Isotonic calibration | [Live](https://mlb-wp-engine.streamlit.app/) |
| **Baseball MLOps** | Batter wOBA MAE .0287 (Marcel: .0326) / Pitcher xFIP MAE 0.483 (Marcel: 0.558) | [Live](https://baseball-mlops.streamlit.app/) |

</details>

### Biomechanics

**[Baseball Skeleton Analysis](https://github.com/yasumorishima/baseball-cv)** — 3D skeleton visualization from Driveline OpenBiomechanics C3D data

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

Trunk rotation range vs pitch speed: r=0.425 (strongest). Contributed bug fix [PR #384](https://github.com/pyomeca/ezc3d/pull/384) to ezc3d.
[Article (JP)](https://zenn.dev/shogaku/articles/baseball-cv-skeleton-biomechanics) / [Article (EN)](https://dev.to/yasumorishima/3d-skeleton-detection-from-baseball-motion-capture-data-with-driveline-c3d-29ja)

### [Handwritten Scorebook OCR](https://github.com/yasumorishima/baseball-scorebook-ocr) 🔒 *(private R&D, active)*

**Amateur Baseball Scorebook Reader** — reads handwritten Japanese paper scorebooks (紙スコアブック) from photos into structured at-bat data. **76% → 93%** on the hardest mark class, evaluated on **29 hand-transcribed ground-truth sheets**.

<details>
<summary>How it reads the sheets, and how it is evaluated</summary>

- **No paid APIs, no cloud OCR** — deterministic computer vision (OpenCV on a Raspberry Pi 5)
- **Game-logic constraint solver** — only accepts readings consistent with legal base-running; fused with template matching it lifted the hardest mark class from 76% to **93% pooled**
- **Honest, live evaluation** — the ground-truth archive is complete and still growing (the latest game was transcribed the day it was played); every new sheet serves as a **held-out generalization test** before joining the pool — 27 consecutive held-out sheets so far, some read perfectly
- **Real output** — my team's 2026 season batting stats are compiled from this ground truth

</details>

Private repo (the method is the product) — public technical write-up: [baseball-scorebook-ocr-docs](https://github.com/yasumorishima/baseball-scorebook-ocr-docs) (JP)

### Statcast Analysis

<!-- MLB_STATS_START -->6 analyses<!-- MLB_STATS_END --> covering Japanese MLB pitchers and Ohtani batting data.

<details>
<summary>All analyses (6)</summary>

| Analysis | Key Finding | Article |
|----------|-------------|---------|
| **Kikuchi Slider Revolution (2019-2025)** | SL 17%→37% after Astros trade | [Zenn](https://zenn.dev/shogaku/articles/kikuchi-slider-revolution-2019-2025) / [DEV.to](https://dev.to/yasumorishima/yusei-kikuchis-pitching-evolution-a-statcast-analysis-2019-2025-2a4a) / [Kaggle](https://www.kaggle.com/code/yasunorim/kikuchi-slider-revolution-2019-2025) |
| **Senga Ghost Fork (2023-2025)** | FO whiff rate 58%→39%, decline pre-injury | [Zenn](https://zenn.dev/shogaku/articles/senga-ghost-fork-analysis-2023-2025) / [DEV.to](https://dev.to/yasumorishima/kodai-sengas-ghost-fork-analyzed-with-statcast-data-2023-2025-1k1d) / [Kaggle](https://www.kaggle.com/code/yasunorim/senga-ghost-fork-analysis-2023-2025) |
| **Imanaga 2nd Year (2024-2025)** | 3-pitch concentration (97%), 1st TTO xwOBA .505 | [Zenn](https://zenn.dev/shogaku/articles/imanaga-2nd-year-analysis-2024-2025) / [DEV.to](https://dev.to/yasumorishima/shota-imanagas-sophomore-year-what-statcast-data-reveals-2024-2025-235) / [Kaggle](https://www.kaggle.com/code/yasunorim/imanaga-rookie-to-sophomore-pitching) |
| **Darvish Evolution (2021-2025)** | SL/ST halved, CU became putaway pitch | [Zenn](https://zenn.dev/shogaku/articles/darvish-pitching-evolution-2021-2025) / [DEV.to](https://dev.to/yasumorishima/yu-darvishs-pitching-evolution-2021-2025-a-statcast-data-analysis-fij) / [Kaggle](https://www.kaggle.com/code/yasunorim/darvish-pitching-evolution) |
| **Ohtani Spray Chart** | spraychart() one-liner vs matplotlib manual | [Zenn](https://zenn.dev/shogaku/articles/pybaseball-spraychart-ohtani) |
| **Ohtani Heatmap** | Stadium drawing + hit density heatmap | [Zenn](https://zenn.dev/shogaku/articles/matplotlib-baseball-heatmap) |

</details>

---

## 🌐 Open Source Contributions

<!-- OSS_STATS_START -->(101 PRs / 54 Merged)<!-- OSS_STATS_END --> across 46 repositories. See [oss-contributions](https://github.com/yasumorishima/oss-contributions) for full details.

<details>
<summary>PR highlights (click to expand)</summary>

| Repository | PR | Description |
|---|---|---|
| **dfinity/icp-js-core** | [#1270](https://github.com/dfinity/icp-js-core/pull/1270) | Improve Candid decode error messages |
| **line/line-bot-mcp-server** | [#369](https://github.com/line/line-bot-mcp-server/pull/369) | Add get_follower_ids tool |
| **pyomeca/ezc3d** | [#384](https://github.com/pyomeca/ezc3d/pull/384) | Fix `__eq__` early return bug |
| **codeforjapan/mapprint** | [#556](https://github.com/codeforjapan/mapprint/pull/556) | Share buttons on the disaster print map |
| **codeforjapan/mapprint** | [#564](https://github.com/codeforjapan/mapprint/pull/564) | Deterministic list order on the printable map |
| **codeforjapan/mapprint** | [#563](https://github.com/codeforjapan/mapprint/pull/563) | 2026 Kumamoto earthquake paper map |
| **codeforjapan/BirdXplorer** | [#281](https://github.com/codeforjapan/BirdXplorer/pull/281) | Statement timeouts for the Community Notes API |
| **hotosm/openaerialmap** | [#289](https://github.com/hotosm/openaerialmap/pull/289) | Stop the STAC ingester dropping the wrong record when an entry fails |
| **apache/fineract-backoffice-ui** | [#321](https://github.com/apache/fineract-backoffice-ui/pull/321) | Translate the accounting screen titles and tooltips |
| **daisy/MathCAT** | [#665](https://github.com/daisy/MathCAT/pull/665) | Fix chemistry assertions that could never fail |
| **PHPOffice/PHPPresentation** | [#897](https://github.com/PHPOffice/PHPPresentation/pull/897) | Fix PHP 8.4/8.5 static analysis by fixing 144 findings instead of ignoring them |
| **project-inclusive/OpenFisca-Japan** | [#479](https://github.com/project-inclusive/OpenFisca-Japan/pull/479) | Add the vocational training benefit for single-parent families to Japan's welfare rules engine |
| **project-inclusive/OpenFisca-Japan** | [#480](https://github.com/project-inclusive/OpenFisca-Japan/pull/480) | Add the housing security benefit to Japan's welfare rules engine |
| **project-inclusive/OpenFisca-Japan** | [#481](https://github.com/project-inclusive/OpenFisca-Japan/pull/481) | Add the welfare loan fund for single-parent families and widows to Japan's welfare rules engine |
| **project-inclusive/OpenFisca-Japan** | [#482](https://github.com/project-inclusive/OpenFisca-Japan/pull/482) | Add the school-cost assistance eligibility check to Japan's welfare rules engine |
| **project-inclusive/OpenFisca-Japan** | [#483](https://github.com/project-inclusive/OpenFisca-Japan/pull/483) | Add the higher-education tuition and entrance-fee reduction to Japan's welfare rules engine |
| **project-inclusive/OpenFisca-Japan** | [#484](https://github.com/project-inclusive/OpenFisca-Japan/pull/484) | Add the jobseeker support benefit paid during free vocational training to Japan's welfare rules engine |
| **optuna/optuna** | — | Hyperparameter optimization framework |
| **pandas-dev/pandas** | — | Data analysis library |
| **jldbc/pybaseball** | [#498-504](https://github.com/jldbc/pybaseball) | Bug fixes & documentation |

<details>
<summary>team-mirai — Civic Tech OSS (<!-- TEAM_MIRAI_STATS_START -->26 PRs (14 Merged / 4 Open / 8 Closed)<!-- TEAM_MIRAI_STATS_END -->)</summary>

Civic tech projects for political transparency & citizen participation in Japan. Next.js / TypeScript / Supabase / Vitest.

| Repository | Highlights |
|---|---|
| **action-board** | [48 unit tests](https://github.com/team-mirai-volunteer/action-board/pull/1969), [RPC tests](https://github.com/team-mirai-volunteer/action-board/pull/1869), [breadcrumb nav](https://github.com/team-mirai-volunteer/action-board/pull/1849), [cache fix](https://github.com/team-mirai-volunteer/action-board/pull/1845) + 5 more |
| **mirai-gikai** | [Supabase CLI v2.106 seed permission fix](https://github.com/team-mirai/mirai-gikai/pull/930), [Safari/iOS ruby spacing fix](https://github.com/team-mirai/mirai-gikai/pull/932) |
| **fact-checker** | [X API investigation](https://github.com/team-mirai-volunteer/fact-checker/issues/69#issuecomment-3811711591) + 5 PRs |

</details>

</details>

---

## 📊 Data & Competitions

### Kaggle

<!-- KAGGLE_COMP_STATS_START -->Notebooks Expert | 🥉 15 Bronze Notebook Medals<!-- KAGGLE_COMP_STATS_END -->

**Active:**
- **SIGNATE NEDO Challenge — Baggage-Loading Optimization** — 3D bin packing for airline ULD containers, hybrid offline+online packing agent (¥15M prize pool, Jul–Oct 2026)
- **[Kaggriculture](https://www.kaggle.com/competitions/kaggriculture)** — two-player farm-economy simulation, scored by ladder rating rather than by money ($50K prize pool, to 2026-09-30). Agent and its measurement harness in [`kaggle-competitions/kaggriculture`](https://github.com/yasumorishima/kaggle-competitions/tree/main/kaggriculture)

**Finished 2026:** [ROGII Wellbore Geology](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) ($50K wellbore TVT regression, closed 2026-08-05 — public LB 7.311, final public rank 2545/6125) · [Playground Series S6E6 - Stellar Classification](https://www.kaggle.com/competitions/playground-series-s6e6) (macro-F1, private LB 0.95939) · NIR Moisture Prediction (SIGNATE, wood spectroscopy) · [Stanford RNA 3D Folding 2](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2) · [BirdCLEF+ 2026](https://www.kaggle.com/competitions/birdclef-2026)

<details>
<summary>Bronze Medal Notebooks (15)</summary>

| Notebook | Topic |
|----------|-------|
| [savant-extras Defense & Pitching Quality](https://www.kaggle.com/code/yasunorim/savant-extras-defense-pitching-quality) | Defense metrics & pitching quality (savant-extras) |
| [MLB Statcast Spray Charts for WBC 2026](https://www.kaggle.com/code/yasunorim/mlb-statcast-spray-charts-for-wbc-2026-players) | WBC 2026 spray + pitch zone charts (baseball-field-viz) |
| [March Machine Learning Mania 2026](https://www.kaggle.com/code/yasunorim/march-machine-learning-mania-2026-baseline) | NCAA tournament prediction (LightGBM) |
| [NFL Geometric Rules Baseline](https://www.kaggle.com/code/yasunorim/geometric-rules-baseline-2-921-rmse-no-ml) | Physics-based rules, No ML, RMSE 2.921 |
| [CAFA 6 Baseline](https://www.kaggle.com/code/yasunorim/baseline-with-regularization) | Protein function prediction (PyTorch MLP) |

[All 15 notebooks →](https://www.kaggle.com/yasunorim/code)

</details>

### Kaggle Datasets

<!-- KAGGLE_DS_STATS_START -->8 public datasets<!-- KAGGLE_DS_STATS_END -->

| Dataset | Description |
|---------|-------------|
| 🥈 [MLB Bat Tracking Leaderboard (2024-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-bat-tracking-2024-2025) | 452 batters, 19 swing metrics |
| 🥈 [WBC 2026 Scouting](https://www.kaggle.com/datasets/yasunorim/wbc-2026-scouting) | 306 players, 20 countries |

<details>
<summary>Other datasets (6)</summary>

| Dataset | Description |
|---------|-------------|
| [Baseball Savant Leaderboards (2024-2025)](https://www.kaggle.com/datasets/yasunorim/baseball-savant-leaderboards-2024) | 15 leaderboards, 2 seasons combined |
| [Japanese MLB Players Statcast (2015-2025)](https://www.kaggle.com/datasets/yasunorim/japan-mlb-pitchers-batters-statcast) | 34 Japanese MLB players, 174k pitches+hits |
| [MLB Pitcher Arsenal Evolution (2020-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-pitcher-arsenal-2020-2025) | 4,253 pitcher-seasons, 111 metrics |
| [MLB Statcast + Bat Tracking (2024-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-statcast-bat-tracking-2024-2025) | Combined Statcast + bat tracking data |
| [XC BirdCLEF 2026 Target Recordings (URLs)](https://www.kaggle.com/datasets/yasunorim/xc-birdclef-2026-target-urls) | Xeno-canto source URLs for the 2026 target species |
| [BEATs iter3+ AS2M Pretrained](https://www.kaggle.com/datasets/yasunorim/beats-pretrained) | Audio-tagging checkpoint mirrored for offline notebooks |

</details>

### DrivenData

**[DrivenData Competitions](https://github.com/yasumorishima/drivendata-comp)** — Automated pipeline: GitHub Actions + GPU training + GPU→CPU fallback.
Most recently competed in [On Top of Pasketti](https://www.drivendata.org/competitions/309/) (Children's ASR, $120K prize, Wav2Vec2 CTC; submission deadline 2026-04-06).

---

## 📱 Dashboards & Mobile

| App | Description | Link |
|---|---|---|
| **[MLB Bat Tracking Dashboard](https://github.com/yasumorishima/mlb-bat-tracking-dashboard)** | Leaderboard, Player Comparison, Team Lineup Builder. Powered by savant-extras | [Live](https://yasumorishima-mlb-bat-tracking.streamlit.app/) |
| **[WBC 2026 Scouting Dashboard](https://github.com/yasumorishima/wbc-scouting)** | 30 Statcast apps across 19 countries. Zone heatmaps, spray charts, pitch movement | [Live](https://wbc-scouting-usa-batters.streamlit.app/) |
| **[Daily Diary](https://github.com/yasumorishima/diary-app-flutter)** | Flutter mobile app, 10 languages, offline-first, biometric app lock, daily reminder, Android Auto Backup, AdMob · links to Sansuu/Shogi/Sora (ja only) | [Google Play](https://play.google.com/store/apps/details?id=com.diary.daily) |
| **[Fire Tablet Google Play Helper](https://github.com/yasumorishima/yasumorishima.github.io/tree/main/fire-gapps)** | Detects Fire OS from the browser UA, then lists the four required APKs in install order with step gating and saved progress | [Live](https://yasumorishima.github.io/fire-gapps/) |

<details>
<summary>WBC 2026 Scouting Dashboard details (30 apps)</summary>

30 Statcast scouting apps across 19 countries (batters + pitchers). Zone heatmaps, spray charts, pitch movement, LHP/RHP splits. Auto-fetched via GitHub Actions.
→ [USA Batters](https://wbc-usa-batters.streamlit.app/) / [Japan Pitchers](https://wbc-japan-pitchers.streamlit.app/) / [All 30 apps](https://github.com/yasumorishima/wbc-scouting#-デプロイ済みアプリ一覧)

</details>

---

## 📦 PyPI Packages

<details>
<summary>6 packages (click to expand)</summary>

| Package | Description |
|---------|-------------|
| [savant-extras](https://github.com/yasumorishima/savant-extras) | 17 Baseball Savant leaderboards + date range support. Complements pybaseball |
| [baseball-field-viz](https://github.com/yasumorishima/baseball-field-viz) | Statcast coordinate transform + field drawing + spray charts + pitch zone charts |
| [kaggle-notebook-deploy](https://github.com/yasumorishima/kaggle-notebook-deploy) | Deploy Kaggle Notebooks via `git push` + GitHub Actions |
| [kaggle-wandb-sync](https://github.com/yasumorishima/kaggle-wandb-sync) | Sync W&B offline runs from Kaggle to W&B cloud |
| [signate-deploy](https://github.com/yasumorishima/signate-deploy) | SIGNATE competition workflow via GitHub Actions |
| [signate-wandb-sync](https://github.com/yasumorishima/signate-wandb-sync) | Record SIGNATE scores to W&B runs |

</details>

---

## 🔬 Learning Projects

| Project | Description |
|---|---|
| **[Sansuu, Shogi & Sora](https://github.com/yasumorishima/icp-counter-learning)** | Three modes on the Internet Computer: arithmetic (36 topics) · shogi · **sora**, a planetarium drawing the real sky for any place and time. English/Japanese, offline, records on-device — [Live](https://iqjbc-7aaaa-aaaaj-qnnsa-cai.icp0.io/) |
| **[OpenClaw Twitter Bot](https://github.com/yasumorishima/raspi-baseball-bot)** | Raspberry Pi 5 + OpenClaw + Gemini API auto-tweet bot (stopped) — [Article (JP)](https://zenn.dev/shogaku/articles/raspi-baseball-bot-openclaw-gemini) |
| **[alexa-rpi5](https://github.com/yasumorishima/alexa-rpi5)** 🔒 | Raspberry Pi 5 to Fire TV Cube control hub for a house with no Echo speaker: cube wrapper, watchers and integrations (details in the repo README) |

<details>
<summary>Past Projects</summary>

| Project | Description |
|---|---|
| [GAS Calendar Tool](https://github.com/yasumorishima/gas-calendar-tool) | Batch calendar event registration with senior-friendly mobile UI |
| [Dune Analytics](https://github.com/yasumorishima/dune-analytics) | On-chain data analysis — [JPYC Stablecoin Dashboard](https://dune.com/shogaku_toushi/jpyc-date) |
| **[selenium-to-playwright](https://github.com/yasumorishima/selenium-to-playwright)** 🔒 | Playwright browser automation: 20+ scripts + night batch runner with auto GitHub Issues |
| [Archived Projects](https://github.com/yasumorishima/archived-projects) | Selenium automation, business workflow tools, etc. |

</details>

---

## 🛠️ Tech Stack
| Category | Technologies |
| --- | --- |
| **Data Analysis & ML** | Python, pandas, scikit-learn, LightGBM, XGBoost, CatBoost, PyTorch, matplotlib, seaborn, DuckDB, W&B |
| **Data Platform** | Hugging Face Datasets (MLB / NPB / geohazard — public, auto-refreshed via GitHub Actions), SQLite, ~~BigQuery + BQML + Cloud Run + Grafana~~ (retired 2026-04) |
| **Data Sources** | Baseball Savant (Statcast), pybaseball, USGS, NASA Earthdata, AIS |
| **Web & Dashboards** | Streamlit, Next.js, TypeScript, Supabase, Vercel, shadcn/ui |
| **Mobile App** | Flutter, Dart, Hive, Google AdMob |
| **Automation & DevOps** | GitHub Actions, Google Apps Script, VBA, Power Query |
| **Tools** | Claude Code, Kaggle, Google Colab, Excel, Looker Studio |
| **Manufacturing** | Statistical Quality Control, Process Engineering |

---

## 📈 Career
* **2024 - Present:** Quality Management @ Marubun Corporation
* **2008 - 2024:** Semiconductor Manufacturing Process Engineer (半導体製造プロセスエンジニア)

---

## 🏆 Patents
**Stencil mask and manufacturing method thereof (ステンシルマスク及びその製造方法)**
* **Patent No:** 6307851 (特許第6307851号)
* **Role:** Inventor (発明者)
* **Link:** [Google Patents (JP6307851B2)](https://patents.google.com/patent/JP6307851B2/ja)

---

## 📫 Contact & Blog
* **Site:** [https://yasumorishima.github.io](https://yasumorishima.github.io) — tools and blog hosted on this domain
* **Blog:** [DEV.to (EN)](https://dev.to/yasumorishima) / [Zenn (JP)](https://zenn.dev/shogaku) / [Quarto Blog (EN)](https://yasumorishima.github.io/quarto-blog/)
* **Kaggle:** [https://www.kaggle.com/yasunorim](https://www.kaggle.com/yasunorim)
* **Wantedly:** [https://www.wantedly.com/id/yasunori_morishima_b](https://www.wantedly.com/id/yasunori_morishima_b)
* **LinkedIn:** [https://www.linkedin.com/in/morishima-yasunori-b70229241](https://www.linkedin.com/in/morishima-yasunori-b70229241?trk=contact-info)
