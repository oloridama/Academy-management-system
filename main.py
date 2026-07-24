"""Academy Management System — Application entry point.

Usage:
    python main.py              # Launch interactive CLI
    python main.py --demo       # Run a demonstration with sample data
    python main.py --overview   # Print academy overview and exit
"""
import sys
from app.cli import CLI


def run_demo() -> None:
    """Seed the system with sample data and print the overview."""
    from app.repositories.student_repository import StudentRepository
    from app.repositories.instructor_repository import InstructorRepository
    from app.repositories.course_repository import CourseRepository
    from app.repositories.batch_repository import BatchRepository
    from app.repositories.enrollment_repository import EnrollmentRepository
    from app.repositories.attendance_repository import AttendanceRepository
    from app.services.registration_service import RegistrationService
    from app.services.enrollment_service import EnrollmentService
    from app.services.attendance_service import AttendanceService
    from app.services.reporting_service import ReportingService

    # Shared repositories (single source of truth)
    student_repo = StudentRepository()
    instructor_repo = InstructorRepository()
    course_repo = CourseRepository()
    batch_repo = BatchRepository()
    enrollment_repo = EnrollmentRepository()
    attendance_repo = AttendanceRepository()

    # Services (all sharing the same repos)
    registration = RegistrationService(
        student_repo=student_repo,
        enrollment_repo=enrollment_repo,
        batch_repo=batch_repo,
    )
    enrollment = EnrollmentService(
        enrollment_repo=enrollment_repo,
        batch_repo=batch_repo,
    )
    attendance = AttendanceService(
        attendance_repo=attendance_repo,
        batch_repo=batch_repo,
    )
    reporting = ReportingService(
        student_repo=student_repo,
        instructor_repo=instructor_repo,
        course_repo=course_repo,
        batch_repo=batch_repo,
        enrollment_repo=enrollment_repo,
        attendance_repo=attendance_repo,
    )

    print("Seeding demo data...\n")

    # Create courses
    py_course = course_repo.add_course(
        course_id="CRS001",
        name="Python Programming",
        description="Learn Python from basics to advanced topics.",
        topics=["Variables", "Control Flow", "Functions", "OOP", "Modules"],
        duration_weeks=12,
        category="Programming",
    )
    js_course = course_repo.add_course(
        course_id="CRS002",
        name="Web Development",
        description="Full-stack web development with HTML, CSS, and JavaScript.",
        topics=["HTML", "CSS", "JavaScript", "React", "Node.js"],
        duration_weeks=16,
        category="Programming",
    )
    print(f"Courses: {py_course.name}, {js_course.name}")

    # Create instructors
    inst1 = instructor_repo.add_instructor(
        first_name="John",
        last_name="Smith",
        email="john.smith@academy.com",
        phone="+1234567890",
        qualification="PhD Computer Science",
        courses=["CRS001"],
    )
    inst2 = instructor_repo.add_instructor(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@academy.com",
        phone="+1234567891",
        qualification="MSc Web Technologies",
        courses=["CRS002"],
    )
    print(f"Instructors: {inst1.full_name}, {inst2.full_name}")

    # Create batches
    batch1 = batch_repo.create_batch(
        batch_id="BATCH001",
        course_id="CRS001",
        course_name="Python Programming",
        start_date="2026-08-01",
        end_date="2026-10-31",
        capacity=20,
        schedule="Mon/Wed/Fri 9:00-11:00",
        instructors=["INST0001"],
        status="upcoming",
    )
    batch2 = batch_repo.create_batch(
        batch_id="BATCH002",
        course_id="CRS002",
        course_name="Web Development",
        start_date="2026-08-15",
        end_date="2026-12-15",
        capacity=15,
        schedule="Tue/Thu 14:00-17:00",
        instructors=["INST0002"],
        status="upcoming",
    )
    print(f"Batches: {batch1.batch_id}, {batch2.batch_id}")

    # Register students
    s1 = registration.register_student(
        firstname="Alice",
        lastname="Johnson",
        dob="2000-05-15",
        gender="female",
        email="alice@example.com",
        phone="+1111111111",
        emergency_contact="+1111111112",
        background="High School Diploma",
        selected_batch_id="BATCH001",
    )
    s2 = registration.register_student(
        firstname="Bob",
        lastname="Williams",
        dob="1999-11-22",
        gender="male",
        email="bob@example.com",
        phone="+2222222221",
        emergency_contact="+2222222222",
        background="Bachelor's Degree",
        selected_batch_id="BATCH001",
    )
    s3 = registration.register_student(
        firstname="Charlie",
        lastname="Brown",
        dob="2001-03-08",
        gender="male",
        email="charlie@example.com",
        phone="+3333333331",
        emergency_contact="+3333333332",
        background="Self-taught",
        selected_batch_id="BATCH002",
    )
    print(f"Students: {s1.full_name}, {s2.full_name}, {s3.full_name}")

    # Mark some attendance
    attendance.mark_student_present(
        first_name="Alice", last_name="Johnson",
        date="2026-08-03", batch_id="BATCH001",
    )
    attendance.mark_student_present(
        first_name="Bob", last_name="Williams",
        date="2026-08-03", batch_id="BATCH001",
    )
    attendance.mark_student_absent(
        first_name="Alice", last_name="Johnson",
        date="2026-08-05", batch_id="BATCH001",
    )
    attendance.mark_student_present(
        first_name="Bob", last_name="Williams",
        date="2026-08-05", batch_id="BATCH001",
    )
    attendance.record_session_attendance(
        date="2026-08-03",
        batch_id="BATCH001",
        lesson_topic="Variables and Control Flow",
        present_student_ids=[s1.student_id, s2.student_id],
    )
    print("Attendance recorded.\n")

    # Print overview
    reporting.print_overview()


def main() -> None:
    """Application entry point."""
    if "--demo" in sys.argv:
        run_demo()
    elif "--overview" in sys.argv:
        from app.services.reporting_service import ReportingService
        ReportingService().print_overview()
    else:
        cli = CLI()
        cli.run()


if __name__ == "__main__":
    main()
