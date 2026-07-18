This document summarizes the domain associated with the academy we are building the software for.

**Student**
A student is an object that exists because they are the reason the academy exists to pass knowledge.
Student should own these: Student ID, Full Name, Date of birth, Gender, Address, Phone Number, Email, Emergency Contact, Educational Background, Passport Photograph, Registration Date, Status(Active, Suspended, Graduated). These information define the student and if changed they alter the state of the student object.

**Course**
A course is subject to be taught in a batch, comprising a body of knowlege a student is interested in. It mainly comprises of topics to be taught and a general name for the whole e.g python programming.

**Batch**
A batch is an instance of a course. It has a start date and an assocaitive end date. It owns batch id, schedule, capacity, status(Upcoming, Active, Completed).

**Registration**
A potential student goes through the process of becoming a student by providing the relevant information to be processed to become a student. The process is completed by being processed into at least a batch and stored in the admissions records. It owns data like application date, admission officer, requested batch, registration status, prospect information, payment status, registration id.

**Enrollment**
Enrollment is the process of registering for a course. When a student enrolls to a course batch, they have to pay; so payment status belongs here. Since a student can transfer enrollement or pause their study; enrollment should have a completion status.