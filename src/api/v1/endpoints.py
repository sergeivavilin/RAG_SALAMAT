import requests  # type: ignore
from typing import Annotated, Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import select, text
from sqlalchemy.orm import Session
from starlette.requests import Request

from src.common.tools.ReAct_agent import agent
from src.db.CRUD import create_db, drop_db, update_db
from src.db.database import get_db
from src.db.Models import Pharmacy, PharmacyProduct, Product

router: APIRouter = APIRouter()


@router.get("/ask_llm", tags=["Agent"])
async def ask_agent(
    request: Request,
) -> Any:
    try:
        body = await request.json()
    except Exception as e:
        if isinstance(e, ValueError):
            return {"status_code": 400, "message": "Invalid JSON body"}
        else:
            return {"status_code": 500, "message": "Internal server error"}

    user_input = body.get("user_input", None)
    thread_id = body.get("thread_id", None)

    if user_input and thread_id:
        inputs = {"messages": [("user", user_input)]}
        config = {"configurable": {"thread_id": thread_id}}
    else:
        return {"status_code": 400, "message": "Missing user_input or thread_id"}

    answer = agent.invoke(inputs, config=config)
    try:
        ai_answer = answer["messages"][-1].content
    except AttributeError:
        return {"status_code": 500, "message": "Unexpected response format from agent"}

    return {"answer": ai_answer}


@router.get("/status_DB", tags=["database"])
async def get_postgres_db_status(
    get_db_session: Annotated[Session, Depends(get_db)],
) -> Dict[str, Any]:
    status = get_db_session.scalar(text("SELECT version();"))
    if status:
        return {"status": "ok", "postgres_version": status}
    return {"status": "error"}


@router.get("/get_all_products", tags=["database"])
async def get_all_products(db: Annotated[Session, Depends(get_db)]) -> Dict[str, Any]:
    amount_updated = db.scalars(select(Product)).all()
    return {"status_code": 201, "message": f"Total products: {len(amount_updated)}"}


@router.get("/get_all_pharmacies_by_product_name", tags=["database"])
async def get_all_pharmacies_by_product(
    product_name: str, db: Annotated[Session, Depends(get_db)]
) -> Dict[str, Any]:
    stmt = (
        select(Pharmacy)
        .join(PharmacyProduct, Pharmacy.id == PharmacyProduct.pharmacy_id)
        .join(Product, Product.id == PharmacyProduct.product_id)
        .where(Product.name == product_name)
    )
    pharmacies_products = db.scalars(stmt).all()

    return {
        "status_code": 201,
        "message": f"Total products: {len(pharmacies_products)}",
    }


@router.get("/get_all_pharmacies_by_like_product_name", tags=["database"])
async def get_all_pharmacies_by_like_product_name(
    product_name: str, db: Annotated[Session, Depends(get_db)]
) -> Dict[str, Any]:
    stmt = (
        select(Pharmacy)
        .join(PharmacyProduct, Pharmacy.id == PharmacyProduct.pharmacy_id)
        .join(Product, Product.id == PharmacyProduct.product_id)
        .where(Product.name.ilike(f"%{product_name}%"))
    )
    pharmacies_products = db.scalars(stmt).all()

    return {
        "status_code": 201,
        "message": f"Total products: {len(pharmacies_products)}",
    }


@router.get("/get_all_pharmacies", tags=["database"])
async def get_all_pharmacies(db: Annotated[Session, Depends(get_db)]) -> Dict[str, Any]:
    amount_updated = db.scalars(select(Pharmacy)).all()
    return {"status_code": 201, "message": f"Total pharmacies: {amount_updated}"}


@router.get("/get_all_pharmacies_products", tags=["database"])
async def get_all_pharmacies_products(
    db: Annotated[Session, Depends(get_db)],
) -> Dict[str, Any]:
    amount_updated = db.scalars(select(PharmacyProduct)).all()
    return {
        "status_code": 201,
        "message": f"Total pharmacies_products: {amount_updated}",
    }


@router.post("/create_DB", tags=["database"])
async def create_tables() -> Dict[str, Any]:
    try:
        message = create_db()
    except Exception as e:
        return {"status": "error", "message": f"Error creating tables: {e}"}
    else:

        return {"status_code": 201, "transaction": f"{message}"}


@router.post("/update_DB", tags=["database"])
async def update_db_from_1c(
    # url: str,
    db: Annotated[Session, Depends(get_db)],
) -> Dict[str, Any]:
    amount_updated = update_db(db)
    return {"status_code": 201, "message": f"Total updated: {amount_updated}"}


@router.delete("/drop_DB", tags=["delete DB"])
async def delete_db() -> Dict[str, Any]:
    message = drop_db()
    return {"status_code": 201, "message": f"{message}"}


@router.get("/test_request", tags=["test_request"])
async def test_request() -> Dict[str, Any]:
    response = requests.get("https://google.com/")
    res = response.status_code
    return {"status_code": 201, "message": f"{res}"}
