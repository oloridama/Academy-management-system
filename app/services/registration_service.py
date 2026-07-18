# This is the business workflow script that handles registration service for the business
from app.repositories.attendance_repository import StudentRepository

class RegistrationService:
    def __init__(self, batches=None):
        # If registration is opening to prospects then the available batches 
        # Should be in the constructor to be accessed later for enrolling the student into a batch
        # So we create the batches and keep them in a list of batches
        self.batches = batches if batches is not None else []

    # student registration entails a number of process which includes:
    # checking if the prospect is already a student so as not to register multiple account profiles
    # 
    def register_student(
            self,
            firstname,
            lastname,
            dob,
            gender,
            email,
            phone,
            emergency_contact,
            background,
            passport,
            student_id: str = "",
            selected_batch: str = "",
        ):
        if StudentRepository.find_student(firstname=firstname, lastname=lastname, student_id=student_id) == False:
            # then we create a new student profile
            new_student = StudentRepository.add_student(
                firstname=firstname,
                lastname=lastname,
                gender=gender,
                dob=dob,
                email=email,
                phone=phone,
                background=background,
                passport=passport,
                emergency=emergency_contact,
            )
        # prospect is a former student and has a profile in the system,
        # we can update their profile with new information
        # Update logic: Package the exact keys the repo expects
        update_data = {
            "student_id": student_id,
            "first_name": firstname,
            "last_name": lastname,
            "gender": gender,
            "email": email,
            "phone": phone,
            "emergency_contact": emergency_contact,
            "educational_background": background,
            "date_of_birth": dob,
            "passport_photograph": passport
        }
        new_student = StudentRepository.update_student(student_id=student_id, **update_data)

        # check if the student selected the selected batch and enroll the student into the batch
        if selected_batch:
            # enroll the student into the selected batch
            batch = next((b for b in self.batches if b.batch_id == selected_batch), None)
            if batch:
                # enroll the student into the batch
                batch.enroll_student(new_student)
            else:
                raise ValueError(f"Batch with ID {selected_batch} not found.")
                print("Check if the batch id is correct. If correct, create batch first! ")

        

