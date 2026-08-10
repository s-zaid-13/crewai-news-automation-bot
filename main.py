import sys

import patches  # noqa: F401 — must be imported before crew/agents build any LLM messages

from config import config
from crew import run_news_pipeline


def main():
    try:
        config.validate()
    except EnvironmentError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print("Starting AI News Automation Bot...")
    result = run_news_pipeline()

    print("\nPipeline finished.")
    print(result)


if __name__ == "__main__":
    main()
