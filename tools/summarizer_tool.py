import time
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

from config import config

genai.configure(api_key=config.GEMINI_API_KEY)


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
        model = genai.GenerativeModel("gemini-3.1-flash-lite")

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
                response = model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.3, "max_output_tokens": 600},
                )
                return response.text.strip()

            except ResourceExhausted:
                if attempt == max_attempts:
                    return (
                        "Summaries unavailable: rate limit reached, please retry later."
                    )
                time.sleep(wait_seconds)
                wait_seconds *= 2

        return "Summaries unavailable."
