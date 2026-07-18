from dataclasses import dataclass

@dataclass
class Batch:
    """
    A batch is a training session for a course at a specific time.
    A batch has a start date and an end date. 
    A batch can be in registraion, active or completed.
    """
    batch_id: str = ""
    course_name: str = ""
    start_date: str = ""
    end_date: str = ""
    capacity: int = 0
    enrolled_students: list[str] = None  # this is a list of students that have enrolled in the batch
    instructors: list[str] = None  # this is a list of instructors that will be teaching the batch
    status: str = ""   # this represent if the batch is in registration, active or completed