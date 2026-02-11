

from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

ASYNC_DATABASE_URL = "mysql+aiomysql://root:mysql.com@115.190.97.143:3306/Hello_FastAPI?charset=utf8"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, # 可选， 输出SQL日志
    pool_size=10, # 设置连接池中保持的持久连接数
    max_overflow=20 # 设置连接池允许创建的额外连接数
)

# 定义基类
class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=datetime.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), onupdate=func.now(), default=datetime.now)

# 表对应的模型类
class Book(Base):
    __tablename__="book"
    
    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    book_name: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")

# 建表：定义函数建表 -> FastAPI 启动的时候调用建表函数
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # 实用模型类的元数据进行创建

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, # 绑定数据库引擎
    class_=AsyncSession, # 指定会话类
    expire_on_commit=False # 回话对象不过期，不重新查询数据库
)

# 依赖项，用于获取数据库会话
async def get_database():
    async with AsyncSessionLocal() as session:
        try: 
            yield session # 返回数据库会话给路由处理函数
            print("session.commit -- auto")
            await session.commit() # 无异常，提交事务
        except Exception:
            await session.rollback() # 有异常则回滚
            raise
        finally:
            await session.close() # 关闭会话