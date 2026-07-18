# This script is for defining functions for the student data model
from app.models.student import Student
import random


class StudentRepository:
    def __init__(self, student: type[Student]):
        self.student = student
        self.students = []
        # the purpose of this is to map an id 
        # created by student id generator to a student name 
        # thereby preventing the creation of duplicate ids for multiple students
        self.students_id = {}   

# Add student
    def add_student(
            self,
            firstname,
            lastname,
            gender,
            dob,
            email,
            phone,
            background,
            passport,
            emergency,
        ) -> Student:
        """
        This creates a student profile,
        add the profile to student list
        and return the student class object
        """
        # create student id for new student
        student_id = self.generate_new_id()
        # map the student id to the student name
        self.students_id[student_id] = firstname + " " + lastname        

        # Fill the student object attributes
        self.student = {
            "student_id": student_id,
            "first_name": firstname,
            "last_name": lastname,
            "gender": gender,
            "email": email,
            "phone": phone,
            "emergency_contact": emergency,
            "educational_background": background,
            "date_of_birth": dob,
            "passport_photograph": passport


        }

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
    
    def generate_new_id(self):
        """
        Generate a new unique student ID
        """
        # student ids must start with "ST" concatenated to a generated random 4 digit number
        # generate an integer from 0 to 9999
        num = random.randint(0, 9999)

        # format it to a string, padding with zeros if its less than 4 digits
        id = f"ST{num:04d}"
        # check if id has been used before
        for student_id in self.students_id:
            if student_id == id:
                # if it has been used, generate a new one
                return self.generate_new_id()

        return id
    
    def find_student(
            self,
            firstname,
            lastname,
            student_id
        ) -> bool:
        """
        Find a student by their first name, last name, and student ID
        """
        # seperate the name by whitespace to derive 
        # the firstname and lastname since they are stored as fullname
        name = self.students_id[id].split(" ")
        first_name = name[0]
        last_name = name[1]

        # find the student id in the mapping of student_id -> fullname
        for id in self.students_id:
            if id == student_id and first_name == firstname and last_name == lastname:
                return True
            else:
                return False
            
    def update_student(self, student_id, **kwargs):
        """
        Updates the student profile with new information
        """
        # New info could be anything, ranging from a changed address, phone number, email, etc.
        # We will check against all the info provided by the user for changes and update the student profile accordingly
        # First find the student by their ID
        for student in self.students:
            # Use dictionary key lookup
            if student.get("student_id") == student_id:

                # Now we will check for changes in the provided info
                for key, value in kwargs.items():
                    # Check if key exists in the typedict and update it
                    if key in student:
                        student[key] = value
                break

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
