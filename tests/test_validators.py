from types import SimpleNamespace

import pytest

from utils.validators import is_valid_student_id, validate_email, validate_file, validate_phone, validate_text


@pytest.mark.parametrize("value", ["24BCE1234", "25CSE0001", "23ECE1234", "24bce1234"])
def test_valid_student_ids_are_strict_and_normalized(value):
    assert is_valid_student_id(value)


@pytest.mark.parametrize("value", ["24BCE123", "24BCE12345", "BCE1234", "2024BCE1234", "24-BCE-1234"])
def test_invalid_student_ids(value):
    assert not is_valid_student_id(value)


@pytest.mark.parametrize("name", ["evidence.pdf", "photo.jpg", "image.png", "document.docx"])
def test_allowed_files(name):
    valid, message = validate_file(SimpleNamespace(name=name, size=1024, type="application/octet-stream"))
    assert valid, message


def test_oversized_file_is_rejected():
    valid, _ = validate_file(SimpleNamespace(name="evidence.pdf", size=10 * 1024 * 1024 + 1))
    assert not valid


def test_unsupported_file_is_rejected():
    valid, _ = validate_file(SimpleNamespace(name="script.exe", size=1024))
    assert not valid


def test_basic_form_validators():
    assert validate_text("A real grievance description", 20, 100)
    assert not validate_text("short", 20, 100)
    assert validate_email("student@vit.ac.in")
    assert not validate_email("not-an-email")
    assert validate_phone("+91 9876543210")