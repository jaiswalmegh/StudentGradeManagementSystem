
from dataclasses import dataclass
from typing import Optional


@dataclass
class Subject:

    subject_code: str
    subject_name: str
    max_marks: float = 100.0
    credits: float = 1.0
    subject_id: Optional[int] = None

    def validate(self):

        if not self.subject_code.strip():
            raise ValueError("Subject code is required.")

        if not self.subject_name.strip():
            raise ValueError("Subject name is required.")

        if self.max_marks <= 0:
            raise ValueError("Maximum marks must be greater than zero.")

        if self.credits <= 0:
            raise ValueError("Subject credits must be greater than zero.")

    def to_dict(self):

        return {
            "subject_id": self.subject_id,
            "subject_code": self.subject_code.strip(),
            "subject_name": self.subject_name.strip(),
            "max_marks": self.max_marks,
            "credits": self.credits
        }

    @classmethod
    def from_row(cls, row):

        if row is None:
            return None

        return cls(
            subject_id=row["subject_id"],
            subject_code=row["subject_code"],
            subject_name=row["subject_name"],
            max_marks=row["max_marks"],
            credits=row["credits"]
        )
