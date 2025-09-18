"""crud operations for user."""

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas import UserApprovalStatus, UserCreate, UserInDB


async def user_exists(db_session: AsyncSession, user_id: int) -> bool:
    stmt = select(User).where(User.user_id == user_id)
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def create_user(
    db_session: AsyncSession,
    user: UserCreate,
    rate_limit: int = 20,
    is_superuser: int = 0,
    status: int = UserApprovalStatus.PENDING,
) -> UserInDB:
    if await user_exists(db_session, user.user_id):
        raise ValueError(f"User with user_id {user.user_id} already exists.")
    try:
        user_obj = User(
            user_id=user.user_id,
            name=user.name,
            rate_limit=rate_limit,
            is_superuser=is_superuser,
            status=status,
        )
        db_session.add(user_obj)
        await db_session.commit()
        await db_session.refresh(user_obj)
        logger.info(f"User created: {user_obj.id}")
        return UserInDB.model_validate(user_obj)
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise
