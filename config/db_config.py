
# 数据库URL
from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


ASYNC_DATABASE_URL = "mysql+aiomysql://root:mysql.com@140.143.164.230:3306/news_app?charset=utf8mb4"



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
            await session.commit() # 无异常，提交事务
        except Exception:
            await session.rollback() # 有异常则回滚
            raise
        finally:
            await session.close() # 关闭会话