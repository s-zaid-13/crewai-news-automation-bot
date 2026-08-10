from crewai import Crew, Process

from agents import researcher_agent, summarizer_agent, publisher_agent
from tasks import build_tasks
from config import config


def build_crew(topics: list[str] = None):
    topics = topics or config.NEWS_TOPICS
    tasks = build_tasks(topics)

    return Crew(
        agents=[researcher_agent, summarizer_agent, publisher_agent],
        tasks=tasks,
        process=Process.sequential,
        memory=False,
        verbose=True,
    )


def run_news_pipeline(topics: list[str] = None):
    crew = build_crew(topics)
    result = crew.kickoff()
    return result
