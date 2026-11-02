
import sqlite3

from database.connection import (
    get_db,
    fetch_all,
    fetch_one
)

from models.grade import Grade
from database.connection import fetch_one as fetch_record


class GradeController:
    """
    Handles all grade and marks-related database operations.
    """

    @staticmethod
    def add_grade(grade):
        """Add a student's marks for a particular subject."""

        if not isinstance(grade, Grade):
            raise TypeError("Expected a Grade object.")

        subject = fetch_one("""
            SELECT max_marks
            FROM subjects
            WHERE subject_id = ?
        """, (grade.subject_id,))

        if subject is None:
            raise ValueError("Subject does not exist.")

        grade.validate(max_marks=subject["max_marks"])

        student = fetch_record("""
            SELECT student_id
            FROM students
            WHERE student_id = ?
        """, (grade.student_id,))

        if student is None:
            raise ValueError("Student does not exist.")

        data = grade.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    INSERT INTO grades (
                        student_id,
                        subject_id,
                        marks_obtained,
                        exam_type,
                        academic_session
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    data["student_id"],
                    data["subject_id"],
                    data["marks_obtained"],
                    data["exam_type"],
                    data["academic_session"]
                ))

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Marks already exist for this student, subject, "
                "exam type and academic session."
            ) from error

    @staticmethod
    def update_grade(grade_id, grade):
        """Update an existing marks record."""

        if not isinstance(grade, Grade):
            raise TypeError("Expected a Grade object.")

        if not isinstance(grade_id, int) or grade_id <= 0:
            raise ValueError("Invalid grade ID.")

        subject = fetch_one("""
            SELECT max_marks
            FROM subjects
            WHERE subject_id = ?
        """, (grade.subject_id,))

        if subject is None:
            raise ValueError("Subject does not exist.")

        grade.validate(max_marks=subject["max_marks"])

        student = fetch_one("""
            SELECT student_id
            FROM students
            WHERE student_id = ?
        """, (grade.student_id,))

        if student is None:
            raise ValueError("Student does not exist.")

        data = grade.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    UPDATE grades
                    SET
                        student_id = ?,
                        subject_id = ?,
                        marks_obtained = ?,
                        exam_type = ?,
                        academic_session = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE grade_id = ?
                """, (
                    data["student_id"],
                    data["subject_id"],
                    data["marks_obtained"],
                    data["exam_type"],
                    data["academic_session"],
                    grade_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError("Grade record not found.")

                return True

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "A marks record already exists for this combination."
            ) from error

    @staticmethod
    def delete_grade(grade_id):
        """Delete a marks record."""

        if not isinstance(grade_id, int) or grade_id <= 0:
            raise ValueError("Invalid grade ID.")

        with get_db() as connection:

            cursor = connection.execute("""
                DELETE FROM grades
                WHERE grade_id = ?
            """, (grade_id,))

            if cursor.rowcount == 0:
                raise ValueError("Grade record not found.")

            return True

    @staticmethod
    def get_grade_by_id(grade_id):
        """Fetch a particular grade record."""

        if not isinstance(grade_id, int) or grade_id <= 0:
            raise ValueError("Invalid grade ID.")

        row = fetch_one("""
            SELECT
                g.*,
                s.roll_number,
                s.name AS student_name,
                sub.subject_code,
                sub.subject_name,
                sub.max_marks
            FROM grades g
            JOIN students s
                ON g.student_id = s.student_id
            JOIN subjects sub
                ON g.subject_id = sub.subject_id
            WHERE g.grade_id = ?
        """, (grade_id,))

        return dict(row) if row else None

    @staticmethod
    def get_student_grades(
        student_id,
        exam_type=None,
        academic_session=None
    ):
        """Fetch all marks belonging to a student."""

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID.")

        query = """
            SELECT
                g.grade_id,
                g.student_id,
                g.subject_id,
                g.marks_obtained,
                g.exam_type,
                g.academic_session,
                sub.subject_code,
                sub.subject_name,
                sub.max_marks,
                sub.credits
            FROM grades g
            JOIN subjects sub
                ON g.subject_id = sub.subject_id
            WHERE g.student_id = ?
        """

        parameters = [student_id]

        if exam_type:
            query += " AND g.exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session:
            query += " AND g.academic_session = ?"
            parameters.append(academic_session.strip())

        query += " ORDER BY sub.subject_name ASC"

        return [
            dict(row)
            for row in fetch_all(query, tuple(parameters))
        ]

    @staticmethod
    def get_subject_grades(
        subject_id,
        exam_type=None,
        academic_session=None
    ):
        """Fetch marks of all students in a subject."""

        if not isinstance(subject_id, int) or subject_id <= 0:
            raise ValueError("Invalid subject ID.")

        query = """
            SELECT
                g.grade_id,
                g.student_id,
                g.subject_id,
                g.marks_obtained,
                g.exam_type,
                g.academic_session,
                s.roll_number,
                s.name AS student_name,
                s.class_name,
                s.section,
                sub.subject_name,
                sub.max_marks
            FROM grades g
            JOIN students s
                ON g.student_id = s.student_id
            JOIN subjects sub
                ON g.subject_id = sub.subject_id
            WHERE g.subject_id = ?
        """

        parameters = [subject_id]

        if exam_type:
            query += " AND g.exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session:
            query += " AND g.academic_session = ?"
            parameters.append(academic_session.strip())

        query += " ORDER BY s.name ASC"

        return [
            dict(row)
            for row in fetch_all(query, tuple(parameters))
        ]

    @staticmethod
    def get_all_grades(
        search=None,
        class_name=None,
        subject_id=None,
        exam_type=None,
        academic_session=None
    ):
        """Fetch all marks with optional search and filters."""

        query = """
            SELECT
                g.grade_id,
                g.student_id,
                g.subject_id,
                g.marks_obtained,
                g.exam_type,
                g.academic_session,
                s.roll_number,
                s.name AS student_name,
                s.class_name,
                s.section,
                sub.subject_code,
                sub.subject_name,
                sub.max_marks,
                sub.credits
            FROM grades g
            JOIN students s
                ON g.student_id = s.student_id
            JOIN subjects sub
                ON g.subject_id = sub.subject_id
            WHERE 1 = 1
        """

        parameters = []

        if search and search.strip():

            term = f"%{search.strip()}%"

            query += """
                AND (
                    s.name LIKE ?
                    OR s.roll_number LIKE ?
                    OR sub.subject_name LIKE ?
                    OR sub.subject_code LIKE ?
                )
            """

            parameters.extend([term, term, term, term])

        if class_name and class_name.strip():
            query += " AND s.class_name = ?"
            parameters.append(class_name.strip())

        if subject_id is not None:
            if not isinstance(subject_id, int) or subject_id <= 0:
                raise ValueError("Invalid subject ID.")

            query += " AND g.subject_id = ?"
            parameters.append(subject_id)

        if exam_type and exam_type.strip():
            query += " AND g.exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session and academic_session.strip():
            query += " AND g.academic_session = ?"
            parameters.append(academic_session.strip())

        query += " ORDER BY g.grade_id DESC"

        return [
            dict(row)
            for row in fetch_all(query, tuple(parameters))
        ]

    @staticmethod
    def get_grade_count(
        exam_type=None,
        academic_session=None
    ):
        """Return the total number of grade entries."""

        query = "SELECT COUNT(*) AS total FROM grades WHERE 1=1"
        parameters = []

        if exam_type:
            query += " AND exam_type = ?"
            parameters.append(exam_type.strip())

        if academic_session:
            query += " AND academic_session = ?"
            parameters.append(academic_session.strip())

        row = fetch_one(query, tuple(parameters))

        return row["total"] if row else 0

    @staticmethod
    def get_available_sessions():
        """Return all available academic sessions."""

        rows = fetch_all("""
            SELECT DISTINCT academic_session
            FROM grades
            ORDER BY academic_session DESC
        """)

        return [
            row["academic_session"]
            for row in rows
        ]

    @staticmethod
    def get_available_exam_types():
        """Return all available examination types."""

        rows = fetch_all("""
            SELECT DISTINCT exam_type
            FROM grades
            ORDER BY exam_type ASC
        """)

        return [
            row["exam_type"]
            for row in rows
        ]
