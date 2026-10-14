from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from repositories.grievance_repository import GrievanceRepository
from repositories.notification_repository import NotificationRepository
from repositories.student_repository import StudentRepository
from services.grievance_service import GrievanceService


def test_student_profile_update_filters_identity_fields():
    client = MagicMock()
    client.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{"name": "Updated"}]

    result = StudentRepository(client).update_profile("user-1", {"name": "Updated", "auth_user_id": "other", "student_id": "other"})

    assert result == {"name": "Updated"}
    client.table.return_value.update.assert_called_once_with({"name": "Updated"})


def test_grievance_repository_returns_empty_categories_and_student_rows():
    client = MagicMock()
    client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value.data = []
    client.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value.data = None
    repository = GrievanceRepository(client)

    assert repository.categories() == []
    assert repository.get("missing") is None


def test_notification_repository_lists_and_marks_read():
    client = MagicMock()
    client.table.return_value.select.return_value.order.return_value.execute.return_value.data = [{"id": "n1", "is_read": False}]
    client.table.return_value.update.return_value.eq.return_value.execute.return_value = SimpleNamespace(data=[])
    repository = NotificationRepository(client)

    assert repository.list() == [{"id": "n1", "is_read": False}]
    repository.mark_read("n1")
    client.table.return_value.update.assert_called_once_with({"is_read": True})


def test_demo_submission_rejects_attachments_before_database_write():
    client = MagicMock()
    service = GrievanceService(client, "grievance-attachments")

    with pytest.raises(ValueError, match="disabled"):
        service.submit("user-1", "category-1", "Valid title", "This is a sufficiently detailed grievance description.", False, [object()])

    client.table.assert_not_called()