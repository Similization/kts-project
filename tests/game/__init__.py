from dataclasses import asdict

from kts_backend.user.dataclasses import User


def user2dict(user: User) -> dict:
    """
    Convert User object to dict
    :param user: User
    :return: dict
    """
    return asdict(user)
