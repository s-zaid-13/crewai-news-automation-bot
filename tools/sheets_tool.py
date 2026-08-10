from datetime import datetime, timezone, timedelta
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import gspread
from google.oauth2.service_account import Credentials

from config import config

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
PKT = timezone(timedelta(hours=5))


class SheetsLoggerInput(BaseModel):
    headline: str = Field(..., description="The news headline.")
    summary: str = Field(..., description="The short summary of the article.")
    source_url: str = Field(..., description="The original article link.")


class SheetsLoggerTool(BaseTool):
    name: str = "Google Sheets Logger"
    description: str = (
        "Logs a news update into a Google Sheet for record-keeping. "
        "Stores the date, headline, summary, and source link as a new row. "
        "Use this after a news item has been summarized, so it stays archived even after Slack messages scroll away."
    )
    args_schema: Type[BaseModel] = SheetsLoggerInput

    def _run(self, headline: str, summary: str, source_url: str) -> str:
        credentials = Credentials.from_service_account_file(
            config.GOOGLE_SHEETS_CREDENTIALS_PATH, scopes=SCOPES
        )
        client = gspread.authorize(credentials)

        sheet = client.open_by_key(config.GOOGLE_SHEET_ID).sheet1

        row = [
            datetime.now(PKT).strftime("%Y-%m-%d %H:%M"),
            headline,
            summary,
            source_url,
        ]
        sheet.append_row(row)

        return f"Logged to Google Sheets: {headline}"
