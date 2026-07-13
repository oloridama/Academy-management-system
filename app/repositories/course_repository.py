# process the course object structure
from app.models.course import Course

class CourseRepository:
    def __init__(self, course: type[Course]):
        self.course = course

    def add_new_course(
            self,
            name,
            category,
            duration,
            compulsory: str
    ) -> Course:
        self.course.name = name
        self.course.field = category
        self.course.duration = duration
        self.course.compulsory = True if compulsory == "yes" else False

        return self.course
        
    # Course is no longer part of curriculum   
    def delete_course(
            self,
            course_name,
            category_name
    ):
        categories = self.course.field
        for category, course_list in categories.items():
            if category == category_name:
                for course in course_list:
                    if course == course_name:
                        course_list.remove(course)