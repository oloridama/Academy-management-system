# models the enrollment of a student
from dataclasses import dataclass

from app.models.date import Date

@dataclass
class Enrollment:
    """
    This models the enrollment of a student in a batch.
    """
    first_name: str 
    last_name: str 
    enrollment_id = ""    # this is different from student id, its for sorting enrollment into batches
    batch_id: str = ""
    Enrollment_date: Date = None # a student can be enrolled in a batch at any time, but the enrollment date is the date when the student was enrolled in the batch.
    payment_status: bool = False  # true if student has paid for the course, false if not    
    status: str = ""      # this is whether the enrollment is active, suspended or graduated
