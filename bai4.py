from fastapi import FastAPI, Path
from pydantic import Field,BaseModel
from typing import Annotated


products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5}
]

class ProductSchemaRequest(BaseModel):
    code: Annotated[str, Field(min_length=5,json_schema_extra={"example": "SP003"})]
    name: Annotated[str, Field(min_length=2)]
    price: Annotated[int, Field(gt=0)]
    stock: Annotated[int,Field(ge=0)]

app = FastAPI()

@app.put("/products/{product_id}")
def update_product_info(product_id: Annotated[int,Path(gt=0)], product: ProductSchemaRequest):
    prd = next((p for p in products if product_id == p['id']),None)

    if not prd:
        return {
            "detail": "Product not found"
        }
    
    for p in products:
        if p['code'] == product.code and p["id"] != product_id:
            return {
                "detail": "Product code already exists"
            }
        

    data = {
        "code": product.code,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }
    
    prd.update(data)

    return {
        "message": "Cập nhật thành công!",
        "data": data
    }