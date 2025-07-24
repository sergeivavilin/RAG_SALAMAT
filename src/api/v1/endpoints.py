from fastapi import APIRouter
from langchain_core.messages import HumanMessage

from src.common.llm_model import LLM

router: APIRouter = APIRouter()


@router.get("/ask_llm")
async def ask_agent(human_input: str) -> dict[str, str]:
    messages = [
        HumanMessage(content=human_input),
    ]
    answer = LLM.invoke(messages).content
    return {"message": answer}
