import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

if not os.getenv("PINECONE_API_KEY"):
    raise ValueError("PINECONE_API_KEY not found in environment variables")

if not os.getenv("API_TOKEN"):
    raise ValueError("API_TOKEN not found in environment variables")


def _get_system_prompt() -> str:
    file_path = Path(__file__).resolve().parent / "system_prompt.txt"

    if not file_path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    with open(file_path, "r", encoding="utf-8") as f:
        sys_prompt = f.read()

    return sys_prompt


AGENT_PROMPT = _get_system_prompt()


class OpenAIModel(BaseModel):  # type: ignore
    """Базовый класс для языковой модели OpenAI."""

    openai_api_key: str = Field(
        default=os.getenv("OPENAI_API_KEY"), description="API-ключ OpenAI"
    )
    timeout: Optional[int] = Field(default=5, description="Таймаут запроса в секундах")


class LLMSettings(OpenAIModel):
    """Конфигурация для языковой модели OpenAI."""

    chat_model: str = Field(
        default="gpt-4o-mini", description="Название модели для чата"
    )
    temperature: float = Field(
        default=0.2, ge=0.0, le=1.0, description="Креативность модели"
    )
    max_tokens: Optional[int] = Field(
        default=1024, description="Максимальное число токенов в ответе"
    )
    system_prompt: Optional[str] = Field(
        default=AGENT_PROMPT, description="Системный промпт для модели"
    )
