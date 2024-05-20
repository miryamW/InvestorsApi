import uvicorn
from fastapi import FastAPI
from app.routes.user_router import user_router
from app.routes.operation_router import operation_router

app = FastAPI()

app.include_router(operation_router, prefix="/operations")
app.include_router(user_router, prefix="/users")

if __name__ == "__main__":

    uvicorn.run("main:app", host="127.0.0.1", port=8080)
