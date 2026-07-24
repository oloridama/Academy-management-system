# Design Assumptions

This document captures the key assumptions made during the design and implementation of the Academy Management System. These assumptions guide development decisions and should be revisited as requirements evolve.

## Domain Assumptions

### 1. Student Identity
- A student is uniquely identified by their `student_id` (format: `ST####`).
- Name matching (first + last) is case-insensitive but treated as a secondary lookup — the primary key is always the ID.
- A student can have multiple enrollments across different batches but only **one active enrollment** at a time.

### 2. Registration vs. Student
- A **Prospect** is a person who has shown interest but has not completed registration.
- A **Registration** captures the admission process: prospect data, admission officer, selected batch, and payment status.
- Once registration is complete, the prospect becomes a **Student** with a permanent `student_id`.
- If a prospect is already a student (returning learner), the registration process updates their existing profile rather than creating a duplicate.

### 3. Course and Batch Relationship
- A **Course** is the abstract subject definition (name, topics, duration).
- A **Batch** is a concrete scheduled delivery of a course with dates, capacity, instructors, and enrolled students.
- A course can have multiple batches running concurrently or sequentially.
- Batch capacity is a hard limit — enrollment is rejected if full.

### 4. Enrollment Lifecycle
- Enrollment statuses form a state machine: `active` → `suspended` (can resume) or `dropped` (permanent exit) or `completed` (graduated).
- Payment status is tracked separately from completion status: `unpaid` → `paid` → `refunded`.
- A student can transfer between batches: the old enrollment is suspended, and a new one is created in the target batch.

### 5. Attendance Model
- Attendance is recorded per person per date per batch — not per course.
- Both students and instructors have attendance tracked.
- A `BatchSessionAttendance` is a roll-up record for a single class session, with `students_absent` calculated dynamically from `total_enrolled - len(present_student_ids)`.
- Dates are stored as ISO 8601 strings (`YYYY-MM-DD`) for universal compatibility.

## Technical Assumptions

### 6. Storage
- The default storage is **in-memory** (lists in repository classes).
- The `Database` class provides optional JSON file persistence but is not integrated by default.
- No database server is required to run the application.

### 7. ID Generation
- Student IDs: `ST` + random 4-digit number with collision detection via a used-IDs set.
- Instructor IDs: `INST` + sequential counter (`INST0001`, `INST0002`, ...).
- Enrollment IDs: `ENR` + sequential counter.
- These schemes prioritize simplicity over global uniqueness. For a production system, UUIDs or database-generated IDs would be preferable.

### 8. No Authentication
- There is no user authentication or role-based access control.
- The CLI assumes a single operator (admission officer, administrator).
- This is a conscious simplification for the current scope.

### 9. Single-User CLI
- The CLI is synchronous and single-user.
- No concurrent access concerns are addressed.
- Data consistency relies on sequential operations.

### 10. Image Handling
- Student passport photographs are stored as file path strings, not binary data.
- PIL/Pillow is listed as an optional dependency for future image processing but is not required to run the core system.

## Business Rule Assumptions

### 11. Batch Status Transitions
- Batches progress: `upcoming` → `active` → `completed`.
- Status transitions are manual (no automatic date-based activation).
- A batch cannot accept enrollments once `active` or `completed` (enforced at the service layer).

### 12. Payment Tracking
- Payment status is tracked per enrollment (`unpaid`/`paid`/`refunded`), not at the registration level.
- No payment amounts, methods, or transaction IDs are stored — this is a simplified model.

### 13. Instructor Assignment
- Instructors are assigned to courses, not directly to batches.
- An instructor can teach multiple courses.
- Instructor deactivation does not cascade to batch assignments.

### 14. Reporting
- Reports are generated from current in-memory state.
- No historical snapshots or time-series data are maintained.
- The `AcademyOverview` is a point-in-time summary.

## Known Limitations

1. **No data persistence by default** — restarting the application loses all data unless the `Database` class is integrated into repositories.
2. **No date validation** — dates are accepted as strings without format enforcement at the model level.
3. **No email/phone format validation** — contact fields accept any string.
4. **No duplicate student detection by email** — only name + ID matching prevents duplicates.
5. **No calendar/scheduling logic** — the `AttendanceService` does not validate that a date falls within a batch's schedule or term dates.
