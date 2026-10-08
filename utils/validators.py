import re
from pathlib import Path
from typing import Any

from .constants import ALLOWED_EXTENSIONS, MAX_FILE_SIZE

STUDENT_ID_PATTERN = re.compile(r"^[0-9]{2}[A-Z]{3}[0-9]{4}$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_student_id(value: str) -> str:
    return value.strip().upper()


def is_valid_student_id(value: str) -> bool:
    return bool(STUDENT_ID_PATTERN.fullmatch(normalize_student_id(value)))


def validate_email(value: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(value.strip()))


def validate_phone(value: str) -> bool:
    return bool(re.fullmatch(r"\+?[0-9 ()-]{7,20}", value.strip()))


def validate_text(value: str, minimum: int, maximum: int) -> bool:
    length = len(value.strip())
    return minimum <= length <= maximum


def file_extension(name: str) -> str:
    return Path(name).suffix.lower().lstrip(".")


def validate_file(file: Any) -> tuple[bool, str]:
    name = getattr(file, "name", "")
    size = getattr(file, "size", 0)
    extension = file_extension(name)
    if extension not in ALLOWED_EXTENSIONS:
        return False, "Allowed files are PDF, PNG, JPG, JPEG, DOC, and DOCX."
    if not isinstance(size, int) or size <= 0 or size > MAX_FILE_SIZE:
        return False, "Each attachment must be greater than 0 and no larger than 10 MB."
    return True, ""