# models the enrollment of a student
from dataclasses import dataclass

@dataclass
class Enrollment:
    first_name: str 
    last_name: str 
    date_of_birth: str 
    email: str
    transfer: bool        # true if transferring from another school
    level: str
    guardian: str
