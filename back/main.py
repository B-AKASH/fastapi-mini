from fastapi import FastAPI
from auth import router as auth_router
from inventory import router as inventory_router
from ai_chat import router as ai_router
from sales import router as sales_router

app = FastAPI(title="ERP Backend")

app.include_router(auth_router)
app.include_router(inventory_router)
app.include_router(ai_router)


app.include_router(sales_router)
