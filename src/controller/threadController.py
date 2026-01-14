from fastapi import APIRouter
from src.service.threadService import testServcie


threadRouter = APIRouter(prefix='/thread')

@threadRouter.get("/")
async def test() -> dict :
    value = await testServcie()
    return {"key" : f"value : {value}"}
