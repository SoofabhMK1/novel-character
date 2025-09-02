from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# 创建 SQLAlchemy 引擎
# connect_args 是为了在多线程环境中（比如 FastAPI）使用 SQLite 时才需要的，
# 对于 PostgreSQL，通常不需要。但保留它作为良好实践的示例。
engine = create_engine(
    str(settings.DATABASE_URL), 
    pool_pre_ping=True
)

# 创建一个 SessionLocal 类
# 这个类的实例将是实际的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    一个 FastAPI 依赖项，用于为每个请求提供一个独立的数据库会话。

    它使用 try/finally 块来确保数据库会话在使用后总是被关闭。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()