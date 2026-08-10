from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import config


class SlackPosterInput(BaseModel):
    headline: str = Field(..., description="The news headline.")
    summary: str = Field(..., description="The short summary of the article.")
    source_url: str = Field(..., description="The original article link.")


class SlackBotTool(BaseTool):
    name: str = "Slack News Poster"
    description: str = (
        "Posts a formatted news update to the team's Slack channel. "
        "Takes a headline, summary, and source link, and sends them as a single readable message. "
        "Use this after a news item has been summarized and is ready for distribution."
    )
    args_schema: Type[BaseModel] = SlackPosterInput

    def _run(self, headline: str, summary: str, source_url: str) -> str:
        client = WebClient(token=config.SLACK_BOT_TOKEN)

        message = f"*{headline}*\n" f"{summary}\n" f"<{source_url}|Read full article>"

        try:
            client.chat_postMessage(
                channel=config.SLACK_CHANNEL_ID,
                text=message,
                unfurl_links=False,
            )
            return f"Posted to Slack: {headline}"
        except SlackApiError as e:
            return f"Failed to post to Slack: {e.response['error']}"
