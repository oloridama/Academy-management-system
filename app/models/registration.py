from dataclasses import dataclass

from app.models.batch import Batch
from app.models.date import Date
from app.models.student import Student

@dataclass
class Registration:
    """
    This models the registration of a prospect as a student
    """
    prospect_information: dict[str, Student] = None  # this is a dictionary that contains the prospect's information
    registration_id: str = ""
    application_date: Date = None
    admission_officer: str = ""
    selected_batch: Batch = None  # a student can change their selected batch and be enrolled to another batch or course
    payment_status: bool = False  # true if student has paid for the course, false if not
    status: str = ""  # 'completed', 'pending', 'rejected' or 'incomplete'