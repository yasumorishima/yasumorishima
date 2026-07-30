# Yasunori Morishima (盛島康徳)
Manufacturing Engineer & Data Analyst with <!-- CAREER_YEARS_START -->18<!-- CAREER_YEARS_END --> years of experience, specializing in data analysis, open source contribution, and business automation.
(製造業にて<!-- CAREER_YEARS_JP_START -->18<!-- CAREER_YEARS_JP_END -->年の経験を持つエンジニア。データ分析・OSS貢献・業務自動化を専門としています)

[![Findy Skill Deviation](https://img.shields.io/badge/Findy_Skill_Deviation-73.0-blue)](https://findy-code.io/skills-share/f6fUT0vdoVeI4) <sub>2026-06-01時点: 73.0</sub>

## 🤖 Robotics / Embedded

### [stackchan-lab](https://github.com/yasumorishima/stackchan-lab) — M5 Stack-chan Development Log (Active)

Development log and tooling for the official M5Stack Stack-chan (`M5STACK-K151` — CoreS3 + 2× FEETECH SCS0009 serial servos).

Straight out of the box, pairing from the companion app never completed — it only reported `No devices found`. Permissions and rescans changed nothing. **Reading the USB serial log showed that the BLE connection and the handshake both succeeded, which placed the failure in the app's response-verification stage rather than in discovery.** The cause was factory firmware nine releases behind, and the update path was circular — **new firmware needs OTA → OTA needs Wi-Fi → Wi-Fi setup needs pairing** — leaving USB flashing as the only way in.

<details>
<summary>Technical highlights</summary>

- **Diagnose from the log, not from the message** — `No devices found` did not describe what was actually happening. `NimBLE: connection established` → `Config data received {"cmd":"handshake"}` → `Config notification sent` all succeeded, which located the failure in verification rather than scanning
- **Firmware update without the M5Burner GUI** — the firmware distribution API is public, so fetching the official binary and flashing it can be done entirely from the CLI ([steps](https://github.com/yasumorishima/stackchan-lab/blob/main/docs/setup/firmware-flash.md) / [script](https://github.com/yasumorishima/stackchan-lab/blob/main/tools/flash-official-firmware.ps1)). `esptool` is used as a standalone executable, so no Python installation is required
- **Building from source does not help** — the handshake implementation in the public source is a stub (a weak symbol that the official build overrides), so an official binary is required
- **Hardware limits read off the firmware** — the firmware sets the AXP2101 charge current to 700mA, so a 500mA PC USB port never starts charging

</details>

The stock voice assistant sends speech to servers in China, so the device was pointed at a Raspberry Pi 5 on the local network instead. The firmware stays the official binary — only an NVS setting changes the destination — and a server that answers OTA and WebSocket was implemented. **Speech recognition and synthesis run entirely locally**, and the tools the device itself exposes (over MCP) can be called.

<details>
<summary>Technical highlights</summary>

- **The speech-recognition backend was chosen by measurement** — 12 synthesized sentences were passed through the same Opus path as the device (16kHz / 60ms) before recognition, then compared by character error rate and RTF (processing time relative to audio length)

  | Backend | CER | RTF |
  | --- | --- | --- |
  | sherpa-onnx + ReazonSpeech k2 v2 (int8) | 4.3% | 0.16 |
  | Vosk small-ja 0.22 | 11.3% | 1.05 |
  | faster-whisper small (int8) | 1.4% | 2.48 |

  faster-whisper is the most accurate, but at RTF 2.48 a 2.5-second utterance takes 6 seconds, which is not a conversation. The sherpa-onnx errors are orthographic only (明日 → あした) and never change the meaning, so it became the default
- **Never await inside the receive loop** — awaiting utterance handling there leaves the server unable to read the reply to its own tool call, which then times out after 10 seconds. Moving it to a separate task brought that to 8ms
- **Tools are called over MCP** — the device is the MCP server and this server is the client: `initialize` and `tools/list` right after connect, then `tools/call` whenever the model returns a function call ([implementation](https://github.com/yasumorishima/stackchan-lab/tree/main/server))
- **Putting the clock in the system prompt threw away the prompt cache on every turn** — tool definitions render *after* the system message in the chat template, so a timestamp that changes by the minute invalidates them too. Measured on the same exchange: **35.1s versus 7.8s** per round trip. The timestamp moved to the user turn instead
- **Pressing the model harder made it stop calling tools** — when a follow-up like "then how about Tottori?" dropped the date argument, marking that argument `required` (or asking for it in prose) made the 3B model **skip the tool entirely and invent the numbers**, down to 1 call in 9. The pressure was removed and the server now resolves the omission itself: a date word in the utterance, else the date asked about moments earlier, else today — with a 180-second limit so a half-hour-old "tomorrow" is never carried into a fresh question
- **Every added instruction cost tool-calling accuracy**, so the shape of the reply is enforced in code rather than requested in prose (3 runs per case, same probe)

  | System prompt | Tool calls | Within 2 sentences |
  | --- | --- | --- |
  | none | 7/9 | 3/9 |
  | previous wording | 4/9 | 6/9 |
  | with instructions added | 1/9 | 8/9 |
  | trimmed + enforced in code | 7/9 | 9/9 spoken |

  The prompt now carries only what code cannot enforce — use the tools, do not invent facts — while sentence count and length are trimmed before speaking
- **It keeps talking with the internet unplugged** — recognition and synthesis were already local, so only response generation needed a second path. It falls back to a local model on the far end's problems (401/403/429/5xx, refused connections, timeouts) but never on 400/404/422, which mean the request itself was malformed. While the primary is down it is not retried on every turn, since one utterance calls it twice and the robot would sit silent through both timeouts. The fallback is verified without running any inference, using a throwaway OpenAI-compatible server in the test itself
- **A bigger model was not the answer** — the same probe on a 7B scored worse than the 3B and mixed in nonsense tokens, and on an 8GB Raspberry Pi it filled swap until sshd could no longer complete a handshake. The host was never down, which is worth knowing: a TCP connect that succeeds but stalls before the banner means starvation, not an outage
- **Synthesis runs per sentence** — the next sentence is synthesized in the background during playback, so the first audio arrives in 2.2–2.5 seconds
- **Never put a changing value in the system prompt** — chat templates render the tool definitions *after* the system message, so a per-minute timestamp there discards the cached prefix and re-processes ~250 tokens of tool definitions every turn. A/B over the same utterances measured **35.1s vs 7.8s per round trip** (96 vs 360 tokens reused). The timestamp now rides on the latest user message instead
- **Keep the tool round trip in the history** — storing only the final sentence made the model answer an elliptical follow-up (“and how about Tottori?”) with invented numbers instead of calling the tool again. Persisting the `tool_calls` and their results fixed it, with trimming that never separates a `tool` message from its `tool_calls`

</details>

`ESP32-S3 / ESP-IDF / esptool / Python / asyncio / sherpa-onnx / VOICEVOX / MCP`

## ⚾ Baseball Websites

### [Minami Baseball OB](https://minami-baseball-ob.vercel.app/) — Alumni Association Site (In Production)

Full-stack web app for a high school baseball alumni association — <!--ob:active_users-->11<!--/ob--> active users · <!--ob:pages-->43<!--/ob--> pages · <!--ob:db_tables-->23<!--/ob--> DB tables · <!--ob:e2e_tests-->18<!--/ob--> e2e tests · <!--ob:cost-->¥0<!--/ob-->/mo running cost (<!--ob:ts_files-->149<!--/ob--> files, <!--ob:loc-->~17300<!--/ob--> LOC). **[Technical Documentation](https://github.com/yasumorishima/minami-baseball-ob-docs)**

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

5-tier RBAC (Middleware + RLS), automated member pipeline (Form → GAS → Actions → Supabase), <!--ob:senseki-->681<!--/ob--> match records (1955–present)

<details>
<summary>Architecture & features</summary>

- **5-tier RBAC** (guest → admin): Next.js Middleware + Supabase RLS — authorization at route, row, and component level
- **Automated member pipeline**: Google Form → Apps Script → GitHub Actions auto-PR → Supabase role sync. Personal names never touch Git
- **Custom CMS**: 9 editor pages + 5 inline edit, soft delete (7-day trash + auto-purge), change history, audit logs
- **<!--ob:senseki-->681<!--/ob--> match records** (1955–present): cross-source verification, generation-based grouping, per-game photo management
- **UX**: Unsaved warning, Web Share + LINE fallback, Calendar registration, ripple feedback, Suspense skeleton UI, weather forecast (Open-Meteo, 10 venues), automated game detection (2 sources → auto-PR)
- **Security**: RLS on all 22 tables (16 main + 6 history), `server-only` admin, CODEOWNERS, branch protection, secret scanning, cookie consent, 60-min session timeout
- **Silent-fail monitoring** — built after a 1-month silent outage (a Form trigger silently lost its OAuth grant):
  - Hourly health-check probes the full member-request + feedback pipeline (Vercel proxy / dispatch chain / GAS time trigger / gas-issue-form secret match / role-sync recency)
  - Workflow-run failure + sync-roles liveness (cron-stall) detection auto-opens a tracking GitHub issue and auto-closes it on recovery
  - Dual-channel alerts: GitHub Actions email + GAS Gmail

</details>

`Next.js 15 / TypeScript 5.8 / Tailwind CSS 4 / Supabase (PostgreSQL + Auth + Storage) / Vercel / GitHub Actions / Google Apps Script / GA4`

### [Yokohama Funnies](https://yokohama-funnies.vercel.app/) — Amateur Baseball Team Site (In Production)

Companion site for an amateur baseball team, forked from Minami Baseball OB — <!--fn:players-->23<!--/fn-->-player roster · <!--fn:pages-->43<!--/fn--> pages · <!--fn:db_tables-->26<!--/fn--> DB tables · <!--fn:e2e_tests-->18<!--/fn--> e2e tests · <!--fn:cost-->¥0<!--/fn-->/mo running cost (<!--fn:ts_files-->146<!--/fn--> files, <!--fn:loc-->~16900<!--/fn--> LOC). **[Technical Documentation](https://github.com/yasumorishima/yokohama-funnies-docs)**

5-tier RBAC (Middleware + RLS), PR-based member approval (Form → GAS → Actions auto-PR → merge → role sync), custom amateur-baseball stats schema (per-game batting / pitching / attendance) with manual-input + spreadsheet-migration ingestion

<details>
<summary>Architecture & features</summary>

- **5-tier RBAC** (guest → admin): Next.js Middleware + Supabase RLS — authorization at route, row, and component level (Google OAuth)
- **PR-based member approval** (same topology as Minami): Google Form → Apps Script → Vercel proxy → GitHub App auto-creates an approval PR editing a roles allowlist (`config/members.yml`); merging triggers a polling role-sync to Supabase + an approval email to the member — approve by merge. Personal data stays minimal in Git
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

- **85 features from 25+ sources** — USGS, NASA Earthdata, INTERMAGNET, NMDB, NOAA, IOC
- **Walk-forward evaluation** — HistGBT + elastic-net + ConvLSTM, best walk-forward AUC ~0.80 (Kaggle T4)
- **Open data & automation** — features published as a public Hugging Face dataset, weekly CI pipeline on GitHub Actions

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

- **No paid APIs, no cloud OCR** — deterministic computer vision (OpenCV on a Raspberry Pi 5)
- **Game-logic constraint solver** — only accepts readings consistent with legal base-running; fused with template matching it lifted the hardest mark class from 76% to **93% pooled**
- **Honest, live evaluation** — the ground-truth archive is complete and still growing (the latest game was transcribed the day it was played); every new sheet serves as a **held-out generalization test** before joining the pool — 27 consecutive held-out sheets so far, some read perfectly
- **Real output** — my team's 2026 season batting stats are compiled from this ground truth

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

<!-- OSS_STATS_START -->(77 PRs / 41 Merged)<!-- OSS_STATS_END --> across 35 repositories. See [oss-contributions](https://github.com/yasumorishima/oss-contributions) for full details.

<details>
<summary>PR highlights (click to expand)</summary>

| Repository | PR | Description |
|---|---|---|
| **dfinity/icp-js-core** | [#1270](https://github.com/dfinity/icp-js-core/pull/1270) | Improve Candid decode error messages |
| **dfinity/icp-js-core** | [#1277](https://github.com/dfinity/icp-js-core/pull/1277) | Deduplicate parallel fetchSubnetKeys |
| **dfinity/pic-js** | [#235](https://github.com/dfinity/pic-js/pull/235) | Add fetchCanisterLogs() method |
| **line/line-bot-mcp-server** | [#369](https://github.com/line/line-bot-mcp-server/pull/369) | Add get_follower_ids tool |
| **pyomeca/ezc3d** | [#384](https://github.com/pyomeca/ezc3d/pull/384) | Fix `__eq__` early return bug |
| **codeforjapan/mapprint** | [#556](https://github.com/codeforjapan/mapprint/pull/556) | Share buttons on the disaster print map |
| **optuna/optuna** | — | Hyperparameter optimization framework |
| **pandas-dev/pandas** | — | Data analysis library |
| **jldbc/pybaseball** | [#498-504](https://github.com/jldbc/pybaseball) | Bug fixes & documentation |

<details>
<summary>team-mirai — Civic Tech OSS (<!-- TEAM_MIRAI_STATS_START -->25 PRs (14 Merged / 3 Open / 8 Closed)<!-- TEAM_MIRAI_STATS_END -->)</summary>

Civic tech projects for political transparency & citizen participation in Japan. Next.js / TypeScript / Supabase / Vitest.

| Repository | Highlights |
|---|---|
| **action-board** | [48 unit tests](https://github.com/team-mirai-volunteer/action-board/pull/1969), [RPC tests](https://github.com/team-mirai-volunteer/action-board/pull/1869), [breadcrumb nav](https://github.com/team-mirai-volunteer/action-board/pull/1849), [cache fix](https://github.com/team-mirai-volunteer/action-board/pull/1845) + 5 more |
| **marumie** | [Category filter total](https://github.com/team-mirai/marumie/pull/1141) |
| **mirai-gikai** | [Supabase CLI v2.106 seed permission fix](https://github.com/team-mirai/mirai-gikai/pull/930), [Safari/iOS ruby spacing fix](https://github.com/team-mirai/mirai-gikai/pull/932) |
| **post-checker** | [Timezone fix](https://github.com/team-mirai-volunteer/post-checker/pull/34) |
| **fact-checker** | [X API investigation](https://github.com/team-mirai-volunteer/fact-checker/issues/69#issuecomment-3811711591) + 5 PRs |

</details>

</details>

---

## 📊 Data & Competitions

### Kaggle

<!-- KAGGLE_COMP_STATS_START -->Notebooks Expert | 🥉 14 Bronze Notebook Medals<!-- KAGGLE_COMP_STATS_END -->

**Active:**
- [ROGII Wellbore Geology Prediction](https://www.kaggle.com/competitions/rogii-wellbore-geology-prediction) — $50K, wellbore TVT regression (public LB 7.311, rank 1406/5063)
- **SIGNATE AI Engineering Challenge** — NTT Data, LLM / RAG / agentic retrieval over a messy corporate drive (¥1.2M prize pool, Jul–Aug 2026)
- **SIGNATE NEDO Challenge — Baggage-Loading Optimization** — 3D bin packing for airline ULD containers, hybrid offline+online packing agent (¥15M prize pool, Jul–Oct 2026)

**Finished 2026:** [Playground Series S6E6 - Stellar Classification](https://www.kaggle.com/competitions/playground-series-s6e6) (macro-F1, private LB 0.95939) · NIR Moisture Prediction (SIGNATE, wood spectroscopy) · [Stanford RNA 3D Folding 2](https://www.kaggle.com/competitions/stanford-rna-3d-folding-2) · [BirdCLEF+ 2026](https://www.kaggle.com/competitions/birdclef-2026)

<details>
<summary>Bronze Medal Notebooks (14)</summary>

| Notebook | Topic |
|----------|-------|
| [savant-extras Defense & Pitching Quality](https://www.kaggle.com/code/yasunorim/savant-extras-defense-pitching-quality) | Defense metrics & pitching quality (savant-extras) |
| [MLB Statcast Spray Charts for WBC 2026](https://www.kaggle.com/code/yasunorim/mlb-statcast-spray-charts-for-wbc-2026-players) | WBC 2026 spray + pitch zone charts (baseball-field-viz) |
| [March Machine Learning Mania 2026](https://www.kaggle.com/code/yasunorim/march-machine-learning-mania-2026-baseline) | NCAA tournament prediction (LightGBM) |
| [NFL Geometric Rules Baseline](https://www.kaggle.com/code/yasunorim/geometric-rules-baseline-2-921-rmse-no-ml) | Physics-based rules, No ML, RMSE 2.921 |
| [CAFA 6 Baseline](https://www.kaggle.com/code/yasunorim/baseline-with-regularization) | Protein function prediction (PyTorch MLP) |

[All 14 notebooks →](https://www.kaggle.com/yasunorim/code)

</details>

### Kaggle Datasets

<!-- KAGGLE_DS_STATS_START -->28 published MLB datasets<!-- KAGGLE_DS_STATS_END -->

| Dataset | Description |
|---------|-------------|
| 🥈 [MLB Bat Tracking Leaderboard (2024-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-bat-tracking-2024-2025) | 452 batters, 19 swing metrics |
| 🥈 [WBC 2026 Scouting](https://www.kaggle.com/datasets/yasunorim/wbc-2026-scouting) | 306 players, 20 countries |

<details>
<summary>Other datasets (4)</summary>

| Dataset | Description |
|---------|-------------|
| [Baseball Savant Leaderboards (2024-2025)](https://www.kaggle.com/datasets/yasunorim/baseball-savant-leaderboards-2024) | 15 leaderboards, 2 seasons combined |
| [Japanese MLB Players Statcast (2015-2025)](https://www.kaggle.com/datasets/yasunorim/japan-mlb-pitchers-batters-statcast) | 34 Japanese MLB players, 174k pitches+hits |
| [MLB Pitcher Arsenal Evolution (2020-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-pitcher-arsenal-2020-2025) | 4,253 pitcher-seasons, 111 metrics |
| [MLB Statcast + Bat Tracking (2024-2025)](https://www.kaggle.com/datasets/yasunorim/mlb-statcast-bat-tracking-2024-2025) | Combined Statcast + bat tracking data |

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
| **[Daily Diary](https://github.com/yasumorishima/diary-app-flutter)** | Flutter mobile app, 10 languages, offline-first, biometric app lock, daily reminder, Android Auto Backup, AdMob | [Google Play](https://play.google.com/store/apps/details?id=com.diary.daily) |
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
| **[ICP Learning Project](https://github.com/yasumorishima/ICP_kinyoku)** | Persistent counter dApp on Internet Computer (Motoko, dfx CLI) |
| **[OpenClaw Twitter Bot](https://github.com/yasumorishima/raspi-baseball-bot)** | Raspberry Pi 5 + OpenClaw + Gemini API auto-tweet bot (stopped) — [Article (JP)](https://zenn.dev/shogaku/articles/raspi-baseball-bot-openclaw-gemini) |
| **[alexa-rpi5](https://github.com/yasumorishima/alexa-rpi5)** 🔒 | RPi5 ↔ Fire TV Cube 操作 hub (Echo speaker 不要環境)。 cube wrapper + watchers + integrations、 機能詳細は repo README 参照 |

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
* **2024 - Present:** Quality Management @ Marubun Corporation (丸文株式会社)
* **2008 - 2024:** Semiconductor Manufacturing Process Engineer (半導体製造プロセスエンジニア)

---

## 🏆 Patents
**Stencil mask and manufacturing method thereof (ステンシルマスク及びその製造方法)**
* **Patent No:** 6307851 (特許第6307851号)
* **Role:** Inventor (発明者)
* **Assignee:** Toppan Printing Co., Ltd. (凸版印刷株式会社)
* **Link:** [Google Patents (JP6307851B2)](https://patents.google.com/patent/JP6307851B2/ja)

---

## 📫 Contact & Blog
* **Site:** [https://yasumorishima.github.io](https://yasumorishima.github.io) — tools and blog hosted on this domain
* **Blog:** [DEV.to (EN)](https://dev.to/yasumorishima) / [Zenn (JP)](https://zenn.dev/shogaku) / [Quarto Blog (EN)](https://yasumorishima.github.io/quarto-blog/)
* **Kaggle:** [https://www.kaggle.com/yasunorim](https://www.kaggle.com/yasunorim)
* **Wantedly:** [https://www.wantedly.com/id/yasunori_morishima_b](https://www.wantedly.com/id/yasunori_morishima_b)
* **LinkedIn:** [https://www.linkedin.com/in/morishima-yasunori-b70229241](https://www.linkedin.com/in/morishima-yasunori-b70229241?trk=contact-info)
