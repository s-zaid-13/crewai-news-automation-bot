from crewai import Task

from agents import researcher_agent, summarizer_agent, publisher_agent


def build_tasks(topics: list[str]):
    topic_list = ", ".join(topics)

    fetch_task = Task(
        description=(
            f"Search for the latest news on the following topics: {topic_list}. "
            "Pull the top 2 articles per topic only — do not exceed this. "
            "Discard anything that looks like a duplicate or an unrelated result."
        ),
        expected_output=(
            "A list of news articles, each with a headline, source URL, and a short snippet, "
            "grouped by topic."
        ),
        agent=researcher_agent,
    )

    summarize_task = Task(
        description=(
            "Take all fetched articles and pass them together, in a single call, to the News Summarizer tool. "
            "Do not call the tool separately for each article. "
            "Each summary should be 2-3 sentences, factual, with no speculation or opinion."
        ),
        expected_output=(
            "A list of news items, each containing: headline, summary, and source URL, "
            "ready for distribution."
        ),
        agent=summarizer_agent,
        context=[fetch_task],
    )

    publish_task = Task(
        description=(
            "For each summarized news item, post it to the Slack channel and log it into "
            "Google Sheets. Every item must be both posted and logged — do not skip one or the other."
        ),
        expected_output=(
            "A confirmation for each news item indicating it was successfully posted to Slack "
            "and logged to Google Sheets."
        ),
        agent=publisher_agent,
        context=[summarize_task],
    )

    return [fetch_task, summarize_task, publish_task]
