# Yasunori Morishima (盛島康徳)
Manufacturing Engineer & Data Analyst with 17 years of experience, specializing in data analysis and business automation.
(製造業にて17年の経験を持つエンジニア。データ分析と業務自動化を専門としています)

## 🎯 Focus Areas
* **Data Analysis & Machine Learning:** Python, scikit-learn
* **Business Process Automation:** VBA, Google Apps Script (GAS)
* **Statistical Quality Control:** Manufacturing Process Improvement (統計的品質管理・工程改善)

---

## 📊 Main Projects

### [Business Automation Workflow](https://github.com/yasumorishima/business-automation-workflow)
End-to-end automation system for processing email PDF attachments and integrating multiple data sources.
(メール添付PDFの処理から複数ソースのデータ統合までを行うエンドツーエンドの自動化システム)

**System Architecture:**
- **Step 1:** Gmail PDF extraction (Google Apps Script)
- **Step 2:** PDF to Excel conversion (VBA + Power Query)
- **Step 3:** Data aggregation to Google Sheets (Google Apps Script)
- **Step 4:** Multi-source data integration (Python/Google Colab)

**Key Features:**
- Automated email processing with duplicate detection (重複検知付きのメール自動処理)
- Text-embedded PDF extraction (Power Query solves GAS OCR accuracy issues)
  - (GASのOCR精度の課題をPower Queryで解決)
- Cross-platform data integration with styled Excel output

**Technical Stack:** Google Apps Script, VBA, Power Query, Python, pandas, gspread, xlsxwriter

**Applied to Work:** Developed for streamlining order processing and repair request management workflows.
(実績: 受注処理および修理依頼管理ワークフローの効率化のために開発・導入)

---

### [GAS Calendar Event Registration Tool](https://github.com/yasumorishima/gas-calendar-tool)
Google Apps Script-based web application for batch calendar event registration with mobile-optimized UI.
(Google Apps ScriptベースのWebアプリ。モバイルに最適化されたUIでカレンダー一括登録を実現)

**Key Features:**
- Batch event creation for multiple dates (複数日程の一括登録)
- Event template management with user properties
- Mobile-first responsive design (28px font, 80px+ touch targets for senior-friendly UI)
- Support for all-day and timed events with color coding

**Technical Stack:** Google Apps Script, HTML5, CSS3, JavaScript, Google Calendar API

**Use Case:** Simplifies recurring event scheduling (shifts, medication reminders, meetings) with a senior-friendly interface.
(用途: シニア層にも使いやすいインターフェースで、シフト管理や服薬リマインダーなどの定期予定作成を簡略化)

---

### [Daily Diary Web App](https://github.com/yasumorishima/gas-daily-diary)
Google Apps Script-based personal diary web application with mobile-optimized UI.
(Google Apps ScriptベースのWebアプリ。モバイル最適化された個人用日記アプリ)

**Key Features:**
- Mobile-first responsive design with dark mode support (モバイルファースト設計とダークモード対応)
- 10 functional pages: Write, Calendar, Search, Statistics, Export, and more
- Privacy-focused data storage in user's own Google Spreadsheet
- Full-text search, tag filtering, and past entries viewing

**Technical Stack:** Google Apps Script, HTML5, CSS3, Vanilla JavaScript

**Use Case:** Personal diary management with comprehensive features for daily writing, reflection, and data export.
(用途: 日常の記録、振り返り、データエクスポートなど、包括的な機能を備えた個人用日記管理)

---

### [Daily Diary - Flutter Mobile App](https://github.com/yasumorishima/diary-app-flutter)
Cross-platform mobile diary app built with Flutter, evolved from the GAS web app above.
(Flutter製クロスプラットフォームモバイル日記アプリ - 上記GAS版からの進化版)

**Key Features:**
- 5 language support (🇯🇵🇺🇸🇨🇳🇰🇷🇪🇸)
- Offline-first with local storage (Hive)
- Dark mode, calendar view, statistics, search
- Google Play release (Coming Soon)

**Technical Stack:** Flutter, Dart, Hive, Provider, Google AdMob

**Development:** Built with Claude Code (AI-assisted development)
(開発手法: Claude Codeを活用したAI支援開発)

**Status:** Google Play - Coming Soon (Currently in Closed Testing)

---

### [Selenium Automation Guide](https://github.com/yasumorishima/selenium-automation-guide)
Practical troubleshooting guide for Selenium browser automation, born from real-world problem solving.
(実務から生まれたSeleniumブラウザ自動化のトラブルシューティングガイド)

**Key Guides:**
| Problem | Solution Approach |
|---------|-------------------|
| **ChromeDriver Version Mismatch** | Dynamic version detection + multi-step fallback (動的バージョン検出+多段階フォールバック) |
| **DevToolsActivePort Error** | New profile management for latest Chrome/Edge (最新Chrome/Edge対応のプロファイル管理) |
| **Brave Browser Migration** | Privacy-focused alternative with stable profiles (プライバシー重視の代替ブラウザ活用) |

**Design Philosophy:**
- No hardcoded version numbers → **Maintenance-free** (バージョン番号ハードコードなし → メンテナンスフリー)
- Relative retry strategy → **Future-proof** (相対的リトライ戦略 → 将来対応)
- Multi-browser support → **Environment-independent** (複数ブラウザ対応 → 環境非依存)

**Technical Stack:** Python, Selenium, webdriver-manager, Chrome/Edge/Brave

---

### [MLB Data Analysis](https://github.com/yasumorishima/mlb-data-analysis)
MLB Statcast data analysis with Python & SQL. (Python & SQLによるMLB Statcastデータ分析)

