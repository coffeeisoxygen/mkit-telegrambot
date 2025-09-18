from enum import IntEnum


class UserApprovalStatus(IntEnum):
    PENDING = 0  # butuh admin verifikasi
    APPROVED = 1  # verified by admin
    REJECTED = 2  # ditolak oleh admin

    BLOCKED = 3  # ini tempororay , semisal karena rate limit / abuse
    BANNED = 4  # ini permanent , semisal karena spam / abuse
    DELETED = 5  # soft deleted
