"""Command-line interface for the Academy Management System."""
from app.repositories.student_repository import StudentRepository
from app.repositories.instructor_repository import InstructorRepository
from app.repositories.course_repository import CourseRepository
from app.repositories.batch_repository import BatchRepository
from app.services.registration_service import RegistrationService
from app.services.enrollment_service import EnrollmentService
from app.services.attendance_service import AttendanceService
from app.services.reporting_service import ReportingService


class CLI:
    """Interactive CLI for managing the academy system."""

    def __init__(self):
        # Repositories
        self.student_repo = StudentRepository()
        self.instructor_repo = InstructorRepository()
        self.course_repo = CourseRepository()
        self.batch_repo = BatchRepository()

        # Services
        self.registration_service = RegistrationService(
            student_repo=self.student_repo,
            batch_repo=self.batch_repo,
        )
        self.enrollment_service = EnrollmentService(
            batch_repo=self.batch_repo,
        )
        self.attendance_service = AttendanceService(
            batch_repo=self.batch_repo,
        )
        self.reporting_service = ReportingService(
            student_repo=self.student_repo,
            instructor_repo=self.instructor_repo,
            course_repo=self.course_repo,
            batch_repo=self.batch_repo,
        )

    def run(self) -> None:
        """Start the interactive CLI loop."""
        self._print_banner()
        while True:
            try:
                choice = self._show_menu()
                if choice == "0":
                    print("Goodbye!")
                    break
                self._handle_choice(choice)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

    def _print_banner(self) -> None:
        print("=" * 50)
        print("   ACADEMY MANAGEMENT SYSTEM")
        print("=" * 50)

    def _show_menu(self) -> str:
        print("\n── MAIN MENU ──")
        print("1.  Register a new student")
        print("2.  Add a course")
        print("3.  Create a batch")
        print("4.  Add an instructor")
        print("5.  Enroll student in batch")
        print("6.  Mark attendance")
        print("7.  View academy overview")
        print("8.  View student report")
        print("0.  Exit")
        return input("Choose an option: ").strip()

    def _handle_choice(self, choice: str) -> None:
        handlers = {
            "1": self._register_student,
            "2": self._add_course,
            "3": self._create_batch,
            "4": self._add_instructor,
            "5": self._enroll_student,
            "6": self._mark_attendance,
            "7": self._view_overview,
            "8": self._view_student_report,
        }
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Invalid option. Please try again.")

    def _register_student(self) -> None:
        print("\n── REGISTER STUDENT ──")
        firstname = input("First name: ").strip()
        lastname = input("Last name: ").strip()
        dob = input("Date of birth (YYYY-MM-DD): ").strip()
        gender = input("Gender: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        emergency = input("Emergency contact: ").strip()
        background = input("Educational background: ").strip()
        batch_id = input("Batch ID (leave blank to skip enrollment): ").strip()

        student = self.registration_service.register_student(
            firstname=firstname,
            lastname=lastname,
            dob=dob,
            gender=gender,
            email=email,
            phone=phone,
            emergency_contact=emergency,
            background=background,
            selected_batch_id=batch_id,
        )
        print(f"\nStudent registered! ID: {student.student_id}")

    def _add_course(self) -> None:
        print("\n── ADD COURSE ──")
        course_id = input("Course ID: ").strip()
        name = input("Course name: ").strip()
        description = input("Description: ").strip()
        duration = input("Duration (weeks): ").strip()
        category = input("Category: ").strip()
        topics_str = input("Topics (comma-separated): ").strip()
        topics = [t.strip() for t in topics_str.split(",")] if topics_str else []

        course = self.course_repo.add_course(
            course_id=course_id,
            name=name,
            description=description,
            topics=topics,
            duration_weeks=int(duration) if duration else 0,
            category=category,
        )
        print(f"\nCourse added! ID: {course.course_id} — {course.name}")

    def _create_batch(self) -> None:
        print("\n── CREATE BATCH ──")
        batch_id = input("Batch ID: ").strip()
        course_id = input("Course ID: ").strip()
        course_name = input("Course name: ").strip()
        start_date = input("Start date (YYYY-MM-DD): ").strip()
        end_date = input("End date (YYYY-MM-DD): ").strip()
        capacity = input("Capacity: ").strip()
        schedule = input("Schedule (e.g. Mon/Wed/Fri 9:00-11:00): ").strip()

        batch = self.batch_repo.create_batch(
            batch_id=batch_id,
            course_id=course_id,
            course_name=course_name,
            start_date=start_date,
            end_date=end_date,
            capacity=int(capacity) if capacity else 0,
            schedule=schedule,
        )
        print(f"\nBatch created! ID: {batch.batch_id} — {batch.course_name}")

    def _add_instructor(self) -> None:
        print("\n── ADD INSTRUCTOR ──")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        dob = input("Date of birth (YYYY-MM-DD): ").strip()
        qualification = input("Qualification: ").strip()

        instructor = self.instructor_repo.add_instructor(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=dob,
            qualification=qualification,
        )
        print(f"\nInstructor added! ID: {instructor.instructor_id}")

    def _enroll_student(self) -> None:
        print("\n── ENROLL STUDENT ──")
        student_id = input("Student ID: ").strip()
        batch_id = input("Batch ID: ").strip()

        enrollment = self.enrollment_service.enroll_student(student_id, batch_id)
        print(f"\nEnrolled! Enrollment ID: {enrollment.enrollment_id}")

    def _mark_attendance(self) -> None:
        print("\n── MARK ATTENDANCE ──")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()
        batch_id = input("Batch ID: ").strip()
        role = input("Role (student/instructor): ").strip().lower()
        present = input("Present? (y/n): ").strip().lower()

        is_present = present == "y"
        record = self.attendance_service.mark_student_present(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
        ) if is_present else self.attendance_service.mark_student_absent(
            first_name=first_name,
            last_name=last_name,
            date=date,
            batch_id=batch_id,
        )
        print(f"\nAttendance recorded! {'Present' if is_present else 'Absent'}")

    def _view_overview(self) -> None:
        print()
        self.reporting_service.print_overview()

    def _view_student_report(self) -> None:
        print("\n── STUDENT REPORT ──")
        student_id = input("Student ID: ").strip()
        try:
            report = self.reporting_service.get_student_report(student_id)
            s = report["student"]
            print(f"\nStudent: {s.full_name} ({s.student_id})")
            print(f"Status: {s.status}")
            print(f"Email: {s.email} | Phone: {s.phone}")
            print(f"\nEnrollments: {len(report['enrollments'])}")
            for e in report["enrollments"]:
                print(f"  - {e.enrollment_id}: Batch {e.batch_id} [{e.completion_status}]")
            print(f"\nAttendance: {report['days_present']} present, {report['days_absent']} absent")
        except ValueError as e:
            print(f"Error: {e}")
