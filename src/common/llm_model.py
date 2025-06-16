import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def init_openai_llm(
    model_name: str = "gpt-4",
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> ChatOpenAI:
    """
    Initialize the LLM model with specified parameters.

    Args:
        model_name: Name of the OpenAI model to use (default: "gpt-4")
        temperature: Controls randomness in the output (default: 0.2)
        max_tokens: Maximum number of tokens to generate (default: None)

    Returns:
        ChatOpenAI: Initialized chat model instance
    """
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        return ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=api_key,
        )
    except Exception as e:
        raise Exception(f"Failed to initialize LLM: {str(e)}")


# Initialize the default LLM instance
LLM = init_openai_llm(model_name="gpt-4.1-nano")
SYSTEM_PROMPT: str | None = os.getenv("SYSTEM_PROMPT")

if __name__ == "__main__":
    print(LLM.invoke("Tell me a joke about dogs"))
