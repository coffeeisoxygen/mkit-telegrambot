"""crud operations for user."""

from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas import UserApprovalStatus, UserInDB


async def user_exists(db_session: AsyncSession, user_id: int) -> bool:
    stmt = select(User).where(User.user_id == user_id)
    result = await db_session.execute(stmt)
    return result.scalar_one_or_none() is not None


async def create_user_entry(
    db_session: AsyncSession,
    user_id: int,
    name: str,
    rate_limit: int = 20,
    is_superuser: int = 0,
    status: int = UserApprovalStatus.PENDING,
    raise_if_exists: bool = True,
):
    if await user_exists(db_session, user_id):
        msg = f"User with user_id {user_id} already exists."
        if raise_if_exists:
            raise ValueError(msg)
        else:
            logger.info(msg)
            return None
    try:
        user_obj = User(
            user_id=user_id,
            name=name,
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


async def get_user_by_telegram_id(
    db_session: AsyncSession, user_id: int
) -> UserInDB | None:
    stmt = select(User).where(User.user_id == user_id)
    result = await db_session.execute(stmt)
    user_obj = result.scalar_one_or_none()
    if user_obj:
        return UserInDB.model_validate(user_obj)
    return None
