
import hashlib
import hmac
import secrets

from database.connection import get_db, fetch_one


class AuthService:
    """
    Handles secure admin account creation and authentication.
    Passwords are stored using PBKDF2-HMAC-SHA256.
    """

    ITERATIONS = 260000
    SALT_LENGTH = 16

    @staticmethod
    def _hash_password(password):
        salt = secrets.token_hex(AuthService.SALT_LENGTH)

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            AuthService.ITERATIONS
        ).hex()

        return (
            f"pbkdf2_sha256${AuthService.ITERATIONS}"
            f"${salt}${password_hash}"
        )

    @staticmethod
    def _verify_password(password, stored_hash):
        try:
            algorithm, iterations, salt, expected_hash = (
                stored_hash.split("$")
            )

            if algorithm != "pbkdf2_sha256":
                return False

            calculated_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                int(iterations)
            ).hex()

            return hmac.compare_digest(
                calculated_hash,
                expected_hash
            )

        except (ValueError, TypeError, AttributeError):
            return False

    @staticmethod
    def admin_exists():
        record = fetch_one(
            "SELECT COUNT(*) AS total FROM users"
        )

        return record["total"] > 0

    @staticmethod
    def create_admin(username, password, confirm_password):
        username = username.strip()

        if not username:
            raise ValueError("Username cannot be empty.")

        if len(username) < 4:
            raise ValueError(
                "Username must contain at least 4 characters."
            )

        if not password:
            raise ValueError("Password cannot be empty.")

        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        if AuthService.admin_exists():
            raise ValueError(
                "An admin account already exists."
            )

        password_hash = AuthService._hash_password(password)

        with get_db() as connection:
            connection.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, "admin")
            )

        return True

    @staticmethod
    def authenticate(username, password):
        username = username.strip()

        if not username or not password:
            return None

        record = fetch_one(
            """
            SELECT user_id, username, password_hash, role
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        if record is None:
            return None

        if not AuthService._verify_password(
            password,
            record["password_hash"]
        ):
            return None

        return {
            "user_id": record["user_id"],
            "username": record["username"],
            "role": record["role"]
        }
