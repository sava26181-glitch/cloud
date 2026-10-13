from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Integer, String, Text, select, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.config import settings

def normalize_db_url(url: str) -> str:
    # Render provides postgres:// or postgresql://; async SQLAlchemy uses asyncpg.
    if url.startswith("postgres://"):
        return "postgresql+asyncpg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    role: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

engine = create_async_engine(normalize_db_url(settings.database_url), pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_message(user_id: int, role: str, content: str):
    async with SessionLocal() as session:
        session.add(Message(user_id=user_id, role=role, content=content))
        await session.commit()

async def get_history(user_id: int, limit: int):
    async with SessionLocal() as session:
        result = await session.execute(
            select(Message).where(Message.user_id == user_id)
            .order_by(Message.id.desc()).limit(limit)
        )
        rows = list(result.scalars().all())
        rows.reverse()
        return [{"role": row.role, "content": row.content} for row in rows]

async def clear_history(user_id: int):
    async with SessionLocal() as session:
        await session.execute(delete(Message).where(Message.user_id == user_id))
        await session.commit()

async def close_db():
    await engine.dispose()
