import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "").strip()
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5").strip()
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./bot.db").strip()
    max_history_messages: int = int(os.getenv("MAX_HISTORY_MESSAGES", "16"))
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "15"))
    max_output_chars: int = int(os.getenv("MAX_OUTPUT_CHARS", "24000"))
    app_host: str = os.getenv("HOST", "0.0.0.0")
    app_port: int = int(os.getenv("PORT", "10000"))

settings = Settings()
