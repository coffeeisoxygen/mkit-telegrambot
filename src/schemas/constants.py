from enum import IntEnum


class UserApprovalStatus(IntEnum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    BLOCKED = 3
    BANNED = 4
    DELETED = 5
