# this is the student model script
from dataclasses import dataclass
from typing import TypedDict
from PIL import Image

@dataclass
class Student(TypedDict):
    """
    This models the information of a student.
    At runtime it can be used to create a student object with the following attributes.
    If used as a TypedDict, it can be used to create a dictionary with the following keys and values.
    """
    student_id: str
    first_name: str
    last_name: str
    gender: str     # male or female
    email: str
    phone: str
    emergency_contact: str
    Educational_background: str
    date_of_birth: str
    passport_photograph: Image.Image    # i considered using Path but the program user may just select and image directly
    created_at: str
    updated_at: str
    status: str   # acitve, suspended or graduated