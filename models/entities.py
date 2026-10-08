from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Student:
    auth_user_id: str
    student_id: str
    name: str
    email: str
    phone: str
    department: str | None = None
    programme: str | None = None
    year: int | None = None
    semester: int | None = None

    @classmethod
    def from_row(cls, row: dict[str, Any]) -> "Student":
        return cls(**{field: row.get(field) for field in cls.__dataclass_fields__})


@dataclass(frozen=True)
class Grievance:
    id: str
    student_auth_user_id: str
    category_id: str
    title: str
    description: str
    is_anonymous: bool
    status: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class Notification:
    id: str
    title: str
    message: str
    is_read: bool
    created_at: str
    grievance_id: str | None = None