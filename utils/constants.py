from enum import StrEnum


class GrievanceStatus(StrEnum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REJECTED = "rejected"
    REOPENED = "reopened"


STATUS_CONFIG = {
    GrievanceStatus.SUBMITTED: {"label": "Submitted", "icon": "📝", "color": "#2563eb"},
    GrievanceStatus.UNDER_REVIEW: {"label": "Under Review", "icon": "🔎", "color": "#7c3aed"},
    GrievanceStatus.ASSIGNED: {"label": "Assigned", "icon": "👤", "color": "#0369a1"},
    GrievanceStatus.IN_PROGRESS: {"label": "In Progress", "icon": "⚙", "color": "#ca8a04"},
    GrievanceStatus.RESOLVED: {"label": "Resolved", "icon": "✓", "color": "#15803d"},
    GrievanceStatus.CLOSED: {"label": "Closed", "icon": "🔒", "color": "#475569"},
    GrievanceStatus.REJECTED: {"label": "Rejected", "icon": "!", "color": "#b91c1c"},
    GrievanceStatus.REOPENED: {"label": "Reopened", "icon": "↻", "color": "#c2410c"},
}
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "doc", "docx"}
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_ATTACHMENTS = 5