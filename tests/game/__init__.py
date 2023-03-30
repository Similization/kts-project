from dataclasses import asdict

from kts_backend.user.dataclasses import User


def user2dict(user: User):
    return asdict(user)
