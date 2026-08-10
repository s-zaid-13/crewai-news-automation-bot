import requests
from typing import Type, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from config import config


class NewsFetcherInput(BaseModel):
    topic: str = Field(
        ...,
        description="The topic or keyword to search news for, e.g. 'AI' or 'crypto'.",
    )
    max_results: int = Field(
        default=5, description="Maximum number of news articles to return."
    )


class NewsFetcherTool(BaseTool):
    name: str = "News Fetcher"
    description: str = (
        "Searches the web for the latest news articles on a given topic. "
        "Returns each article's headline, source URL, and a short snippet. "
        "Use this when you need current, real-world news rather than general knowledge."
    )
    args_schema: Type[BaseModel] = NewsFetcherInput

    def _run(self, topic: str, max_results: int = 5) -> str:
        url = "https://google.serper.dev/news"
        headers = {
            "X-API-KEY": config.SERPER_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {"q": topic}

        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()

        results = response.json().get("news", [])[:max_results]

        if not results:
            return f"No news articles found for topic: {topic}"

        formatted = []
        for i, article in enumerate(results, start=1):
            headline = article.get("title", "No title")
            link = article.get("link", "No link")
            snippet = article.get("snippet", "")[:200]
            source = article.get("source", "Unknown source")

            formatted.append(
                f"{i}. {headline}\n"
                f"   Source: {source}\n"
                f"   Link: {link}\n"
                f"   Snippet: {snippet}"
            )

        return "\n\n".join(formatted)
