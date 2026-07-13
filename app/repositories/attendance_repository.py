# This script is for defining functions for the attendance model
from app.models.attendance import Attendance
from app.repositories.student_repository import StudentRepository
from app.repositories.instructor_repository import InstructorRepository
from dataclasses import dataclass

@dataclass
class Date:
    year: str = ""
    month: str = ""
    day: int = 00

# months is a constant with the names of the months as keys to access their number of days
MONTHS = {
    "january": 31,
    "february": 28 or 29,
    "march": 31,
    "april": 30,
    "may": 31,
    "june": 30,
    "july": 31,
    "august": 31,
    "september": 30,
    "october": 31,
    "november": 30,
    "december": 31
}

class AttendanceRepository:
    def __init__(
            self, 
            attendance: type[Attendance], 
            day, 
            month, 
            year, 
            session_days: int, 
            breaks: list[Date], 
            general_calender: list[Date]
    ):
        # Initialize school session days depending on region in __init__ constructor
        self.valid_days = session_days

        # Take the school breaks list and remove the dates from the general calender
        # to create the list of valid school dates
        self.calender_list = general_calender
        for break_date in breaks:
            for date in self.calender_list:
                if break_date == date:
                    self.calender_list.remove(date)

        #Instantiate student repository to get access to the students list
        students = StudentRepository()
        instructors = InstructorRepository()
        self.date = Date(year=year, month=month, day=day)

        students_list = students.students
        instructor_list = instructors.tutors

        self.attendance = attendance
        self.attendance.days_absent = self.valid_days - self.attendance.days_present
        self.instructors = instructor_list
        self.students = students_list

        #Attendance list should have a tutors session alongside a students session under a date
        self.attendance_list: dict[Date, dict[str, dict[str, int]]] = {} # {"date": {"tutors": [{"name1": 0}, {"name2": 0}], "students": [{"name1": 0}, "name2": 0]}}
        
        # warm start up for the attendance list
        self.attendance_list[self.date] = {
            "tutor": {instructor: 0 for instructor in self.instructors},
            "students": {student: 0 for student in self.students}
        }
    # Attendance has the names of students and academic(tutors) 
    # Everyone checks in under the present day in the week
    # Not checking in at the end of the day equals absent
    def mark_person_attendance(
            self,
            role: str,
            firstname: str,
            lastname: str,
        ):
        """
        Uses self.date to automatically find the right records
        Role: 'students' or 'tutors'
        """
        # Find person in self.attendance_list which is a dict
        if self.attendance_list[self.date][role] == "tutor":
            # self.attendance_list[self.date]["tutor"] is a list of dict 
            # That contains a dataclass object for each key
            for individual in self.attendance_list[self.date]["tutor"]:
                # individual is not a dict but a dataclass object
                if individual.first_name == firstname and individual.last_name == lastname:
                    self.atttendance_list[self.date]["tutor"][individual] += 1
                    print("Attendance marked for today!")
        for individual in self.attendance_list[self.date]["students"]:
            if individual.first_name == firstname and individual.last_name == lastname:
                self.attendance_list[self.date]["students"][individual] += 1
                print("Attendance marked for today!")

        # Increase attendance number by 1
        self.attendance.days_present += 1        
        

    def get_days_absent(self, firstname, lastname):
        """
        Uses and individual's name to check their attendance record
        Absent days = Total number of school days - days present
        """
        absent_days = 0
        if self.attendance.first_name == firstname and \
            self.attendance.last_name == lastname:
            absent_days = self.attendance.days_absent

        return absent_days
        
    def get_absent_dates(
            self,
            role,
            firstname,
            lastname,
    ):
        """
        Uses an individual's name to check their attendance record for dates absent
        """
        # We can get this by initializing a school calender for valid dates in the constructor
        # We check the dates that the student didn't mark attendance and return them in a list
        calender = self.get_calender_year()
        # loop through self.attendance list, for any name 0 = absent and 1 = present
        absent_dates = []
        for date in self.attendance_list:
            if self.attendance_list[date][role] == "tutor":
                for individual in self.attendance_list[date]["tutor"]:
                    if self.attendance_list[date]["tutor"][individual] == 0:
                        if individual.first_name == firstname and \
                            individual.last_name == lastname:
                            absent_dates.append(date)

        return absent_dates

    # Create a helper function for school calender,     
    def get_calender_year(self):
        return self.calender_list