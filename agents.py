from crewai import Agent, LLM

from config import config
from tools.news_fetcher_tool import NewsFetcherTool
from tools.summarizer_tool import SummarizerTool
from tools.slack_tool import SlackBotTool
from tools.sheets_tool import SheetsLoggerTool

llm = LLM(
    model=config.GEMINI_MODEL,
    api_key=config.GEMINI_API_KEY,
    temperature=0.4,
    max_retries=5,
    timeout=120,
)

news_fetcher_tool = NewsFetcherTool()
summarizer_tool = SummarizerTool()
slack_tool = SlackBotTool()
sheets_tool = SheetsLoggerTool()


researcher_agent = Agent(
    role="News Researcher",
    goal="Find the latest, most relevant news articles on the given topics and hand over clean, structured findings.",
    backstory=(
        "You've spent years working the news desk, and you have a nose for what's actually worth "
        "reporting versus what's noise. You don't just dump search results — you filter out duplicates "
        "and low-quality sources before passing anything along."
    ),
    tools=[news_fetcher_tool],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

summarizer_agent = Agent(
    role="Content Summarizer",
    goal="Turn raw news articles into short, clear summaries that someone can read in under 10 seconds.",
    backstory=(
        "You're a former wire-service editor who got very good at saying more with less. "
        "You strip out fluff, avoid repeating the headline in the summary, and never add your own "
        "opinion to a news item — just the facts, tightened up."
    ),
    tools=[summarizer_tool],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

publisher_agent = Agent(
    role="News Publisher",
    goal="Distribute summarized news to the team's Slack channel and keep a permanent log in Google Sheets.",
    backstory=(
        "You're the one responsible for making sure news actually reaches people, and reaches them in a "
        "format they'll read. You also know that Slack messages scroll away fast, so nothing goes out "
        "without also being archived properly."
    ),
    tools=[slack_tool, sheets_tool],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)