| Analysis | Key Finding |
|----------|-------------|
| **WBC 2023 Sandoval Scouting** | 49.2% sliders vs left-handed batters, 0 HR allowed (左打者にスライダー49.2%、被HR 0本) |
| **Bauer Set Position (Image)** | K-means detected glove position "tells" (グラブ位置に球種の癖を検出) |
| **Ohtani Batting 2022** | Hit concentration at 2B area → "Ohtani Shift" (セカンド付近集中→大谷シフトの根拠) |
| **Ohtani Injury 2023** | Multi-parameter anomaly detection (±2σ) (複数パラメーター組合せで予兆検出) |
| **HR Race 2024** | Bar chart race animation (動的バーチャートレース) |

**Technical Stack:** Python, pybaseball, pandas, matplotlib, PIL, scikit-learn, **DuckDB (SQL)**

📌 **SQL versions available** - Each analysis has both Python (pandas) and SQL (DuckDB) implementations
(各分析にPython版とSQL版の両方を用意)

---

### [Kaggle Competitions](https://github.com/yasumorishima/kaggle-competitions)
🥉 **4 Bronze Medals (Notebook)** - Earned through AI-assisted development with Claude Code
(4つのブロンズメダル（ノートブック） - Claude Codeを活用したAI支援開発で獲得)

**Note:** These are Notebook Medals (community votes), not competition ranking medals.
(注: コミュニティ投票によるノートブックメダルであり、コンペティション順位のメダルではありません)

| Competition | Notebook | Key Approach |
|-------------|----------|--------------|
| **NFL Big Data Bowl 2026** | [Geometric Rules Baseline](https://www.kaggle.com/code/yasunorim/geometric-rules-baseline-2-921-rmse-no-ml) | Physics-based rules, No ML, RMSE 2.921 |
| **PhysioNet ECG** | [ECG Baseline](https://www.kaggle.com/code/yasunorim/physionet-ecg-baseline) | Submission format guide |
| **Diabetes (S5E12)** | [EDA & Baseline](https://www.kaggle.com/code/yasunorim/diabetes-prediction-eda-baseline-s5e12) | LightGBM 5-fold CV, AUC 0.727 |
| **Diabetes (S5E12)** | [Rank-Based Ensemble](https://www.kaggle.com/code/yasunorim/diabetes-prediction-rank-based-ensemble) | Rank averaging for AUC optimization |

**Technical Stack:** Python, pandas, LightGBM, scikit-learn, Claude Code

**Key Learning:** Domain knowledge + AI tools = effective problem solving
(重要な学び: ドメイン知識 + AIツール = 効果的な問題解決)

---

### [Dune Analytics - Blockchain Data Analysis](https://github.com/yasumorishima/dune-analytics)
On-chain data analysis using SQL on Dune Analytics. (Dune AnalyticsでSQLを使ったオンチェーンデータ分析)

| Analysis | Key Metrics |
|----------|-------------|
| **[JPYC Stablecoin](https://dune.com/shogaku_toushi/jpyc-date)** | ~400K txns, ~10B JPY volume, ~100K users across 3 chains |

**Technical Highlights:**
- Multi-chain analysis (Ethereum, Polygon, Avalanche)
- 9 CTEs with window functions (`SUM OVER`, `FIRST_VALUE`)
- Cross-chain user deduplication logic

**Technical Stack:** SQL (DuneSQL/Trino), Dune Analytics

*Powered by [Dune Analytics](https://dune.com)*

---

## 🔬 Learning Projects

### [ICP Learning Project](https://github.com/yasumorishima/ICP_kinyoku)
Built a persistent counter dApp on Internet Computer (ICP).
(ICP上で継続カウンターdAppを構築)

| Challenge | Solution |
|-----------|----------|
| **dfx 0.25.1 Type Errors** | Downgrade to dfx 0.20.1 (安定版にダウングレード) |
| **Cycles Wallet Setup** | 0.5T+ Cycles, Identity & NNS Dapp integration |

**Technical Stack:** Motoko, Vanilla JavaScript, dfx CLI, Webpack

---

## 🛠️ Tech Stack
| Category | Technologies |
| --- | --- |
| **Data Analysis & ML** | Python, pandas, scikit-learn, matplotlib, seaborn, **DuckDB (SQL)**, **Dune Analytics** |
| **Automation** | VBA, Google Apps Script, Power Query, Selenium |
| **Mobile App** | Flutter, Dart, Hive, Google AdMob |
| **Tools** | Excel, Access, Looker Studio, Salesforce |
| **Manufacturing** | Statistical Quality Control, Process Engineering |

---

## 📈 Career
* **2024 - Present:** Quality Management @ Marubun Corporation (丸文株式会社)
* **2020 - 2024:** Technical Dept. @ Metaco Corporation (株式会社メタコ)
* **2008 - 2020:** Process Engineering in Semiconductor Manufacturing (半導体製造プロセスエンジニア)

---

## 🏆 Patents
**Stencil mask and manufacturing method thereof (ステンシルマスク及びその製造方法)**
* **Patent No:** 6307851 (特許第6307851号)
* **Role:** Inventor (発明者)
* **Assignee:** Toppan Printing Co., Ltd. (凸版印刷株式会社)
* **Link:** [Google Patents (JP6307851B2)](https://patents.google.com/patent/JP6307851B2/ja)

---

## 📫 Contact
* **Kaggle:** [https://www.kaggle.com/yasunorim](https://www.kaggle.com/yasunorim)
* **Wantedly:** [https://www.wantedly.com/id/yasunori_morishima_b](https://www.wantedly.com/id/yasunori_morishima_b)
* **LinkedIn:** [https://www.linkedin.com/in/yasunori-morishima-b70229241](https://www.linkedin.com/in/yasunori-morishima-b70229241)

> 💡 *"Bridging manufacturing expertise with data-driven solutions"*
