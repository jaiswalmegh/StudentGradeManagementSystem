
import sys
from pathlib import Path

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox
)
from PyQt5.QtCore import Qt

from database.db_setup import create_tables
from services.auth_service import AuthService

from ui.dialogs.setup_admin_dialog import SetupAdminDialog
from ui.dialogs.login_dialog import LoginDialog
from ui.main_window import MainWindow

from utils.constants import APP_NAME, APP_VERSION


BASE_DIR = Path(__file__).resolve().parent
THEME_PATH = BASE_DIR / "assets" / "styles" / "dark_theme.qss"


def load_theme(app):
    """Load the application's global dark theme."""

    if THEME_PATH.exists():
        try:
            with open(THEME_PATH, "r", encoding="utf-8") as theme_file:
                app.setStyleSheet(theme_file.read())

        except OSError as error:
            print(f"Theme loading failed: {error}")

    else:
        print("Warning: Dark theme stylesheet not found.")


def initialize_database():
    """Initialize database tables before launching the UI."""

    try:
        create_tables()
        return True

    except Exception as error:
        QMessageBox.critical(
            None,
            "Database Initialization Error",
            f"Unable to initialize the database.\n\n{error}"
        )
        return False


def setup_first_admin():
    """Create the first administrator account."""

    dialog = SetupAdminDialog()

    def create_account(username, password, confirm_password):
        try:
            AuthService.create_admin(
                username,
                password,
                confirm_password
            )

            QMessageBox.information(
                dialog,
                "Account Created",
                "Administrator account created successfully.\n"
                "You can now log in."
            )

            dialog.accept_setup()

        except ValueError as error:
            dialog.set_error(str(error))

        except Exception as error:
            dialog.set_error(
                f"Unable to create administrator account: {error}"
            )

    dialog.setup_requested.connect(create_account)

    return dialog.exec_() == SetupAdminDialog.Accepted


def authenticate_admin():
    """Display the login screen and authenticate the administrator."""

    dialog = LoginDialog()
    authenticated_user = {}

    def verify_credentials(username, password):
        try:
            user = AuthService.authenticate(username, password)

            if user is None:
                dialog.set_login_error(
                    "Invalid username or password."
                )
                return

            authenticated_user.update(user)
            dialog.accept_login(user["username"])

        except Exception as error:
            dialog.set_login_error(
                f"Login failed. Please try again. {error}"
            )

    dialog.login_requested.connect(verify_credentials)

    if dialog.exec_() == LoginDialog.Accepted:
        return authenticated_user

    return None


def launch_application():
    """Start the GradeFlow desktop application."""

    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("GradeFlow")

    app.setStyle("Fusion")

    load_theme(app)

    # Initialize database.
    if not initialize_database():
        return 1

    # First-run administrator setup.
    try:
        if not AuthService.admin_exists():
            if not setup_first_admin():
                return 0

    except Exception as error:
        QMessageBox.critical(
            None,
            "Authentication Error",
            f"Unable to check administrator account.\n\n{error}"
        )
        return 1

    # Administrator login.
    authenticated_user = authenticate_admin()

    if not authenticated_user:
        return 0

    # Launch main application window.
    try:
        window = MainWindow()

        window.header.set_admin_name(
            authenticated_user["username"]
        )

        window.show()

        return app.exec_()

    except Exception as error:
        QMessageBox.critical(
            None,
            "Application Startup Error",
            f"Unable to launch GradeFlow.\n\n{error}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(launch_application())
