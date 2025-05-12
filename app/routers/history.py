from fastapi import APIRouter, Query, Depends

from app.db import get_db
from app.models.models import Message
from app.schemas.message import MessageRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

history_router = APIRouter(prefix="/history")


@history_router.get("/{chat_id}", response_model=[MessageRead])
async def get_history(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    return result.scalars().all()
