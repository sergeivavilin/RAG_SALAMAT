from fastapi import FastAPI

from src.api.v1 import endpoints

app = FastAPI(
    title="FastAPI Template",
    version="0.1.0",
)

app.include_router(endpoints.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
