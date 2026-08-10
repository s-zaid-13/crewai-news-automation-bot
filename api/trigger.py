from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

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
            self.wfile.write(json.dumps({"status": "triggered"}).encode())
        except urllib.error.HTTPError as e:
            self.wfile.write(
                json.dumps({"error": f"GitHub API error: {e.code}"}).encode()
            )
