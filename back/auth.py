from fastapi import APIRouter, HTTPException
from users import fake_users
from jose import jwt

SECRET_KEY = "secret"
router = APIRouter()

@router.post("/login")
def login(data: dict):
    user = fake_users.get(data["username"])
    if not user or user["password"] != data["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"username": data["username"], "role": user["role"]},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "role": user["role"]}
