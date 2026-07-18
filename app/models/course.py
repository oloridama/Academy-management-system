#course script
from dataclasses import dataclass

@dataclass
class Course:
    """
    this models a course in the institution
    """
    name: str
    topics: list[str] # this is a list of topics that will be covered in the course
