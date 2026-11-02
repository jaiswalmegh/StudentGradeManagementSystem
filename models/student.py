
from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:

    roll_number: str
    name: str
    class_name: str
    email: Optional[str] = None
    section: Optional[str] = None
    student_id: Optional[int] = None

    def validate(self):

        if not self.roll_number.strip():
            raise ValueError("Roll number is required.")

        if not self.name.strip():
            raise ValueError("Student name is required.")

        if not self.class_name.strip():
            raise ValueError("Class name is required.")

        if self.email and "@" not in self.email:
            raise ValueError("Enter a valid email address.")

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "roll_number": self.roll_number.strip(),
            "name": self.name.strip(),
            "email": self.email.strip() if self.email else None,
            "class_name": self.class_name.strip(),
            "section": self.section.strip() if self.section else None
        }

    @classmethod
    def from_row(cls, row):

        if row is None:
            return None

        return cls(
            student_id=row["student_id"],
            roll_number=row["roll_number"],
            name=row["name"],
            email=row["email"],
            class_name=row["class_name"],
            section=row["section"]
        )
