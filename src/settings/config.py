import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")


class LLMSettings(BaseModel):  # type: ignore
    """Конфигурация для языковой модели OpenAI."""

    openai_api_key: str = Field(
        default=os.getenv("OPENAI_API_KEY"), description="API-ключ OpenAI"
    )
    model_name: str = Field(default="gpt-3.5-turbo", description="Название модели")
    temperature: float = Field(
        default=0.2, ge=0.0, le=1.0, description="Креативность модели"
    )
    max_tokens: Optional[int] = Field(
        default=1024, description="Максимальное число токенов в ответе"
    )
    timeout: Optional[int] = Field(default=5, description="Таймаут запроса в секундах")
    system_prompt: Optional[str] = Field(
        default=os.getenv("SYSTEM_PROMPT"), description="Системный промпт для модели"
    )
