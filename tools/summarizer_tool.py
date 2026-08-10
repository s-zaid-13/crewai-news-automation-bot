import time
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from google import genai
from google.genai import errors

from config import config

client = genai.Client(api_key=config.GEMINI_API_KEY)


class SummarizerInput(BaseModel):
    articles: list[str] = Field(
        ...,
        description="A list of raw article texts (headline + snippet) to summarize together.",
    )


class SummarizerTool(BaseTool):
    name: str = "News Summarizer"
    description: str = (
        "Summarizes a batch of news articles in a single call. "
        "Takes a list of raw article texts and returns one short summary per article, "
        "in the same order. Use this once per topic, passing all fetched articles together — "
        "do not call this separately for each individual article."
    )
    args_schema: Type[BaseModel] = SummarizerInput

    def _run(self, articles: list[str]) -> str:
        trimmed_articles = [text[:800] for text in articles]
        numbered_input = "\n\n".join(
            f"Article {i+1}:\n{text}" for i, text in enumerate(trimmed_articles)
        )

        prompt = (
            "Summarize each of the following news articles in 2-3 sentences. "
            "Be factual, avoid repetition, and do not add opinions or speculation. "
            "Return your answer as a numbered list, one summary per article, in the same order.\n\n"
            f"{numbered_input}"
        )

        max_attempts = 3
        wait_seconds = 10

        for attempt in range(1, max_attempts + 1):
            try:
                response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=prompt,
                    config={"temperature": 0.3, "max_output_tokens": 600},
                )
                return response.text.strip()

            except errors.ClientError as e:
                if getattr(e, "code", None) == 429:
                    if attempt == max_attempts:
                        return "Summaries unavailable: rate limit reached, please retry later."
                    time.sleep(wait_seconds)
                    wait_seconds *= 2
                else:
                    raise

        return "Summaries unavailable."
