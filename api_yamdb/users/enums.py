from enum import Enum


class UserRole(Enum):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
