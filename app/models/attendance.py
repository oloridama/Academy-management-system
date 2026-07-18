# attendance model
from dataclasses import dataclass
from app.models.date import Date
from app.models.batch import Batch

@dataclass
class Attendance:
    first_name: str # name could be student or academic staff
    last_name: str
    date: Date
    batch_class: str = ""     # this is the batch class a student is suppose to attend or an academic staff is suppose to teach
    present_status: bool  # true if present, false if absent

@dataclass
class BatchClassAttendance:
    """
    This models the attendance of a batch class for a specific date.
    """
    date: Date
    lesson: str = ""
    names_of_students_present = list[str] = None  
    number_of_students_present: int = 0
    batch: Batch  
    # students_absent should be calculated as the difference 
    # between the batch capacity and the number of students present
    # but initialize the field without a default math equation
    students_absent: int = 0

    # dynamically calculate the number of absent students
    def __post_init__(self):
        self.number_of_students_present = len(self.names_of_students_present)
        self.students_absent = len(self.batch.enrolled_students) - self.number_of_students_present