#course script
from dataclasses import dataclass

@dataclass
class Course:
    """
    this models a course in the institution
    """
    name: str
    field: str # e.g science or art or social sciences
    duration: str # short course or full academic calender
    compulsory: bool # this is whether all students will take the course or not