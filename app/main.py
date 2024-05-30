import uvicorn
from fastapi import FastAPI
from app.routes.user_router import user_router
from app.routes.operation_router import operation_router
from app.routes.visualization_router import visualization_router

app = FastAPI()

# Include routers for different endpoints
app.include_router(operation_router, prefix="/operations")
app.include_router(user_router, prefix="/users")
app.include_router(visualization_router, prefix="/visualization")

if __name__ == "__main__":
    # Run the application using Uvicorn server
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
