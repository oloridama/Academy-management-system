# Academy Management System

A Python-based management system for educational academies that handles student registration, course enrollment, attendance tracking, and reporting.

## Overview

The Academy Management System provides an end-to-end solution for managing the day-to-day operations of an educational institution. It covers the full student lifecycle — from prospect inquiry through registration, enrollment in course batches, attendance tracking, and graduation.

## Features

- **Student Registration** — Capture prospect information and convert prospects into registered students with full profile management.
- **Course & Batch Management** — Define courses with topics and schedule them into batches with capacity limits, instructors, and status tracking (Upcoming → Active → Completed).
- **Enrollment** — Enroll students into specific course batches with payment status tracking and support for transfers and pauses.
- **Attendance Tracking** — Record daily attendance for students and instructors per batch class session.
- **Instructor Management** — Maintain instructor profiles, qualifications, and course assignments.
- **Reporting** — Generate institution-wide reports on admissions, enrollment, and attendance.

## Domain Model

| Entity | Description |
|--------|-------------|
| **Student** | A registered learner with personal details, educational background, and status (Active, Suspended, Graduated) |
| **Course** | A subject of study (e.g., Python Programming) with a list of topics |
| **Batch** | A scheduled instance of a course with start/end dates, capacity, and instructors |
| **Registration** | The admission process: capturing a prospect's information and creating their student record |
| **Enrollment** | A student's enrollment in a specific batch with payment and completion status |
| **Attendance** | Daily presence record for students and instructors in a batch class session |
| **Instructor** | A teaching staff member with qualifications and assigned courses |

For detailed domain definitions, see [Ubiquitous Language](docs/ubiquitous-language.md) and [Domain Model](docs/domain-model.md).

## Project Structure

```
academy-management-system/
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── README.md
├── docs/
│   ├── architecture.md              # System architecture (TBD)
│   ├── assumptions.md               # Design assumptions (TBD)
│   ├── business-requirements.md     # Business workflows
│   ├── domain-model.md              # Domain entity definitions
│   └── ubiquitous-language.md       # Shared terminology
├── app/
│   ├── models/                      # Domain data models (dataclasses)
│   │   ├── student.py
│   │   ├── course.py
│   │   ├── batch.py
│   │   ├── enrollment.py
│   │   ├── registration.py
│   │   ├── attendance.py
│   │   ├── instructor.py
│   │   └── date.py
│   ├── repositories/                # Data access layer
│   │   ├── student_repository.py
│   │   ├── course_repository.py
│   │   ├── batch_repository.py
│   │   ├── enrollment_repository.py
│   │   ├── attendance_repository.py
│   │   └── instructor_repository.py
│   ├── services/                    # Business logic layer
│   │   ├── attendance_service.py
│   │   ├── enrollment_service.py
│   │   ├── registration_service.py
│   │   └── reporting_service.py
│   ├── cli/                         # Command-line interface (TBD)
│   ├── config/                      # Application configuration (TBD)
│   ├── database/                    # Database layer (TBD)
│   └── utils/                       # Utility functions (TBD)
└── tests/                           # Test suite (TBD)
```

## Architecture

The system follows a layered architecture:

```
┌─────────────────────────────┐
│         CLI / UI            │  ← User interface layer
├─────────────────────────────┤
│        Services             │  ← Business logic orchestration
├─────────────────────────────┤
│       Repositories          │  ← Data access & persistence
├─────────────────────────────┤
│         Models              │  ← Domain entities (dataclasses)
└─────────────────────────────┘
```

- **Models** — Pure Python dataclasses representing domain entities (Student, Course, Batch, etc.)
- **Repositories** — Handle data persistence operations (create, read, update, delete) for each entity
- **Services** — Orchestrate business workflows by coordinating multiple repositories (e.g., `RegistrationService` uses both `StudentRepository` and `EnrollmentRepository`)
- **CLI/UI** — User-facing interface layer (currently under development)

## Business Workflows

### Admission & Registration
1. A prospect contacts the academy and is briefed on requirements
2. An admission officer captures the prospect's details via the registration form
3. The prospect selects a desired course batch
4. Upon completion, the prospect becomes a registered **Student**

### Enrollment
1. A registered student is enrolled into a specific batch
2. Payment status is recorded
3. Enrollment status tracks progress (Active, Suspended, Graduated)
4. Students can transfer batches or pause their enrollment

### Attendance
1. Each class session within a batch has an attendance record
2. Both students and instructors are tracked for presence
3. Absentee counts are calculated dynamically from batch capacity

## Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd academy-management-system

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
# Run the application
python main.py
```

## Dependencies

- **Pillow (PIL)** — Image handling for student passport photographs

Additional dependencies will be added as the database layer and CLI are implemented.

## Development Status

| Component | Status |
|-----------|--------|
| Domain Models | ✅ Implemented |
| Repositories | 🚧 In Progress |
| Services | 🚧 In Progress |
| CLI | ⬜ Planned |
| Database Layer | ⬜ Planned |
| Configuration | ⬜ Planned |
| Tests | ⬜ Planned |

## Documentation

- [Business Requirements](docs/business-requirements.md) — Day-to-day business operations
- [Domain Model](docs/domain-model.md) — Entity definitions and relationships
- [Ubiquitous Language](docs/ubiquitous-language.md) — Shared terminology glossary
- [Architecture](docs/architecture.md) — System design (TBD)
- [Assumptions](docs/assumptions.md) — Design decisions and assumptions (TBD)

## License

This project is unlicensed. All rights reserved.
