from fastapi import FastAPI
from src.controller.testController import testRouter

app = FastAPI()

@app.get("/")
async def main() ->dict : #입력 및 반환 타입으로 dict 명시
    return {"message" : "Hello world"}

app.include_router(testRouter)