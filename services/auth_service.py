from typing import Any

from repositories.student_repository import StudentRepository
from utils.validators import normalize_student_id


class AuthService:
    def __init__(self, client: Any, email_redirect_to: str = "http://localhost:8501") -> None:
        self.client = client
        self.email_redirect_to = email_redirect_to
        self.students = StudentRepository(client)

    def sign_up(self, student_id: str, name: str, email: str, phone: str, password: str) -> Any:
        response = self.client.auth.sign_up({
            "email": email.strip().lower(),
            "password": password,
            "options": {
                "data": {
                    "student_id": normalize_student_id(student_id),
                    "name": name.strip(),
                    "phone": phone.strip(),
                },
                "email_redirect_to": self.email_redirect_to,
            },
        })
        if not response.user:
            raise ValueError("Supabase did not create an authentication user.")
        return response

    def sign_in(self, student_id: str, password: str) -> Any:
        email = self.students.email_for_student_id(normalize_student_id(student_id))
        if not email:
            raise ValueError("No student account was found for that Student ID.")
        return self.client.auth.sign_in_with_password({"email": email, "password": password})

    def sign_out(self) -> None:
        self.client.auth.sign_out()