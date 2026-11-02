
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget,
    QMessageBox
)
from PyQt5.QtCore import Qt

from ui.components.sidebar import Sidebar
from ui.components.header import Header

from ui.dashboard import Dashboard
from ui.pages.students_page import StudentsPage
from ui.pages.subjects_page import SubjectsPage
from ui.pages.marks_page import MarksPage
from ui.pages.analytics_page import AnalyticsPage


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(
            "GradeFlow | Student Grade Management System"
        )

        self.setMinimumSize(1100, 700)
        self.resize(1450, 900)

        self.pages = {}
        self.page_information = {
            "dashboard": (
                "Dashboard",
                "Overview of your academic workspace"
            ),
            "students": (
                "Student Management",
                "Manage student records and information"
            ),
            "subjects": (
                "Subject Management",
                "Manage subjects and credit allocation"
            ),
            "marks": (
                "Marks Management",
                "Manage examination marks and results"
            ),
            "analytics": (
                "Academic Analytics",
                "Explore academic performance and insights"
            )
        }

        self.setup_ui()
        self.connect_signals()

        self.navigate_to("dashboard")

    def setup_ui(self):

        # Central Widget
        central_widget = QWidget()
        central_widget.setObjectName("CentralWidget")

        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()

        main_layout.addWidget(self.sidebar)

        # Main Content Area
        self.content_container = QWidget()
        self.content_container.setObjectName(
            "ContentContainer"
        )

        content_layout = QVBoxLayout(
            self.content_container
        )

        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Header
        self.header = Header()

        content_layout.addWidget(self.header)

        # Page Stack
        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("PageStack")

        content_layout.addWidget(
            self.page_stack,
            1
        )

        main_layout.addWidget(
            self.content_container,
            1
        )

        # Register Application Pages
        self.register_pages()

        # Global Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #101722;
            }

            QWidget#CentralWidget {
                background-color: #101722;
            }

            QWidget#ContentContainer {
                background-color: #101722;
            }

            QStackedWidget#PageStack {
                background-color: #101722;
                border: none;
            }

            QWidget {
                font-family: Segoe UI;
            }
        """)

    def register_pages(self):

        self.pages = {
            "dashboard": Dashboard(),
            "students": StudentsPage(),
            "subjects": SubjectsPage(),
            "marks": MarksPage(),
            "analytics": AnalyticsPage()
        }

        for page in self.pages.values():

            self.page_stack.addWidget(page)

        # Dashboard Quick Navigation
        self.pages["dashboard"].navigation_requested.connect(
            self.navigate_to
        )

    def connect_signals(self):

        # Sidebar Navigation
        self.sidebar.page_changed.connect(
            self.navigate_to
        )

        # Sidebar Collapse / Expand
        self.header.sidebar_toggle_requested.connect(
            self.toggle_sidebar
        )

        # Global Search
        self.header.search_changed.connect(
            self.handle_global_search
        )

    def navigate_to(self, page_id):

        if page_id not in self.pages:
            return

        page = self.pages[page_id]

        self.page_stack.setCurrentWidget(page)

        self.sidebar.set_active_page(page_id)

        title, subtitle = self.page_information[page_id]

        self.header.set_title(
            title,
            subtitle
        )

        self.header.clear_search()

        if page_id == "dashboard":
            self.pages["dashboard"].refresh_dashboard()

        elif page_id == "analytics":
            self.pages["analytics"].refresh_analytics()

        elif page_id == "students":
            self.pages["students"].load_students()

        elif page_id == "subjects":
            self.pages["subjects"].load_subjects()

        elif page_id == "marks":
            self.pages["marks"].load_filter_options()
            self.pages["marks"].load_marks()

    def toggle_sidebar(self):

        self.sidebar.toggle_sidebar()

    def handle_global_search(self, search_text):

        current_page = self.page_stack.currentWidget()

        if isinstance(current_page, StudentsPage):

            current_page.search_input.setText(search_text)

        elif isinstance(current_page, SubjectsPage):

            current_page.search_input.setText(search_text)

        elif isinstance(current_page, MarksPage):

            current_page.search_input.setText(search_text)

    def closeEvent(self, event):

        confirmation = QMessageBox.question(
            self,
            "Exit GradeFlow",
            "Are you sure you want to close GradeFlow?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
