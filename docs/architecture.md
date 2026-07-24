# System Architecture

## Overview

The Academy Management System follows a **layered architecture** pattern, with clear separation between domain models, data access, business logic, and presentation.

```
┌──────────────────────────────────────────────────┐
│                   Presentation                    │
│              CLI (app/cli/)                       │
├──────────────────────────────────────────────────┤
│                 Business Logic                    │
│            Services (app/services/)               │
├──────────────────────────────────────────────────┤
│                  Data Access                      │
│         Repositories (app/repositories/)          │
├──────────────────────────────────────────────────┤
│                  Domain Model                     │
│            Models (app/models/)                   │
├──────────────────────────────────────────────────┤
│                 Infrastructure                    │
│   Database (app/database/)  │  Config (app/config/)│
│   Utils (app/utils/)                               │
└──────────────────────────────────────────────────┘
```

## Layer Descriptions

### 1. Domain Model (`app/models/`)

Pure Python dataclasses with no external dependencies. Each entity is self-contained and serializable. Models represent the core business concepts:

| Model | File | Purpose |
|-------|------|---------|
| `Student` | `student.py` | Registered learner profile |
| `Course` | `course.py` | Subject definition with topics |
| `Batch` | `batch.py` | Scheduled course instance |
| `Registration` | `registration.py` | Prospect admission workflow |
| `Enrollment` | `enrollment.py` | Student-to-batch linking |
| `AttendanceRecord` | `attendance.py` | Individual presence mark |
| `BatchSessionAttendance` | `attendance.py` | Per-session attendance summary |
| `Instructor` | `instructor.py` | Teaching staff profile |

### 2. Repositories (`app/repositories/`)

Data access layer providing CRUD operations for each entity. All repositories are **in-memory** by default, with optional JSON file persistence via the `Database` class. This design allows swapping the storage backend (e.g., SQLite, PostgreSQL) without changing business logic.

Each repository follows a consistent interface:
- `add_*()` / `create_*()` — Create new entity
- `get_*_by_id()` — Lookup by primary key
- `get_all_*()` — Retrieve all entities
- `update_*()` — Modify fields via `**kwargs`
- `delete_*()` / `remove_*()` / `deactivate_*()` — Remove or soft-delete

### 3. Services (`app/services/`)

Business logic orchestration layer. Services coordinate multiple repositories to implement workflows:

| Service | Responsibility |
|---------|---------------|
| `RegistrationService` | Prospect → Student → Enrollment pipeline; batch transfers |
| `EnrollmentService` | Enrollment lifecycle: enroll, pay, suspend, drop, complete |
| `AttendanceService` | Mark presence/absence; session summaries; absence queries |
| `ReportingService` | Aggregate reports: academy overview, student detail |

Services accept repository instances via **dependency injection** in their constructors, enabling testability and shared state.

### 4. CLI (`app/cli/`)

Interactive command-line interface providing menu-driven access to all system functions. Currently supports 8 operations: register student, add course, create batch, add instructor, enroll student, mark attendance, view overview, view student report.

## Data Flow

### Registration Workflow

```
CLI input
    │
    ▼
RegistrationService.register_student()
    │
    ├──▶ StudentRepository.find_student()     [check if exists]
    │
    ├──▶ StudentRepository.add_student()      [create new]  OR
    │    StudentRepository.update_student()   [update existing]
    │
    └──▶ EnrollmentRepository.enroll()        [if batch selected]
         BatchRepository.enroll_student()     [add to roster]
```

### Attendance Workflow

```
CLI input
    │
    ▼
AttendanceService.mark_student_present/absent()
    │
    └──▶ AttendanceRepository.mark_attendance()   [individual record]

AttendanceService.record_session_attendance()
    │
    └──▶ AttendanceRepository.create_session_attendance()  [roll-up]
         ◀── BatchRepository.get_batch_by_id()             [capacity data]
```

## Design Decisions

### Why dataclasses instead of ORM models?
- No external ORM dependency required for core domain
- Dataclasses are serializable, comparable, and type-safe
- Easy to convert to ORM models later (SQLAlchemy, Django)

### Why in-memory repositories?
- Fast development iteration without database setup
- All repositories share the same interface for future swapping
- JSON persistence via `Database` class provides optional durability

### Why `**kwargs` for updates?
- Flexible partial updates without requiring all fields
- Validation can be added at the service layer before reaching the repo
- Avoids "god methods" with 15 parameters for every update variant

### Why dependency injection for repositories?
- Services can share the same repository instance (single source of truth)
- Easy to swap real repos with mocks for testing
- No global state or singletons

## Future Architecture Considerations

1. **Database migration**: Replace in-memory repos with SQLite/PostgreSQL backends implementing the same interface
2. **Web API**: Add a FastAPI/Flask layer above services for REST access
3. **Authentication**: Add user/auth models for staff login and role-based access
4. **Event sourcing**: Track state changes via events for audit trails
5. **Async support**: Convert services to async for web framework compatibility
