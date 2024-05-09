import uvicorn
from fastapi import FastAPI
from app.conrollers.user_controller import user_router
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

CONNECTION_STRING = 'mongodb://localhost/hand2products'


async def connect_db():
    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        print("Connected to database cluster.")


app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080)
