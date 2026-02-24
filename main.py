from fastapi import FastAPI
from routers import news

app = FastAPI()


@app.get('/book/all')
async def root():
    return {"message": "success"}

# 注册路由
app.include_router(news.router)