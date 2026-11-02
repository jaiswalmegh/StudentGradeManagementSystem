
from database.connection import get_db


def ensure_column(connection, table, column, definition):
    """Add a column only if it does not already exist."""

    existing_columns = {
        row["name"]
        for row in connection.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    }

    if column not in existing_columns:
        connection.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


def create_tables():
    """Create and initialize all application database tables."""

    with get_db() as connection:

        # ==========================================
        # 1. USERS TABLE
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'admin',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ==========================================
        # 2. STUDENTS TABLE
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                email TEXT,
                class_name TEXT NOT NULL,
                section TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ==========================================
        # 3. SUBJECTS TABLE
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_code TEXT NOT NULL UNIQUE,
                subject_name TEXT NOT NULL,
                max_marks REAL NOT NULL DEFAULT 100,
                credits REAL NOT NULL DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CHECK(max_marks > 0),
                CHECK(credits > 0)
            )
        """)

        # ==========================================
        # 4. GRADES TABLE
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                grade_id INTEGER PRIMARY KEY AUTOINCREMENT,

                student_id INTEGER NOT NULL,
                subject_id INTEGER NOT NULL,

                marks_obtained REAL NOT NULL,

                exam_type TEXT NOT NULL,
                academic_session TEXT NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(student_id)
                    REFERENCES students(student_id)
                    ON DELETE CASCADE,

                FOREIGN KEY(subject_id)
                    REFERENCES subjects(subject_id)
                    ON DELETE CASCADE,

                UNIQUE(
                    student_id,
                    subject_id,
                    exam_type,
                    academic_session
                ),

                CHECK(marks_obtained >= 0)
            )
        """)

        # ==========================================
        # 5. DATABASE MIGRATIONS
        # ==========================================

        ensure_column(
            connection,
            "students",
            "updated_at",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        ensure_column(
            connection,
            "grades",
            "updated_at",
            "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        )

        # ==========================================
        # 6. DATABASE INDEXES
        # ==========================================

        indexes = [

            """
            CREATE INDEX IF NOT EXISTS idx_student_name
            ON students(name)
            """,

            """
            CREATE INDEX IF NOT EXISTS idx_student_class
            ON students(class_name, section)
            """,

            """
            CREATE INDEX IF NOT EXISTS idx_grade_student
            ON grades(student_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS idx_grade_subject
            ON grades(subject_id)
            """,

            """
            CREATE INDEX IF NOT EXISTS idx_grade_session
            ON grades(academic_session)
            """
        ]

        for query in indexes:
            connection.execute(query)

        # ==========================================
        # 7. SCHEMA VERSION
        # ==========================================

        connection.execute("""
            CREATE TABLE IF NOT EXISTS schema_info (
                version INTEGER NOT NULL
            )
        """)

        connection.execute("""
            INSERT INTO schema_info (version)
            SELECT 1
            WHERE NOT EXISTS (
                SELECT 1 FROM schema_info
            )
        """)

    print("Database initialized successfully!")


if __name__ == "__main__":
    create_tables()
