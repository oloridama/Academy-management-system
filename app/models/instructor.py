# this script is for modelling the instructor
from dataclasses import dataclass

@dataclass
class Instructor:
    """
    Contains details about the instructor
    """
    first_name: str
    last_name: str
    date_of_birth: str
    email: str
    phone: str
    instructor_id: str
    qualification: str
    courses: list[str] # number of course the instructor covers and their names
