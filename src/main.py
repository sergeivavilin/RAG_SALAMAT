from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.v1 import endpoints

app = FastAPI(
    title="FastAPI Test Salamat",
    version="0.1.0",
)

app.include_router(endpoints.router, prefix="/api/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
