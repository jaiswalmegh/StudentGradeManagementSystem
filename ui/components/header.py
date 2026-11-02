
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal


class Header(QWidget):

    search_changed = pyqtSignal(str)
    sidebar_toggle_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Header")
        self.setFixedHeight(82)

        self.setup_ui()

    def setup_ui(self):

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(18)

        # Sidebar Toggle Button
        self.toggle_button = QPushButton("☰")
        self.toggle_button.setObjectName("SidebarToggle")
        self.toggle_button.setFixedSize(42, 42)
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.clicked.connect(
            self.sidebar_toggle_requested.emit
        )

        main_layout.addWidget(self.toggle_button)

        # Page Information
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        self.page_title = QLabel("Dashboard")
        self.page_title.setObjectName("PageTitle")

        self.page_subtitle = QLabel(
            "Overview of your academic workspace"
        )
        self.page_subtitle.setObjectName("PageSubtitle")

        title_layout.addWidget(self.page_title)
        title_layout.addWidget(self.page_subtitle)

        main_layout.addLayout(title_layout)

        main_layout.addStretch()

        # Global Search
        self.search_input = QLineEdit()
        self.search_input.setObjectName("GlobalSearch")
        self.search_input.setPlaceholderText(
            "Search students, subjects..."
        )
        self.search_input.setFixedWidth(270)
        self.search_input.setFixedHeight(40)
        self.search_input.setClearButtonEnabled(True)

        self.search_input.textChanged.connect(
            self.search_changed.emit
        )

        main_layout.addWidget(self.search_input)

        # Vertical Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setObjectName("HeaderSeparator")
        separator.setFixedHeight(38)

        main_layout.addWidget(separator)

        # Admin Profile
        profile_layout = QHBoxLayout()
        profile_layout.setSpacing(10)

        self.admin_avatar = QLabel("A")
        self.admin_avatar.setObjectName("AdminAvatar")
        self.admin_avatar.setAlignment(Qt.AlignCenter)
        self.admin_avatar.setFixedSize(40, 40)

        admin_details = QVBoxLayout()
        admin_details.setSpacing(3)

        self.admin_name = QLabel("Administrator")
        self.admin_name.setObjectName("AdminName")

        self.admin_role = QLabel("System Admin")
        self.admin_role.setObjectName("AdminRole")

        admin_details.addWidget(self.admin_name)
        admin_details.addWidget(self.admin_role)

        profile_layout.addWidget(self.admin_avatar)
        profile_layout.addLayout(admin_details)

        main_layout.addLayout(profile_layout)

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

    def set_title(self, title, subtitle=None):

        self.page_title.setText(title)

        if subtitle is not None:
            self.page_subtitle.setText(subtitle)

    def set_admin_name(self, name):

        self.admin_name.setText(name)

        if name.strip():
            self.admin_avatar.setText(name.strip()[0].upper())
        else:
            self.admin_avatar.setText("A")

    def set_search_placeholder(self, text):

        self.search_input.setPlaceholderText(text)

    def get_search_text(self):

        return self.search_input.text().strip()

    def clear_search(self):

        self.search_input.clear()
