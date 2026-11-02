
import sqlite3
from pathlib import Path
from contextlib import contextmanager


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "student_grades.db"


def get_connection():
    """Create a new SQLite database connection."""

    connection = sqlite3.connect(
        str(DB_PATH),
        timeout=10
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")

    return connection


@contextmanager
def get_db():
    """
    Provide a database connection with automatic
    commit, rollback and connection closing.
    """

    connection = get_connection()

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def execute_query(query, parameters=()):
    """Execute INSERT, UPDATE or DELETE queries."""

    with get_db() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.lastrowid


def fetch_all(query, parameters=()):
    """Fetch all matching records."""

    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchall()


def fetch_one(query, parameters=()):
    """Fetch a single matching record."""

    with get_connection() as connection:
        cursor = connection.execute(query, parameters)
        return cursor.fetchone()
