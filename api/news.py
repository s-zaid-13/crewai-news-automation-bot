from http.server import BaseHTTPRequestHandler
import json
import os

import gspread
from google.oauth2.service_account import Credentials

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
        "last_updated": rows[0]["Date"] if rows else None,
        "items": rows[:50],
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "s-maxage=300, stale-while-revalidate")
        self.end_headers()

        try:
            data = fetch_news()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.wfile.write(json.dumps({"error": str(e)}).encode())
