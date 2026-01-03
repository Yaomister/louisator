

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import  ForeignKey
from datetime import datetime, timezone
import uuid


class Base(AsyncAttrs, DeclarativeBase):
    async def save(self, db : AsyncSession):
        try:
            db.add(self)
            await db.commit()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail="Could not save to database")
    @classmethod
    async def find_by_id(cls, id : str, db: AsyncSession):
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        return result.scalars().first
    
class Session(Base):
    __tablename__ = "session"
    id: Mapped[uuid.UUID] = mapped_column( primary_key=True, default=uuid.uuid4)
    start_time : Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone))
    end_time: Mapped[datetime] = mapped_column(nullable=True)


class State(Base):
    __tablename__ = "state"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id = mapped_column(ForeignKey("session.id"), nullable=False)
    session = relationship("Session")
    timestamp: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone))
    energy: Mapped[float]
    activity: Mapped[str] 


class Event(Base):
    __tablename__ = "event"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    session_id = mapped_column(ForeignKey("session.id"), nullable=False)
    session = relationship("Session")
    timestamp: Mapped[datetime] = mapped_column( nullable=False, default=lambda: datetime.now(timezone.utc)) 
    type: Mapped[str]
    description: Mapped[str]



class KnownFace(Base):
    __tablename__ = 'known_face'
    id : Mapped[uuid.UUID] = mapped_column(primary_key=True, nullable=False, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    

