from fastapi import APIRouter, HTTPException, Header
from jose import jwt

router = APIRouter()
SECRET_KEY = "secret"

sales_data = []

@router.post("/sell")
def sell_item(data: dict, authorization: str = Header(...)):
    try:
        token = authorization.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        if payload["role"] not in ["admin", "staff"]:
            raise HTTPException(status_code=403, detail="Not allowed")

        sales_data.append({
            "product": data["product"],
            "quantity": data["quantity"],
            "total": data["total"]
        })

        return {"message": "Sale recorded"}

    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/sales")
def get_sales(authorization: str = Header(...)):
    try:
        token = authorization.split()[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        if payload["role"] != "admin":
            raise HTTPException(status_code=403, detail="Admin only")

        return sales_data

    except:
        raise HTTPException(status_code=401, detail="Invalid token")
