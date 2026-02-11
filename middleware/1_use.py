from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# 中间件 - 在每次请求和响应都会执行的函数

@app.middleware("http")
async def middleware1(request, call_next):
    print("middleware1 - started")
    response = await call_next(request)
    print("middleware1 - ended")
    return response

@app.middleware("http")
async def middleware2(request, call_next):
    print("middleware2 - started")
    response = await call_next(request)
    print("middleware2 - ended")
    return response


# 自定义响应数据格式
# 请求体

class User(BaseModel):
    user_name: str
    password: str = Field(..., max_length=20, min_length=6, description="用户密码")


class ResponseRegister(BaseModel):
    user_name: str = Field(description="用户名")

@app.post("/user/register", response_model=ResponseRegister)
async def register(user: User):
    if user.user_name == " ":
        raise HTTPException(status_code=501, detail="用户名不能为空格")
    return {"user_name": user.user_name}
