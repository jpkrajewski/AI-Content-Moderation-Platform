from dataclasses import dataclass

@dataclass
class UserInfo:
    id: int | None
    email: str | None
    verified_email: bool | None
    name: str | None
    given_name: str | None
    family_name: str | None
    picture: str | None
