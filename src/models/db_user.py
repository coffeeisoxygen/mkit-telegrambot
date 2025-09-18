"""database schemas untuk user."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.models.mixins import TimestampMixin
from src.schemas import UserApprovalStatus


class User(Base, TimestampMixin):
    """Model untuk user di database."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, unique=True, index=True, nullable=False
    )  # Telegram user ID
    name: Mapped[str] = mapped_column(
        String, nullable=False
    )  # not unique, bisa aja nama user nya sama yg di stored dsini bisa username / name
    rate_limit: Mapped[int] = mapped_column(
        Integer, default=5
    )  # Jumlah maksimum permintaan per menit agar tidak abuse

    is_superuser: Mapped[int] = mapped_column(Integer, default=0)  # 0 = False, 1 = True
    status: Mapped[int] = mapped_column(
        Integer, default=UserApprovalStatus.PENDING
    )  # 0 = pending, 1 = approved, 2 = rejected, 3 = blocked, 4 = banned, 5 = deleted
