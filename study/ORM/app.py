from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from .base import create_tables, get_database, Book
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_tables()
    yield
    # Shutdown (如果需要清理操作可以在这里添加)

app = FastAPI(lifespan=lifespan)

# 获取一条数据
# scalars().first() 
# get(模型类, 主键值)
@app.get('/book/all')
async def get(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book)) # 返回一个ORM对象
    book = result.scalars().all() # 获取所有数据
    return book

# 聚合查询
@app.get('/book/count')
async def get_book_count(db: AsyncSession = Depends(get_database), ):
    result = await db.execute(select(func.count(Book.id))) # 返回一个ORM对象
    book = result.scalar()
    return book

@app.get('/book/price/{book_id}')
async def get_book_by_price(book_id: int ,db: AsyncSession = Depends(get_database), ):
    result = await db.execute(select(Book).where((Book.price > 50) |  (Book.id == book_id))) # 返回一个ORM对象
    book = result.scalars().all()
    return book

@app.get('/book/id/{book_id}')
async def get_book_by_id(book_id: int ,db: AsyncSession = Depends(get_database), ):
    result = await db.execute(select(Book).where(Book.id == book_id)) # 返回一个ORM对象
    book = result.scalar_one_or_none()
    return book

# 分页查询
# select().offset().limit()
# offset = (当前页数 - 1) * limit

@app.get("/book/list")
async def get_book_list(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_database)):
    skip = (page - 1) * page_size
    stmt = select(Book).offset(skip).limit(page_size)
    result = await db.execute(stmt)
    books = result.scalars().all()
    return {"books": books}
     

class BookInfo(BaseModel):
    book_name: str
    author: str
    price: float
    
@app.post("/book/add")
async def add_book(book: BookInfo,db:AsyncSession = Depends(get_database)):
    book_obj = Book(**book.model_dump())
    db.add(book_obj)
    await db.flush()    # flush 将数据写入数据库但不提交，可获取自增 id 等字段
    await db.refresh(book_obj)  # 刷新获取数据库生成的字段（id、create_time等）
    return book_obj     # commit 由 get_database 依赖自动完成

# class BookInfo(BaseModel):
#     book_name: str
#     author: str
#     price: float
    
@app.put("/book/update/{id}")
async def update_book(id: int, data: BookInfo,db:AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, id)
    if db_book is None: 
        raise HTTPException(
            status_code=404,
            detail="查无此书"
        )
    db_book.book_name = data.book_name
    db_book.author = data.author
    db_book.price = data.price
    return db_book  # commit 由 get_database 依赖自动完成

# 删除
@app.delete("/book/delete_book/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    # 先查在删
    db_book = await db.get(Book, book_id)
    if db_book is None: 
        raise HTTPException(
            status_code=404,
            detail="查无此书"
        )
    await db.delete(db_book)
    return {"message": "删除成功"}  # commit 由 get_database 依赖自动完成