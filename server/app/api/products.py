from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies import get_product_service

router = APIRouter(prefix="/api/products")


@router.get("")
def list_products(category: str | None = None, sub_category: str | None = None, keyword: str | None = None,
                  limit: int = Query(20, ge=1, le=100), service=Depends(get_product_service)):
    return {"products": service.list(category, sub_category, keyword, limit)}


@router.get("/{product_id}")
def product_detail(product_id: str, service=Depends(get_product_service)):
    product = service.get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product

