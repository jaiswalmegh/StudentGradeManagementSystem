
import sqlite3

from database.connection import (
    get_db,
    fetch_all,
    fetch_one
)

from models.subject import Subject


class SubjectController:
    """
    Handles all subject-related database operations.
    """

    @staticmethod
    def add_subject(subject):
        """Add a new subject to the database."""

        if not isinstance(subject, Subject):
            raise TypeError("Expected a Subject object.")

        subject.validate()

        data = subject.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    INSERT INTO subjects (
                        subject_code,
                        subject_name,
                        max_marks,
                        credits
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    data["subject_code"],
                    data["subject_name"],
                    data["max_marks"],
                    data["credits"]
                ))

                return cursor.lastrowid

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "A subject with this subject code already exists."
            ) from error

    @staticmethod
    def update_subject(subject_id, subject):
        """Update an existing subject."""

        if not isinstance(subject, Subject):
            raise TypeError("Expected a Subject object.")

        if not isinstance(subject_id, int) or subject_id <= 0:
            raise ValueError("Invalid subject ID.")

        subject.validate()

        data = subject.to_dict()

        try:
            with get_db() as connection:

                cursor = connection.execute("""
                    UPDATE subjects
                    SET
                        subject_code = ?,
                        subject_name = ?,
                        max_marks = ?,
                        credits = ?
                    WHERE subject_id = ?
                """, (
                    data["subject_code"],
                    data["subject_name"],
                    data["max_marks"],
                    data["credits"],
                    subject_id
                ))

                if cursor.rowcount == 0:
                    raise ValueError("Subject record not found.")

                return True

        except sqlite3.IntegrityError as error:
            raise ValueError(
                "Another subject already uses this subject code."
            ) from error

    @staticmethod
    def delete_subject(subject_id):
        """Delete a subject and its associated grade records."""

        if not isinstance(subject_id, int) or subject_id <= 0:
            raise ValueError("Invalid subject ID.")

        with get_db() as connection:

            cursor = connection.execute("""
                DELETE FROM subjects
                WHERE subject_id = ?
            """, (subject_id,))

            if cursor.rowcount == 0:
                raise ValueError("Subject record not found.")

            return True

    @staticmethod
    def get_subject_by_id(subject_id):
        """Retrieve a subject using its database ID."""

        if not isinstance(subject_id, int) or subject_id <= 0:
            raise ValueError("Invalid subject ID.")

        row = fetch_one("""
            SELECT *
            FROM subjects
            WHERE subject_id = ?
        """, (subject_id,))

        return Subject.from_row(row)

    @staticmethod
    def get_subject_by_code(subject_code):
        """Retrieve a subject using its subject code."""

        if not subject_code or not subject_code.strip():
            raise ValueError("Subject code is required.")

        row = fetch_one("""
            SELECT *
            FROM subjects
            WHERE subject_code = ?
        """, (subject_code.strip(),))

        return Subject.from_row(row)

    @staticmethod
    def get_all_subjects(search=None):
        """Retrieve all subjects with optional searching."""

        query = """
            SELECT *
            FROM subjects
            WHERE 1 = 1
        """

        parameters = []

        if search and search.strip():

            search_term = f"%{search.strip()}%"

            query += """
                AND (
                    subject_name LIKE ?
                    OR subject_code LIKE ?
                )
            """

            parameters.extend([
                search_term,
                search_term
            ])

        query += " ORDER BY subject_name ASC"

        rows = fetch_all(query, tuple(parameters))

        return [
            Subject.from_row(row)
            for row in rows
        ]

    @staticmethod
    def get_subject_count():
        """Return the total number of registered subjects."""

        row = fetch_one("""
            SELECT COUNT(*) AS total
            FROM subjects
        """)

        return row["total"] if row else 0

    @staticmethod
    def get_subject_statistics():
        """Return basic subject statistics."""

        row = fetch_one("""
            SELECT
                COUNT(*) AS total_subjects,
                COALESCE(SUM(credits), 0) AS total_credits,
                COALESCE(AVG(max_marks), 0) AS average_max_marks
            FROM subjects
        """)

        return dict(row) if row else {
            "total_subjects": 0,
            "total_credits": 0,
            "average_max_marks": 0
        }
