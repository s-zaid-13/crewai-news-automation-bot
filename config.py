import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

    SERPER_API_KEY = os.getenv("SERPER_API_KEY")

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
    GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini/gemini-3.1-flash-lite")
    NEWS_TOPICS = os.getenv("NEWS_TOPICS", "AI,technology").split(",")

    GOOGLE_CREDENTIALS_BASE64 = os.getenv("GOOGLE_CREDENTIALS_BASE64")

    @classmethod
    def validate(cls):
        required = {
            "SLACK_BOT_TOKEN": cls.SLACK_BOT_TOKEN,
            "SLACK_CHANNEL_ID": cls.SLACK_CHANNEL_ID,
            "SERPER_API_KEY": cls.SERPER_API_KEY,
            "GOOGLE_SHEET_ID": cls.GOOGLE_SHEET_ID,
            "GEMINI_API_KEY": cls.GEMINI_API_KEY,
        }

        missing = [key for key, value in required.items() if not value]

        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


config = Config()
