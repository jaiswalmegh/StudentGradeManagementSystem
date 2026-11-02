
import re


class Validators:

    @staticmethod
    def is_empty(value):
        """Check whether a value is empty or contains only spaces."""

        return value is None or str(value).strip() == ""

    @staticmethod
    def validate_name(name):
        """Validate a person's name."""

        if Validators.is_empty(name):
            return False, "Name is required."

        name = str(name).strip()

        if len(name) < 2:
            return False, "Name must contain at least 2 characters."

        if len(name) > 100:
            return False, "Name cannot exceed 100 characters."

        if not re.fullmatch(r"[A-Za-z][A-Za-z .'-]*", name):
            return False, "Name contains invalid characters."

        return True, "Valid name."

    @staticmethod
    def validate_email(email):
        """Validate an email address. Empty email is allowed."""

        if Validators.is_empty(email):
            return True, "Email is optional."

        email = str(email).strip()

        if len(email) > 150:
            return False, "Email cannot exceed 150 characters."

        pattern = (
            r"^[A-Za-z0-9._%+-]+"
            r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        if not re.fullmatch(pattern, email):
            return False, "Please enter a valid email address."

        return True, "Valid email."

    @staticmethod
    def validate_roll_number(roll_number):
        """Validate a student's roll number."""

        if Validators.is_empty(roll_number):
            return False, "Roll number is required."

        roll_number = str(roll_number).strip()

        if len(roll_number) > 30:
            return False, "Roll number cannot exceed 30 characters."

        if not re.fullmatch(r"[A-Za-z0-9/_-]+", roll_number):
            return False, "Roll number contains invalid characters."

        return True, "Valid roll number."

    @staticmethod
    def validate_subject_code(subject_code):
        """Validate a subject code."""

        if Validators.is_empty(subject_code):
            return False, "Subject code is required."

        subject_code = str(subject_code).strip()

        if len(subject_code) > 20:
            return False, "Subject code cannot exceed 20 characters."

        if not re.fullmatch(r"[A-Za-z0-9_-]+", subject_code):
            return False, "Subject code contains invalid characters."

        return True, "Valid subject code."

    @staticmethod
    def validate_class_name(class_name):
        """Validate a class or programme name."""

        if Validators.is_empty(class_name):
            return False, "Class name is required."

        class_name = str(class_name).strip()

        if len(class_name) > 100:
            return False, "Class name cannot exceed 100 characters."

        if not re.fullmatch(r"[A-Za-z0-9 &()_./-]+", class_name):
            return False, "Class name contains invalid characters."

        return True, "Valid class name."

    @staticmethod
    def validate_section(section):
        """Validate a section. Empty section is allowed."""

        if Validators.is_empty(section):
            return True, "Section is optional."

        section = str(section).strip()

        if len(section) > 20:
            return False, "Section cannot exceed 20 characters."

        if not re.fullmatch(r"[A-Za-z0-9_-]+", section):
            return False, "Section contains invalid characters."

        return True, "Valid section."

    @staticmethod
    def validate_positive_number(value, field_name="Value"):
        """Validate a number greater than zero."""

        try:
            number = float(value)
        except (TypeError, ValueError):
            return False, f"{field_name} must be a valid number."

        if number <= 0:
            return False, f"{field_name} must be greater than zero."

        return True, f"Valid {field_name.lower()}."

    @staticmethod
    def validate_marks(marks, maximum_marks):
        """Validate obtained marks against maximum marks."""

        try:
            marks = float(marks)
            maximum_marks = float(maximum_marks)
        except (TypeError, ValueError):
            return False, "Marks must be valid numbers."

        if maximum_marks <= 0:
            return False, "Maximum marks must be greater than zero."

        if marks < 0:
            return False, "Marks cannot be negative."

        if marks > maximum_marks:
            return False, (
                f"Marks cannot exceed {maximum_marks:g}."
            )

        return True, "Valid marks."

    @staticmethod
    def validate_academic_session(session):
        """Validate an academic session such as 2026-27."""

        if Validators.is_empty(session):
            return False, "Academic session is required."

        session = str(session).strip()

        if not re.fullmatch(r"\d{4}-\d{2}", session):
            return False, "Use academic session format YYYY-YY."

        start_year = int(session[:4])
        end_year = int(session[5:])

        if end_year != (start_year + 1) % 100:
            return False, "Invalid academic session."

        return True, "Valid academic session."

    @staticmethod
    def validate_exam_type(exam_type):
        """Validate an examination type."""

        if Validators.is_empty(exam_type):
            return False, "Exam type is required."

        if len(str(exam_type).strip()) > 50:
            return False, "Exam type cannot exceed 50 characters."

        return True, "Valid exam type."
