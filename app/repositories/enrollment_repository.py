# Enrollment processing script
from app.models.enrollment import Enrollment
from student_repository import StudentRepository


# This script 

class EnrollmentRepository:
    """
    Enroll the student into the academy by creating the student object
    """
    def __init__(self, enroll: type[Enrollment]):
        self.enroll = enroll

    def enroll_new_student(
        self,
        firstname,
        lastname,
        date_of_birth,
        email,
        phone,
        transfer: str,
        guardian,       
    ):
        process_student = StudentRepository()
        student = process_student.add_student(firstname, lastname, date_of_birth, email, phone)
        self.enroll.first_name = student.first_name
        self.enroll.last_name = student.last_name
        self.enroll.date_of_birth = student.date_of_birth
        self.enroll.email = student.email
        self.enroll.phone = student.phone
        self.enroll.transfer = True if transfer == "yes" else False
        self.enroll.guardian = guardian
     