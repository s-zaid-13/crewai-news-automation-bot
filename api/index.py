import json
import os
import urllib.request
import urllib.error

from flask import Flask, jsonify, request
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def fetch_news():
    credentials_info = json.loads(os.environ["GOOGLE_CREDENTIALS_JSON"])
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
    client = gspread.authorize(credentials)

    sheet = client.open_by_key(os.environ["GOOGLE_SHEET_ID"]).sheet1
    rows = sheet.get_all_records()
    rows.sort(key=lambda r: r.get("Date", ""), reverse=True)

    return {
        "count": len(rows),
        "last_updated": rows[0].get("Datetime") if rows else None,
        "items": rows[:50],
    }


@app.route("/api/news", methods=["GET"])
def news():
    try:
        data = fetch_news()
        resp = jsonify(data)
    except Exception as e:
        resp = jsonify({"error": str(e)})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Cache-Control"] = "s-maxage=300, stale-while-revalidate"
    return resp


@app.route("/api/trigger", methods=["POST"])
def trigger():
    owner = os.environ["GITHUB_OWNER"]
    repo = os.environ["GITHUB_REPO"]
    token = os.environ["GITHUB_TOKEN"]

    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/news-bot.yml/dispatches"
    payload = json.dumps({"ref": "main"}).encode()

    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")

    try:
        urllib.request.urlopen(req)
        resp = jsonify({"status": "triggered"})
    except urllib.error.HTTPError as e:
        resp = jsonify({"error": f"GitHub API error: {e.code}"})

    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
