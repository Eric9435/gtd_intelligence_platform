ROLE_ADMIN = "ADMIN"
ROLE_ENGINEER = "ENGINEER"
ROLE_VIEWER = "VIEWER"


def can_access_admin(role: str) -> bool:
    return role == ROLE_ADMIN


def can_edit(role: str) -> bool:
    return role in [ROLE_ADMIN, ROLE_ENGINEER]


def can_view(role: str) -> bool:
    return role in [ROLE_ADMIN, ROLE_ENGINEER, ROLE_VIEWER]
