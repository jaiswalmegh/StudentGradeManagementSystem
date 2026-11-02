
import sqlite3

from database.connection import (
    get_db,
    fetch_all,
    fetch_one
)

from models.student import Student


class StudentController:
    """
    Handles all student-related database operations.
    """

    @staticmethod
    def add_student(student):
        """Add a new student to the database."""

        if not isinstance(student, Student):
            raise TypeError("Expected a Student object.")

        student.validate()

        data = student.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    INSERT INTO students (
                        roll_number,
                        name,
                        email,
                        class_name,
                        section
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    data["roll_number"],
                    data["name"],
                    data["email"],
                    data["class_name"],
                    data["section"]
                ))

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "A student with this roll number already exists."
            ) from error

    @staticmethod
    def update_student(student_id, student):
        """Update an existing student record."""

        if not isinstance(student, Student):
            raise TypeError("Expected a Student object.")

        student.validate()

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID.")

        data = student.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    UPDATE students
                    SET
                        roll_number = ?,
                        name = ?,
                        email = ?,
                        class_name = ?,
                        section = ?,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE student_id = ?
                """, (
                    data["roll_number"],
                    data["name"],
                    data["email"],
                    data["class_name"],
                    data["section"],
                    student_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError("Student record not found.")

                return True

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Another student already uses this roll number."
            ) from error

    @staticmethod
    def delete_student(student_id):
        """Delete a student and associated grade records."""

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID.")

        with get_db() as connection:

            cursor = connection.execute("""
                DELETE FROM students
                WHERE student_id = ?
            """, (student_id,))

            if cursor.rowcount == 0:
                raise ValueError("Student record not found.")

            return True

    @staticmethod
    def get_student_by_id(student_id):
        """Retrieve a student using their database ID."""

        if not isinstance(student_id, int) or student_id <= 0:
            raise ValueError("Invalid student ID.")

        row = fetch_one("""
            SELECT *
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        return Student.from_row(row)

    @staticmethod
    def get_student_by_roll_number(roll_number):
        """Retrieve a student using their roll number."""

        if not roll_number or not roll_number.strip():
            raise ValueError("Roll number is required.")

        row = fetch_one("""
            SELECT *
            FROM students
            WHERE roll_number = ?
        """, (roll_number.strip(),))

        return Student.from_row(row)

    @staticmethod
    def get_all_students(
        search=None,
        class_name=None,
        section=None
    ):
        """
        Retrieve students with optional search and filters.
        """

        query = """
            SELECT *
            FROM students
            WHERE 1 = 1
        """

        parameters = []

        if search and search.strip():

            search_term = f"%{search.strip()}%"

            query += """
                AND (
                    name LIKE ?
                    OR roll_number LIKE ?
                    OR email LIKE ?
                )
            """

            parameters.extend([
                search_term,
                search_term,
                search_term
            ])

        if class_name and class_name.strip():

            query += " AND class_name = ?"
            parameters.append(class_name.strip())

        if section and section.strip():

            query += " AND section = ?"
            parameters.append(section.strip())

        query += " ORDER BY student_id DESC"

        rows = fetch_all(query, tuple(parameters))

        return [
            Student.from_row(row)
            for row in rows
        ]

    @staticmethod
    def get_student_count():
        """Return the total number of students."""

        row = fetch_one("""
            SELECT COUNT(*) AS total
            FROM students
        """)

        return row["total"] if row else 0

    @staticmethod
    def get_all_classes():
        """Return all distinct class names."""

        rows = fetch_all("""
            SELECT DISTINCT class_name
            FROM students
            ORDER BY class_name
        """)

        return [
            row["class_name"]
            for row in rows
        ]

    @staticmethod
    def get_sections(class_name=None):
        """Return distinct sections, optionally by class."""

        if class_name and class_name.strip():

            rows = fetch_all("""
                SELECT DISTINCT section
                FROM students
                WHERE class_name = ?
                  AND section IS NOT NULL
                  AND section != ''
                ORDER BY section
            """, (class_name.strip(),))

        else:

            rows = fetch_all("""
                SELECT DISTINCT section
                FROM students
                WHERE section IS NOT NULL
                  AND section != ''
                ORDER BY section
            """)

        return [
            row["section"]
            for row in rows
        ]
