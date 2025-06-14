from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get("/ping")  # type: ignore[misc]
async def ping() -> dict[str, str]:
    return {"message": "pong"}
