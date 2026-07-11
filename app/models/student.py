# this is the student model script
from dataclasses import dataclass

@dataclass
class Student:
    student_id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: str
    created_at: str
    updated_at: str