from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserResponse
from .deps import get_db

router = APIRouter()

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(User).where(User.id == user_id)
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.email = f"deleted_{user_id}@example.com"
    user.is_active = False
    await db.commit()
    
    async def final_deletion():
        await db.delete(user)
        await db.commit()
    
    background_tasks.add_task(final_deletion)
    return user
