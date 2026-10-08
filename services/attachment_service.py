from pathlib import Path
from typing import Any
from uuid import uuid4

from repositories.grievance_repository import GrievanceRepository
from utils.constants import MAX_ATTACHMENTS
from utils.validators import file_extension, validate_file


class AttachmentService:
    def __init__(self, client: Any, bucket: str) -> None:
        self.client = client
        self.bucket = bucket
        self.grievances = GrievanceRepository(client)

    def upload_all(self, grievance_id: str, user_id: str, files: list[Any]) -> None:
        if len(files) > MAX_ATTACHMENTS:
            raise ValueError("A grievance can have at most 5 attachments.")
        uploaded: list[str] = []
        try:
            for file in files:
                valid, message = validate_file(file)
                if not valid:
                    raise ValueError(message)
                path = f"{grievance_id}/{uuid4()}.{file_extension(file.name)}"
                self.client.storage.from_(self.bucket).upload(path, file.getvalue(), {"content-type": getattr(file, "type", "application/octet-stream")})
                uploaded.append(path)
                self.client.table("grievance_attachments").insert({"grievance_id": grievance_id, "file_name": Path(file.name).name, "storage_path": path, "file_type": getattr(file, "type", "application/octet-stream"), "file_size": file.size, "uploaded_by": user_id}).execute()
        except Exception:
            for path in uploaded:
                try:
                    self.client.storage.from_(self.bucket).remove([path])
                except Exception:
                    pass
            raise

    def signed_url(self, path: str) -> str:
        return self.client.storage.from_(self.bucket).create_signed_url(path, 300)["signedURL"]