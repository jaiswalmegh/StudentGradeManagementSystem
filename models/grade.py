
from dataclasses import dataclass
from typing import Optional


@dataclass
class Grade:

    student_id: int
    subject_id: int
    marks_obtained: float
    exam_type: str
    academic_session: str
    grade_id: Optional[int] = None

    def validate(self, max_marks=None):

        if self.student_id <= 0:
            raise ValueError("Invalid student ID.")

        if self.subject_id <= 0:
            raise ValueError("Invalid subject ID.")

        if self.marks_obtained < 0:
            raise ValueError("Marks cannot be negative.")

        if max_marks is not None:
            if self.marks_obtained > max_marks:
                raise ValueError(
                    f"Marks cannot exceed {max_marks}."
                )

        if not self.exam_type.strip():
            raise ValueError("Exam type is required.")

        if not self.academic_session.strip():
            raise ValueError("Academic session is required.")

    def to_dict(self):

        return {
            "grade_id": self.grade_id,
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "marks_obtained": self.marks_obtained,
            "exam_type": self.exam_type.strip(),
            "academic_session": self.academic_session.strip()
        }

    @classmethod
    def from_row(cls, row):

        if row is None:
            return None

        return cls(
            grade_id=row["grade_id"],
            student_id=row["student_id"],
            subject_id=row["subject_id"],
            marks_obtained=row["marks_obtained"],
            exam_type=row["exam_type"],
            academic_session=row["academic_session"]
        )
