from fastapi import APIRouter


userRouter = APIRouter(prefix='/user')

@userRouter.post('/login')
async def login(id : str, pw : str) -> dict :
    # id는 반드시 4자 이상
    # pw는 8자리 이상 특수문자, 숫자, 알파벳 반드시 포함