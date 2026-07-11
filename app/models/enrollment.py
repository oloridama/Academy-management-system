# models the enrollment of a student
from dataclasses import dataclass
from student import Student

class Enrollment:
    def __init__(self, student):
        student = Student()
        first_name: str = student.first_name # name of new student
        last_name: str = student.last_name
        date_of_birth: str = student.date_of_birth
        email: str = student.email
        transfer: bool        # true if transferring from another school
        level: str
        Guardian: str
