from typing import Any

from repositories.grievance_repository import GrievanceRepository
from services.attachment_service import AttachmentService
from utils.constants import MAX_ATTACHMENTS
from utils.validators import validate_text


class GrievanceService:
    def __init__(self, client: Any, bucket: str) -> None:
        self.repository = GrievanceRepository(client)
        self.attachments = AttachmentService(client, bucket)

    def submit(self, user_id: str, category_id: str, title: str, description: str, anonymous: bool, files: list[Any]) -> dict[str, Any]:
        if not category_id or not validate_text(title, 3, 160):
            raise ValueError("Choose a category and enter a title between 3 and 160 characters.")
        if not validate_text(description, 20, 10000):
            raise ValueError("Description must be between 20 and 10,000 characters.")
        if len(files) > MAX_ATTACHMENTS:
            raise ValueError("A grievance can have at most 5 attachments.")
        grievance = self.repository.create({"student_auth_user_id": user_id, "category_id": category_id, "title": title.strip(), "description": description.strip(), "is_anonymous": anonymous, "status": "submitted"})
        self.repository.add_initial_history(grievance["id"], user_id)
        if files:
            self.attachments.upload_all(grievance["id"], user_id, files)
        return grievance