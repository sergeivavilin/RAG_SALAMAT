import os

from langchain_openai import ChatOpenAI

from src.settings.config import LLMSettings


def init_openai_llm() -> ChatOpenAI:
    """
    Initialize the LLM model with specified parameters.

    Returns:
        ChatOpenAI: Initialized chat model instance
    """
    try:
        settings = LLMSettings()
        return ChatOpenAI(
            model_name=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            openai_api_key=settings.openai_api_key,
        )
    except Exception as e:
        raise Exception(f"Failed to initialize LLM: {str(e)}")


# Initialize the default LLM instance and system prompt
LLM = init_openai_llm()
SYSTEM_PROMPT: str | None = os.getenv("SYSTEM_PROMPT")

if __name__ == "__main__":
    print(LLM.invoke("Tell me a joke about dogs"))
