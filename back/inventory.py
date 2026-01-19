from fastapi import APIRouter, Depends, HTTPException, Header
from jose import jwt


router = APIRouter()
SECRET_KEY = "secret"

inventory_data = [
    {"product_name": "Laptop", "category": "Electronics", "price": 60000, "current_stock": 10},
    {"product_name": "Phone", "category": "Electronics", "price": 30000, "current_stock": 25},
]

@router.get("/inventory")
def get_inventory(authorization: str = Header(...)):
    try:
        token = authorization.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if payload["role"] not in ["admin", "staff"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return inventory_data
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
