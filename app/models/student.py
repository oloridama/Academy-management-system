# this is the student model script
from dataclasses import dataclass
from PIL import Image

@dataclass
class Student:
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