# This script is for defining functions for the student data model
from app.models.student import Student


class StudentRepository:
    def __init__(self, student: type[Student]):
        self.student = student
        self.students = []

# Add student
    def add_student(
            self,
            firstname,
            lastname,
            dob,
            email,
            phone
        ) -> Student:
        """
        This creates a student profile
        Add the profile to student list
        And return the student class object
        """
        id = firstname[0] + lastname[0] + "00"

        # Fill the student object attributes
        self.student.first_name = firstname
        self.student.last_name = lastname
        self.student.date_of_birth = dob
        self.student.email = email
        self.student.phone = phone
        self.student.student_id = id

        # Save student to students list
        self.students.append(self.student)
        return self.student

    # method for getting student id
    def get_student_id(
            self, 
            firstname,
            lastname
        ):
        """
        search for student id and return it
        """
        id = ""
        for i in range(self.students):
            first_name = self.students[i].first_name
            last_name = self.students[i].last_name
            if first_name == firstname and last_name == lastname:
                id = self.students[i].student_id
                break
        
        return id
    
    def get_all_students(self):
        return self.students
    
    # Some students may no longer be active in the system
    # So remove them
    def deactivate_student(self, name):
        """
        Find and delete inactive student
        """
        name_list = name.split(" ")
        first_name = name_list[0]
        last_name = name_list[1]
        for student in self.students:
            if student.last_name == last_name and student.first_name == first_name:
                self.students.remove(student)
                break
