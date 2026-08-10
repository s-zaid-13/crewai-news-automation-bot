import json
import os
import re
from datetime import datetime

from flask import Flask, jsonify
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str):
    """Returns a sortable datetime; unparseable/missing values sort last."""
    if not value:
        return datetime.min
    try:
        return datetime.strptime(value.strip(), DATETIME_FORMAT)
    except ValueError:
        return datetime.min


def normalize_key(row: dict) -> str:
    """Key used for de-duplication — prefers Source URL, falls back to headline."""
    url = (row.get("Source URL") or "").strip().lower()
    if url:
        url = re.sub(r"[?#].*$", "", url).rstrip("/")
        return url
    return (row.get("Headline") or "").strip().lower()


def get_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def fetch_news():
    credentials_info = json.loads(get_env("GOOGLE_CREDENTIALS_JSON"))
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(get_env("GOOGLE_SHEET_ID")).sheet1
    raw_rows = sheet.get_all_records()

    # Sort newest first using a real datetime parse (not plain string sort)
    raw_rows.sort(key=lambda r: parse_datetime(r.get("Datetime", "")), reverse=True)

    # De-duplicate, keeping the newest occurrence of each article
    seen = set()
    deduped = []
    for row in raw_rows:
        key = normalize_key(row)
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(row)

    items = deduped[:50]

    return {
        "count": len(deduped),
        "last_updated": deduped[0].get("Datetime") if deduped else None,
        "items": items,
    }


@app.route("/api/news", methods=["GET"])
def news():
    try:
        data = fetch_news()
        resp = jsonify(data)
    except Exception as e:
        resp = jsonify({"error": str(e)})
        return resp, 500
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate"
    return resp


@app.route("/api/trigger", methods=["POST"])
def trigger():
    import urllib.request
    import urllib.error

    try:
        owner = get_env("GITHUB_OWNER")
        repo = get_env("GITHUB_REPO")
        token = get_env("GITHUB_TOKEN")
    except RuntimeError as e:
        resp = jsonify({"error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 500

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/news-bot.yml/dispatches"
    payload = json.dumps({"ref": "main"}).encode()

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")

    try:
        urllib.request.urlopen(req, timeout=10)
        resp = jsonify({"status": "triggered"})
    except urllib.error.HTTPError as e:
        resp = jsonify({"error": f"GitHub API error: {e.code}"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 502
    except Exception as e:
        resp = jsonify({"error": str(e)})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 502

    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
