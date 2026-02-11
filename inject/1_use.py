from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

app = FastAPI()

# 依赖注入：可以用来共享通用的逻辑，避免代码重复
# 中间件是所有的请求都会走，依赖注入根据你的需求自己注入
# 优点：
# 1. 代码复用：一次编写，多处使用
# 2. 解耦：业务逻辑与基础设施代码分离
# 3. 易于测试：轻松的用模拟依赖替换真实依赖进行测试


async def common_parameters():
    return {"message": "1111"}
# 自定义响应数据格式
# 请求体

class User(BaseModel):
    user_name: str
    password: str = Field(..., max_length=20, min_length=6, description="用户密码")


class ResponseRegister(BaseModel):
    user_name: str = Field(description="用户名")

@app.post("/user/register", response_model=ResponseRegister)
async def register(user: User):
    common = Depends(common_parameters)
    print(common)
    if user.user_name == " ":
        raise HTTPException(status_code=501, detail="用户名不能为空格")
    return {"user_name": user.user_name}
