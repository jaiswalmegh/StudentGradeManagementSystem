
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal


class LoginDialog(QDialog):

    login_requested = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.authenticated = False
        self.username = ""

        self.setWindowTitle("GradeFlow | Admin Login")
        self.setFixedSize(480, 650)
        self.setWindowFlags(
            Qt.Dialog | Qt.FramelessWindowHint
        )

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        container = QFrame()
        container.setObjectName("LoginContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(38, 30, 38, 25)
        layout.setSpacing(0)

        # =========================
        # BRANDING
        # =========================

        brand = QLabel("GRADEFLOW")
        brand.setObjectName("BrandName")
        brand.setAlignment(Qt.AlignCenter)

        layout.addWidget(brand)

        layout.addSpacing(9)

        tagline = QLabel(
            "STUDENT GRADE MANAGEMENT SYSTEM"
        )
        tagline.setObjectName("BrandTagline")
        tagline.setAlignment(Qt.AlignCenter)

        layout.addWidget(tagline)

        # =========================
        # LOGO
        # =========================

        layout.addSpacing(27)

        logo = QLabel("G")
        logo.setObjectName("LoginLogo")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFixedSize(76, 76)

        logo_container = QHBoxLayout()
        logo_container.addStretch()
        logo_container.addWidget(logo)
        logo_container.addStretch()

        layout.addLayout(logo_container)

        # =========================
        # WELCOME SECTION
        # =========================

        layout.addSpacing(19)

        welcome = QLabel("Welcome Back")
        welcome.setObjectName("WelcomeTitle")
        welcome.setAlignment(Qt.AlignCenter)

        layout.addWidget(welcome)

        layout.addSpacing(8)

        description = QLabel(
            "Sign in to access your academic dashboard"
        )
        description.setObjectName("WelcomeDescription")
        description.setAlignment(Qt.AlignCenter)

        layout.addWidget(description)

        # =========================
        # LOGIN FORM
        # =========================

        layout.addSpacing(30)

        # Username label
        username_label = QLabel("USERNAME")
        username_label.setObjectName("InputLabel")

        layout.addWidget(username_label)

        layout.addSpacing(9)

        # Username input
        self.username_input = QLineEdit()
        self.username_input.setObjectName("LoginInput")
        self.username_input.setPlaceholderText(
            "Enter your username"
        )
        self.username_input.setFixedHeight(46)

        layout.addWidget(self.username_input)

        # Password section
        layout.addSpacing(21)

        password_label = QLabel("PASSWORD")
        password_label.setObjectName("InputLabel")

        layout.addWidget(password_label)

        layout.addSpacing(9)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setObjectName("LoginInput")
        self.password_input.setPlaceholderText(
            "Enter your password"
        )
        self.password_input.setEchoMode(
            QLineEdit.Password
        )
        self.password_input.setFixedHeight(46)

        layout.addWidget(self.password_input)

        # Show password
        show_layout = QHBoxLayout()
        show_layout.setContentsMargins(0, 8, 0, 0)

        show_layout.addStretch()

        self.show_password_button = QPushButton(
            "Show Password"
        )
        self.show_password_button.setObjectName(
            "ShowPasswordButton"
        )
        self.show_password_button.setCursor(
            Qt.PointingHandCursor
        )

        self.show_password_button.clicked.connect(
            self.toggle_password_visibility
        )

        show_layout.addWidget(
            self.show_password_button
        )

        layout.addLayout(show_layout)

        # =========================
        # ERROR MESSAGE
        # =========================

        layout.addSpacing(8)

        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setMinimumHeight(20)

        layout.addWidget(self.error_label)

        # =========================
        # SIGN IN BUTTON
        # =========================

        layout.addSpacing(10)

        self.login_button = QPushButton("SIGN IN")
        self.login_button.setObjectName("LoginButton")
        self.login_button.setFixedHeight(49)
        self.login_button.setCursor(
            Qt.PointingHandCursor
        )

        self.login_button.clicked.connect(
            self.handle_login
        )

        layout.addWidget(self.login_button)

        # =========================
        # FOOTER
        # =========================

        layout.addStretch()

        footer_line = QFrame()
        footer_line.setFixedHeight(1)
        footer_line.setStyleSheet(
            "background-color: #29394A; border: none;"
        )

        layout.addWidget(footer_line)

        layout.addSpacing(17)

        footer = QLabel(
            "SECURE ADMINISTRATOR ACCESS  •  GRADEFLOW"
        )
        footer.setObjectName("LoginFooter")
        footer.setAlignment(Qt.AlignCenter)

        layout.addWidget(footer)

        main_layout.addWidget(container)

        # Enter key support
        self.username_input.returnPressed.connect(
            self.password_input.setFocus
        )

        self.password_input.returnPressed.connect(
            self.handle_login
        )

        # =========================
        # STYLESHEET
        # =========================

        self.setStyleSheet("""
            QDialog {
                background-color: #0B1420;
            }

            QFrame#LoginContainer {
                background-color: #111C29;
                border: 1px solid #293B4F;
                border-radius: 15px;
            }

            QLabel#BrandName {
                color: #22D3EE;
                font-size: 25px;
                font-weight: 900;
                letter-spacing: 4px;
                border: none;
            }

            QLabel#BrandTagline {
                color: #71849A;
                font-size: 9px;
                letter-spacing: 1.5px;
                border: none;
            }

            QLabel#LoginLogo {
                background-color: #164E63;
                color: #67E8F9;
                border: 2px solid #22D3EE;
                border-radius: 38px;
                font-size: 32px;
                font-weight: 800;
            }

            QLabel#WelcomeTitle {
                color: #F1F5F9;
                font-size: 25px;
                font-weight: 800;
                border: none;
            }

            QLabel#WelcomeDescription {
                color: #94A3B8;
                font-size: 11px;
                border: none;
            }

            QLabel#InputLabel {
                color: #A8B6C7;
                font-size: 10px;
                font-weight: 800;
                letter-spacing: 1.2px;
                border: none;
            }

            QLineEdit#LoginInput {
                background-color: #1C2939;
                color: #F1F5F9;
                border: 1px solid #34495E;
                border-radius: 8px;
                padding: 0 13px;
                font-size: 12px;
                selection-background-color: #087F95;
            }

            QLineEdit#LoginInput:focus {
                border: 1px solid #22D3EE;
                background-color: #202F40;
            }

            QLineEdit#LoginInput::placeholder {
                color: #718096;
            }

            QPushButton#ShowPasswordButton {
                background: transparent;
                color: #22D3EE;
                border: none;
                font-size: 10px;
                font-weight: 600;
                padding: 3px;
            }

            QPushButton#ShowPasswordButton:hover {
                color: #67E8F9;
            }

            QPushButton#LoginButton {
                background-color: #00AFC8;
                color: #07131D;
                border: none;
                border-radius: 9px;
                font-size: 13px;
                font-weight: 800;
                letter-spacing: 1.2px;
            }

            QPushButton#LoginButton:hover {
                background-color: #22D3EE;
            }

            QPushButton#LoginButton:pressed {
                background-color: #0891B2;
            }

            QLabel#ErrorLabel {
                color: #FB7185;
                font-size: 11px;
                font-weight: 600;
                border: none;
            }

            QLabel#LoginFooter {
                color: #64748B;
                font-size: 9px;
                letter-spacing: 1px;
                border: none;
            }
        """)

    def toggle_password_visibility(self):

        if self.password_input.echoMode() == QLineEdit.Password:

            self.password_input.setEchoMode(
                QLineEdit.Normal
            )

            self.show_password_button.setText(
                "Hide Password"
            )

        else:

            self.password_input.setEchoMode(
                QLineEdit.Password
            )

            self.show_password_button.setText(
                "Show Password"
            )

    def handle_login(self):

        username = self.username_input.text().strip()
        password = self.password_input.text()

        self.error_label.clear()

        if not username:

            self.error_label.setText(
                "Please enter your username."
            )

            self.username_input.setFocus()
            return

        if not password:

            self.error_label.setText(
                "Please enter your password."
            )

            self.password_input.setFocus()
            return

        self.login_requested.emit(
            username,
            password
        )

    def set_login_error(self, message):

        self.error_label.setText(str(message))

        self.password_input.clear()
        self.password_input.setFocus()

    def accept_login(self, username):

        self.authenticated = True
        self.username = username

        self.accept()

    def get_username(self):

        return self.username
