<div align="center">

# 📰 Signal Desk
### An unattended newsroom, run by agents, read by you.

*A multi-agent AI pipeline that researches, summarizes, and publishes AI news — automatically, on a schedule, with zero human intervention.*

[![Built with CrewAI](https://img.shields.io/badge/Built%20with-CrewAI-6C5CE7?style=flat-square)](https://www.crewai.com/)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel)](https://vercel.com)
[![Automated by GitHub Actions](https://img.shields.io/badge/Automated%20by-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)

[Live Dashboard](https://crewai-news-automation-bot.vercel.app/) 

</div>

---

## 🎥 Demo

📹 **[Watch the demo](assets/demo.mp4)**

*(GitHub doesn't autoplay local `.mp4` files inline in a README — click the link above to view, or drop the same file into a GitHub Release / Issue comment to get an embeddable player.)*

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [Using the Dashboard](#-using-the-dashboard)
- [API Reference](#-api-reference)
- [Contributing](#-contributing)

---

## 🧠 Overview

**Signal Desk** is a self-operating AI newsroom. A crew of three specialized AI agents — a **Researcher**, a **Summarizer**, and a **Publisher** — work together every few hours to:

1. Scan the web for fresh AI/tech news
2. Filter out duplicates and noise
3. Condense each story into a tight, factual 2–3 sentence brief
4. Publish the results to **Slack** and archive them in **Google Sheets**
5. Surface everything on a **live, auto-refreshing dashboard**

No human touches the pipeline once it's deployed. It just runs — quietly, on schedule, in the background.

---

## ✨ Features

| | |
|---|---|
| 🤖 **Multi-agent pipeline** | CrewAI-powered Researcher → Summarizer → Publisher workflow |
| ⏰ **Scheduled automation** | Runs on a cron schedule via GitHub Actions — no server to maintain |
| 💬 **Slack publishing** | Every dispatch is posted straight to your team's channel |
| 📊 **Google Sheets archive** | Permanent, queryable record of every story ever published |
| 🌐 **Live dashboard** | A styled, real-time web UI reading directly from the Sheet |
| 🔁 **Duplicate-safe reads** | The dashboard de-duplicates stories by source URL before rendering |
| ⚡ **Manual override** | Trigger an off-schedule run with one click from the dashboard |
| 🟡 **Live status & highlights** | Watch the pipeline run in real time — new stories glow as they land |

---

## 🏗 Architecture

```
┌─────────────────┐      cron / manual trigger      ┌──────────────────────┐
│  GitHub Actions   │ ───────────────────────────▶  │   CrewAI Pipeline    │
│  (news-bot.yml)   │                                │  Researcher          │
└─────────────────┘                                  │  → Summarizer        │
        ▲                                             │  → Publisher         │
        │ workflow_dispatch                           └──────────┬───────────┘
        │                                                          │
┌───────┴────────┐                                         ┌──────┴───────┐
│  api/trigger    │◀──── button click ────┐                │  Slack        │
│  (Vercel func)  │                        │                │  Channel      │
└─────────────────┘                        │                └───────────────┘
                                            │                        │
┌─────────────────┐   reads sheet   ┌──────┴────────┐      writes row│
│  index.html      │◀───────────────│  api/index.py │◀────────────────┘
│  (Dashboard)      │   JSON feed    │  (Vercel func) │
└─────────────────┘                 └───────┬────────┘
                                              │
                                     ┌────────┴────────┐
                                     │  Google Sheets   │
                                     │  (data store)    │
                                     └──────────────────┘
```

**Two independent surfaces, one source of truth:** Slack gets a live feed as stories are published; the dashboard and Google Sheet stay in sync as the permanent archive.

---

## 🛠 Tech Stack

- **Agents & Orchestration:** [CrewAI](https://www.crewai.com/)
- **LLM:** Google Gemini (`gemini/gemini-3.1-flash-lite` by default)
- **Web Search:** [Serper.dev](https://serper.dev/)
- **Backend / API:** Python, Flask (Vercel Serverless Functions)
- **Data store:** Google Sheets (via `gspread`)
- **Notifications:** Slack Bot API
- **Automation:** GitHub Actions (scheduled cron + manual `workflow_dispatch`)
- **Frontend:** Vanilla HTML/CSS/JS (no framework, no build step)
- **Hosting:** Vercel

---

## 📁 Project Structure

```
ai-news-bot/
│
├── agents.py                 # Agent definitions (Researcher, Summarizer, Publisher)
├── tasks.py                   # Task definitions for the crew
├── crew.py                    # Crew assembly + run function
├── main.py                    # Local entry point for testing the pipeline
├── config.py                  # Env loading + shared constants
├── patches.py                 # Runtime/library compatibility patches applied before the crew runs
│
├── tools/
│   ├── __init__.py
│   ├── news_fetcher_tool.py   # Fetches raw news for the Researcher (via Serper)
│   ├── summarizer_tool.py     # Condenses articles for the Summarizer
│   ├── slack_tool.py          # Posts dispatches to Slack
│   └── sheets_tool.py         # Logs dispatches to Google Sheets
│
├── api/
│   ├── index.py                # Vercel serverless function — dashboard API + trigger
│   └── index.html              # Live dashboard (served as a static asset)
│
├── assets/
│   └── demo.mp4                # Demo video
│
├── .github/
│   └── workflows/
│       └── news-bot.yml        # Scheduled + manually-triggerable pipeline run
│
├── credentials.json             # Google service account key (gitignored, local only)
├── .env                          # Local environment variables (gitignored)
├── .env.example                  # Template for required env vars, safe to commit
├── .python-version                # Pinned Python version for local/CI consistency
├── .gitignore
├── .vercelignore                  # Files excluded from the Vercel deployment bundle
├── requirements.txt
├── pyproject.toml
├── vercel.json                    # Deployment + routing config
└── README.md
```

---

## ⚙️ How It Works

1. **Trigger** — Either GitHub Actions fires on its cron schedule, or someone clicks **"Trigger Pipeline"** on the dashboard, which calls `/api/trigger` and manually dispatches the workflow.
2. **Research** — The Researcher agent searches Serper for recent news across the topics defined in `NEWS_TOPICS`.
3. **Summarize** — The Summarizer agent (Gemini) rewrites each article into a short, factual, no-speculation brief.
4. **Publish** — The Publisher agent posts the headline + summary + link to Slack, and logs the same data as a new row in Google Sheets.
5. **Serve** — `api/index.py` reads the sheet on every request, de-duplicates by source URL, sorts by real timestamp (newest first), and returns clean JSON.
6. **Display** — `index.html` polls the API, renders the feed, and — after a manual trigger — actively watches for new dispatches and highlights them as they arrive.

---

## 🚀 Getting Started

### Prerequisites

- Python version pinned in `.python-version`
- A Google Cloud service account with **Sheets API** + **Drive API** enabled
- A Slack app with a bot token, invited into your target channel
- A [Serper.dev](https://serper.dev/) API key for news search
- A Google Gemini API key
- A GitHub repo with Actions enabled
- A Vercel account (for the dashboard)

### Local Setup

```bash
# Clone the repo
git clone https://github.com/s-zaid-13/crewai-news-automation-bot.git
cd ai-news-bot

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env            # then fill in your values

# Run the pipeline once, locally
python main.py
```

---

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in your own values:

```dotenv
SLACK_BOT_TOKEN=
SLACK_CHANNEL_ID=
SERPER_API_KEY=
GOOGLE_SHEETS_CREDENTIALS_PATH=
GOOGLE_SHEET_ID=
NEWS_TOPICS=AI,technology
GEMINI_API_KEY=
GEMINI_MODEL=gemini/gemini-3.1-flash-lite
GOOGLE_CREDENTIALS_BASE64=

```

| Variable | Used By | Description |
|---|---|---|
| `SLACK_BOT_TOKEN` | `slack_tool.py` | Bot token used to post dispatches to Slack |
| `SLACK_CHANNEL_ID` | `slack_tool.py` | Channel the bot posts into |
| `SERPER_API_KEY` | `news_fetcher_tool.py` | API key for Serper.dev web search |
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | `sheets_tool.py` | Local path to the service account JSON (used when running the pipeline locally / in Actions) |
| `GOOGLE_CREDENTIALS_BASE64` | `api/index.py` | Base64-encoded service account JSON, used by the Vercel function (env vars can't hold multi-line files cleanly) |
| `GOOGLE_SHEET_ID` | `sheets_tool.py`, `api/index.py` | ID of the Google Sheet used as the data store |
| `NEWS_TOPICS` | `news_fetcher_tool.py` | Comma-separated list of topics the Researcher searches for |
| `GEMINI_API_KEY` | `agents.py` | API key for the Gemini LLM powering the crew |
| `GEMINI_MODEL` | `agents.py` | Gemini model identifier used by the agents |
| `GITHUB_OWNER` | `api/index.py` (trigger route) | GitHub username/org that owns the repo |
| `GITHUB_REPO` | `api/index.py` (trigger route) | Repository name |
| `GITHUB_TOKEN` | `api/index.py` (trigger route) | PAT with `workflow` scope, used to dispatch the Action |


---

## ☁️ Deployment

**Dashboard (Vercel):**
1. Import the repo into Vercel.
2. Add the relevant environment variables (`GOOGLE_CREDENTIALS_BASE64`, `GOOGLE_SHEET_ID`, `GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_TOKEN`) under **Project Settings → Environment Variables**.
3. `.vercelignore` keeps the agent/pipeline source (`agents.py`, `tasks.py`, `crew.py`, `main.py`, `tools/`, `credentials.json`, etc.) out of the deployed bundle — only `api/` and `index.html` are needed there.
4. Vercel builds `index.html` as a static asset and `api/index.py` as a serverless function.

**Automation (GitHub Actions):**
1. Add the pipeline secrets (`SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`, `SERPER_API_KEY`, `GOOGLE_SHEETS_CREDENTIALS_PATH`/credentials, `GOOGLE_SHEET_ID`, `GEMINI_API_KEY`, `GEMINI_MODEL`) under **Repo Settings → Secrets and variables → Actions**.
2. `.github/workflows/news-bot.yml` runs on a cron schedule and can also be triggered manually via `workflow_dispatch` — which is exactly what the dashboard's **Trigger Pipeline** button calls through `/api/trigger`.

---

## 🖱 Using the Dashboard

- **Browse dispatches** — newest first, de-duplicated, auto-refreshing every 5 minutes.
- **Trigger Pipeline** — runs the crew on demand. The button shows live status (`Dispatching…` → `Running…` → `New dispatch added ✓`), and any newly published story is highlighted with a gold glow as it lands.

---

## 🔌 API Reference

### `GET /api/news`
Returns the de-duplicated, sorted news feed.

```json
{
  "count": 15,
  "last_updated": "2026-08-10 20:22",
  "items": [
    {
      "Datetime": "2026-08-10 20:22",
      "Headline": "Example Headline",
      "Summary": "Example summary text.",
      "Source URL": "https://example.com/article"
    }
  ]
}
```

### `POST /api/trigger`
Dispatches the GitHub Actions workflow on demand.

```json
{ "status": "triggered" }
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes
4. Open a pull request

---

<div align="center">

**Signal Desk** · CrewAI multi-agent pipeline · GitHub Actions cron · Vercel dashboard

</div>