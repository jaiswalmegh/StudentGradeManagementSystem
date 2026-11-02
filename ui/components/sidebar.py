
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QSpacerItem,
    QSizePolicy
)

from PyQt5.QtCore import pyqtSignal, Qt


class Sidebar(QWidget):

    page_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.expanded_width = 245
        self.collapsed_width = 76

        self.is_collapsed = False
        self.active_page = "dashboard"

        self.buttons = {}
        self.navigation_items = [
            ("dashboard", "▦", "Dashboard"),
            ("students", "♙", "Students"),
            ("subjects", "▤", "Subjects"),
            ("marks", "✎", "Marks Management"),
            ("analytics", "◫", "Analytics"),
        ]

        self.setObjectName("Sidebar")
        self.setFixedWidth(self.expanded_width)

        self.setup_ui()
        self.set_active_page("dashboard")

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            16, 25, 16, 20
        )

        self.main_layout.setSpacing(10)

        # BRANDING

        self.logo = QLabel(
            '<span style="color:#F1F5F9;">GRADE</span>'
            '<span style="color:#21C7D9;">FLOW</span>'
        )

        self.logo.setObjectName("Logo")
        self.logo.setTextFormat(Qt.RichText)
        self.logo.setAlignment(Qt.AlignCenter)

        self.subtitle = QLabel("STUDENT MANAGEMENT")
        self.subtitle.setObjectName("SidebarSubtitle")
        self.subtitle.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.logo)
        self.main_layout.addWidget(self.subtitle)

        self.main_layout.addSpacing(35)

        # MENU LABEL

        self.menu_label = QLabel("MAIN MENU")
        self.menu_label.setObjectName("MenuLabel")

        self.main_layout.addWidget(self.menu_label)
        self.main_layout.addSpacing(5)

        # NAVIGATION BUTTONS

        for page_id, icon, title in self.navigation_items:

            button = QPushButton(
                f"{icon}   {title}"
            )

            button.setObjectName("NavButton")
            button.setCursor(Qt.PointingHandCursor)
            button.setCheckable(True)
            button.setMinimumHeight(46)
            button.setToolTip(title)

            button.clicked.connect(
                lambda checked=False, page=page_id:
                self.navigate(page)
            )

            self.buttons[page_id] = button

            self.main_layout.addWidget(button)

        # SPACING

        self.main_layout.addItem(
            QSpacerItem(
                20,
                40,
                QSizePolicy.Minimum,
                QSizePolicy.Expanding
            )
        )

        # SIDEBAR FOOTER

        self.footer_line = QFrame()
        self.footer_line.setObjectName("SidebarDivider")
        self.footer_line.setFixedHeight(1)

        self.main_layout.addWidget(self.footer_line)
        self.main_layout.addSpacing(12)

        self.footer = QLabel(
            "ACADEMIC MANAGEMENT SYSTEM"
        )

        self.footer.setObjectName("SidebarFooter")
        self.footer.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.footer)

        self.version = QLabel("VERSION 1.0.0")
        self.version.setObjectName("SidebarVersion")
        self.version.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.version)

    def navigate(self, page_id):
        """
        Handle navigation and emit the selected page.
        """

        if page_id not in self.buttons:
            return

        self.set_active_page(page_id)
        self.page_changed.emit(page_id)

    def set_active_page(self, page_id):
        """
        Update the active navigation button.
        """

        if page_id not in self.buttons:
            return

        self.active_page = page_id

        for key, button in self.buttons.items():

            button.setChecked(key == page_id)

    def toggle_sidebar(self):
        """
        Expand or collapse the sidebar.
        """

        self.is_collapsed = not self.is_collapsed

        if self.is_collapsed:

            self.setFixedWidth(self.collapsed_width)

            self.logo.setText(
                '<span style="color:#21C7D9;">G</span>'
            )

            self.subtitle.hide()
            self.menu_label.hide()
            self.footer.hide()
            self.version.hide()
            self.footer_line.hide()

            for page_id, icon, title in self.navigation_items:

                button = self.buttons[page_id]
                button.setText(icon)
                button.setMinimumHeight(48)

        else:

            self.setFixedWidth(self.expanded_width)

            self.logo.setText(
                '<span style="color:#F1F5F9;">GRADE</span>'
                '<span style="color:#21C7D9;">FLOW</span>'
            )

            self.subtitle.show()
            self.menu_label.show()
            self.footer.show()
            self.version.show()
            self.footer_line.show()

            for page_id, icon, title in self.navigation_items:

                button = self.buttons[page_id]
                button.setText(f"{icon}   {title}")
                button.setMinimumHeight(46)

        self.set_active_page(self.active_page)
