"""Research Assistant"""

from app.research.assistant import ResearchAssistant
from .email import send_email_with_attachment

__all__ = ["ResearchAssistant", "send_email_with_attachment"]