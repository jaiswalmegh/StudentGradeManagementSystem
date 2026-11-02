
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QCheckBox,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal


class SetupAdminDialog(QDialog):
    setup_requested = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("GradeFlow | Admin Setup")
        self.setFixedSize(480, 650)
        self.setModal(True)

        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #0B1420;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(38, 30, 38, 28)
        root.setSpacing(0)

        # Branding
        logo = QLabel("GF")
        logo.setFixedSize(64, 64)
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            QLabel {
                background: #00BCD4;
                color: #07131D;
                border-radius: 18px;
                font-size: 25px;
                font-weight: 900;
            }
        """)

        logo_row = QHBoxLayout()
        logo_row.addStretch()
        logo_row.addWidget(logo)
        logo_row.addStretch()

        root.addLayout(logo_row)
        root.addSpacing(22)

        title = QLabel("Create Administrator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #F8FAFC;
            font-size: 24px;
            font-weight: 800;
        """)

        subtitle = QLabel(
            "Set up your secure administrator account"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            color: #94A3B8;
            font-size: 12px;
        """)

        root.addWidget(title)
        root.addSpacing(8)
        root.addWidget(subtitle)
        root.addSpacing(30)

        # Form card
        card = QFrame()
        card.setObjectName("formCard")
        card.setStyleSheet("""
            QFrame#formCard {
                background-color: #142130;
                border: 1px solid #293B4F;
                border-radius: 15px;
            }
        """)

        form = QVBoxLayout(card)
        form.setContentsMargins(23, 24, 23, 23)
        form.setSpacing(0)

        self.username_input = self.create_input(
            "Enter username"
        )
        self.password_input = self.create_input(
            "Enter a strong password", True
        )
        self.confirm_password_input = self.create_input(
            "Re-enter your password", True
        )

        form.addWidget(self.create_label("USERNAME"))
        form.addSpacing(9)
        form.addWidget(self.username_input)

        form.addSpacing(21)

        form.addWidget(self.create_label("PASSWORD"))
        form.addSpacing(9)
        form.addWidget(self.password_input)

        form.addSpacing(21)

        form.addWidget(self.create_label("CONFIRM PASSWORD"))
        form.addSpacing(9)
        form.addWidget(self.confirm_password_input)

        form.addSpacing(16)

        self.show_password_checkbox = QCheckBox(
            "Show passwords"
        )
        self.show_password_checkbox.setCursor(
            Qt.PointingHandCursor
        )
        self.show_password_checkbox.setStyleSheet("""
            QCheckBox {
                color: #A8B6C7;
                font-size: 11px;
                spacing: 9px;
                border: none;
            }

            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #52657A;
                border-radius: 4px;
                background: #0B1420;
            }

            QCheckBox::indicator:checked {
                background: #00BCD4;
                border-color: #00BCD4;
            }
        """)

        self.show_password_checkbox.toggled.connect(
            self.toggle_password_visibility
        )

        form.addWidget(self.show_password_checkbox)

        root.addWidget(card)
        root.addSpacing(15)

        # Error message
        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setMinimumHeight(25)
        self.error_label.setStyleSheet("""
            color: #FB7185;
            font-size: 11px;
            font-weight: 600;
        """)

        root.addWidget(self.error_label)
        root.addSpacing(7)

        # Create button
        self.setup_button = QPushButton(
            "Create Admin Account"
        )
        self.setup_button.setFixedHeight(49)
        self.setup_button.setCursor(Qt.PointingHandCursor)
        self.setup_button.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: #07131D;
                border: none;
                border-radius: 9px;
                font-size: 13px;
                font-weight: 800;
            }

            QPushButton:hover {
                background-color: #22D3E5;
            }

            QPushButton:pressed {
                background-color: #0891B2;
            }

            QPushButton:disabled {
                background-color: #42616B;
                color: #A8BAC0;
            }
        """)

        self.setup_button.clicked.connect(self.handle_setup)
        root.addWidget(self.setup_button)

        root.addSpacing(17)

        footer = QLabel(
            "YOUR DATA IS PROTECTED WITH SECURE PASSWORD HASHING"
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setWordWrap(True)
        footer.setStyleSheet("""
            color: #64748B;
            font-size: 9px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)

        root.addWidget(footer)

    @staticmethod
    def create_label(text):
        label = QLabel(text)
        label.setStyleSheet("""
            color: #9FB0C2;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        """)
        return label

    @staticmethod
    def create_input(placeholder, password=False):
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setFixedHeight(45)
        field.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        if password:
            field.setEchoMode(QLineEdit.Password)

        field.setStyleSheet("""
            QLineEdit {
                background-color: #0B1420;
                color: #F1F5F9;
                border: 1px solid #34495E;
                border-radius: 8px;
                padding: 0 13px;
                font-size: 12px;
                selection-background-color: #087F95;
            }

            QLineEdit:focus {
                border: 1px solid #00BCD4;
                background-color: #101D2B;
            }

            QLineEdit::placeholder {
                color: #64748B;
            }
        """)

        return field

    def toggle_password_visibility(self, visible):
        mode = (
            QLineEdit.Normal
            if visible
            else QLineEdit.Password
        )

        self.password_input.setEchoMode(mode)
        self.confirm_password_input.setEchoMode(mode)

    def handle_setup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not username or not password or not confirm_password:
            self.set_error("Please complete all fields.")
            return

        if len(username) < 4:
            self.set_error(
                "Username must contain at least 4 characters."
            )
            return

        if len(password) < 8:
            self.set_error(
                "Password must contain at least 8 characters."
            )
            return

        if password != confirm_password:
            self.set_error("Passwords do not match.")
            return

        self.error_label.clear()
        self.setup_button.setEnabled(False)
        self.setup_button.setText("Creating Account...")

        self.setup_requested.emit(
            username,
            password,
            confirm_password
        )

    def set_error(self, message):
        self.error_label.setText(message)
        self.setup_button.setEnabled(True)
        self.setup_button.setText("Create Admin Account")

    def accept_setup(self):
        self.accept()
