# This repository script handles the batch processing of the academy
from app.models.batch import Batch

class BatchRepository:
    def __init__(self):
        self.batches = []

    @staticmethod
    def create_batch(
        self,
        batch_id,
        course_name,
        start_date,
        end_date,
        capacity,
        enrolled_students,
        instructors,
        status
    ):
        # Returns a structured batch object based on the provided parameters
        batch =  Batch(
            batch_id=batch_id,
            course_name=course_name,
            start_date=start_date,
            end_date=end_date,
            capacity=capacity,
            enrolled_students=enrolled_students,
            instructors=instructors,
            status=status
        )

        self.batches.append(batch)
        return batch