from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from supabase_client import DEMO_ACCOUNTS, clear_demo_session, require_demo_session, sign_in_demo_student, validate_demo_credentials


@pytest.mark.parametrize("student_id,password", [("24BCE1234", "abcd123"), ("24BCE5678", "abcd123")])
def test_defined_demo_accounts_are_accepted(student_id, password):
    assert validate_demo_credentials(student_id, password) is True


def test_unknown_student_id_is_rejected():
    assert validate_demo_credentials("24BCE9999", "student123") is False


def test_wrong_password_is_rejected():
    assert validate_demo_credentials("24BCE1234", "wrong-pass") is False


def test_invalid_student_id_format_is_rejected():
    assert validate_demo_credentials("abc123", "student123") is False


def test_logout_clears_session_data():
    session = {"student": {"student_id": "24BCE1234"}, "user": SimpleNamespace(id="demo-user-id")}
    cleared = clear_demo_session(session)
    assert "student" not in cleared
    assert "user" not in cleared


def test_unauthenticated_access_is_rejected():
    with pytest.raises(RuntimeError, match="authenticated"):
        require_demo_session({})


def test_session_for_another_student_is_rejected():
    with pytest.raises(RuntimeError, match="does not match"):
        require_demo_session({
            "student": {"student_id": "24BCE1234", "auth_user_id": "student-one"},
            "user": SimpleNamespace(id="student-two"),
        })


def test_demo_sign_in_uses_supabase_session(monkeypatch):
    fake_user = SimpleNamespace(id="user-123")
    fake_response = SimpleNamespace(user=fake_user, session={"access_token": "token", "refresh_token": "refresh"})
    fake_client = MagicMock()
    fake_client.rpc.return_value.execute.return_value.data = "student@vit.ac.in"
    fake_client.auth.sign_in_with_password.return_value = fake_response
    monkeypatch.setattr("supabase_client.get_supabase", lambda: fake_client)
    monkeypatch.setattr("supabase_client.get_demo_student_record", lambda student_id, client=None: {"student_id": student_id, "auth_user_id": "user-123", "email": "student@vit.ac.in"})

    response = sign_in_demo_student("24BCE1234", "abcd123")
    assert response.user.id == "user-123"
    fake_client.rpc.assert_called_once_with("resolve_student_email", {"p_student_id": "24BCE1234"})
    fake_client.auth.sign_in_with_password.assert_called_once_with({"email": "student@vit.ac.in", "password": "abcd123"})


def test_authenticated_client_rehydrates_session(monkeypatch):
    from supabase_client import authenticated_supabase

    fake_client = MagicMock()
    monkeypatch.setattr("supabase_client.get_supabase", lambda: fake_client)

    assert authenticated_supabase({"access_token": "access", "refresh_token": "refresh"}) is fake_client
    fake_client.auth.set_session.assert_called_once_with("access", "refresh")
