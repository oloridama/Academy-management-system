# repo for processing instructor
from app.models.instructor import Instructor

class InstructorRepository:
    """
    Process the instructor dataclass object and list of instructors
    """
    def __init__(self, tutor: type[Instructor]):
        self.tutor = tutor
        self.tutors = []

    # Add student
    def add_instructor(
            self,
            name,
            dob,
            email,
            phone
        ):
        """
        This creates an instructor profile
        """
        # Name will be recieved as a whole but split with a space
        # Use the split method to create a list of the first name and last name
        name_list = name.split(" ")
        first_name = name_list[0]
        last_name = name_list[1]
        id = first_name[0] + last_name[0] + "00"

        # Fill the student object attributes
        self.tutor.first_name = first_name
        self.tutor.last_name = last_name
        self.tutor.date_of_birth = dob
        self.tutor.email = email
        self.tutor.phone = phone
        self.tutor.instructor_id = id

        # Save student to students list
        self.tutors.append(self.tutor)

    # method for getting student id
    def get_instructor_id(self, name):
        """
        search for student id and return it
        """
        id = ""
        for i in range(self.tutors):
            if self.tutors[i].name == name:
                id = self.tutors[i].instructor_id
                break
        
        return id
    
    def get_all_instructors(self):
        return self.tutors
    
    # An instructor may resign or is fired
    # So remove them
    def deactivate_instructor(self, name):
        """
        Find and delete inactive student
        """
        name_list = name.split(" ")
        first_name = name_list[0]
        last_name = name_list[1]
        for tutor in self.tutors:
            if tutor.last_name == last_name and tutor.first_name == first_name:
                self.tutors.remove(tutor)
                break