"""pydantic schema for user entity."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from schemas import UserApprovalStatus


class UserConfig(BaseModel):
    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "coerce_numbers_to_str": True,
    }


class UserCreate(UserConfig):
    user_id: int = Field(..., description="Telegram user ID")
    name: str = Field(..., description="Name of the user")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: int) -> int:
        if not isinstance(v, int) or v <= 0:
            raise ValueError("Invalid Telegram user_id. Must be a positive integer.")
        return v


class SeedDefaultAdminUser(UserCreate):
    rate_limit: int = Field(
        default=20, description="Number of messages allowed per minute"
    )
    is_superuser: int = Field(default=1, description="1 if superuser, else 0")
    status: UserApprovalStatus = Field(
        default=UserApprovalStatus.APPROVED,
        description="User status, default is approved",
    )


class UserInDB(UserConfig):
    id: int = Field(description="Internal database ID")
    user_id: int = Field(description="Telegram user ID")
    name: str = Field(description="Name of the user")
    rate_limit: int = Field(description="Number of messages allowed per minute")
    is_superuser: int = Field(description="1 if superuser, else 0")
    status: UserApprovalStatus = Field(description="User status")
    created_at: datetime = Field(description="Timestamp when the user was created")
    updated_at: datetime = Field(description="Timestamp when the user was last updated")
    deleted_at: datetime | None = Field(
        default=None, description="Timestamp when the user was soft deleted"
    )


class SeedResponse(SeedDefaultAdminUser):
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: datetime = Field(
        ..., description="Timestamp when the user was last updated"
    )
    deleted_at: datetime | None = Field(
        default=None, description="Timestamp when the user was soft deleted"
    )
