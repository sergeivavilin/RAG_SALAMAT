from fastapi import APIRouter
from langchain_core.messages import HumanMessage, SystemMessage

from src.common.llm_model import LLM, SYSTEM_PROMPT

router: APIRouter = APIRouter()


@router.get("/ask_llm")  # type: ignore
async def ask_agent(human_input: str) -> dict[str, str]:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=human_input),
    ]
    answer = LLM.invoke(messages).content
    return {"message": answer}
