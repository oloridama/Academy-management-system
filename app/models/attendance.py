# attendance model
from dataclasses import dataclass

@dataclass
class Attendance:
    first_name: str # name could be student or academic staff
    last_name: str
    days_present: int = 0
    days_absent: int