
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal

from controllers.student_controller import StudentController
from controllers.subject_controller import SubjectController
from services.analytics_service import AnalyticsService
from ui.components.stat_card import StatCard


class Dashboard(QWidget):

    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_dashboard_data()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 25, 28, 25)
        main_layout.setSpacing(22)

        # Welcome Section
        welcome_frame = QFrame()
        welcome_frame.setObjectName("WelcomeFrame")
        welcome_frame.setMinimumHeight(145)

        welcome_layout = QHBoxLayout(welcome_frame)
        welcome_layout.setContentsMargins(26, 22, 26, 22)

        welcome_text_layout = QVBoxLayout()
        welcome_text_layout.setSpacing(9)

        welcome_title = QLabel("Welcome to GradeFlow")
        welcome_title.setObjectName("WelcomeTitle")

        welcome_subtitle = QLabel(
            "Your academic management workspace. "
            "Monitor students, manage subjects and track performance."
        )
        welcome_subtitle.setObjectName("WelcomeSubtitle")
        welcome_subtitle.setWordWrap(True)

        welcome_text_layout.addWidget(welcome_title)
        welcome_text_layout.addWidget(welcome_subtitle)

        welcome_layout.addLayout(welcome_text_layout)
        welcome_layout.addStretch()

        self.welcome_badge = QLabel("ACADEMIC OVERVIEW")
        self.welcome_badge.setObjectName("WelcomeBadge")
        self.welcome_badge.setAlignment(Qt.AlignCenter)

        welcome_layout.addWidget(self.welcome_badge)

        main_layout.addWidget(welcome_frame)

        # Statistics Heading
        stats_heading = QHBoxLayout()

        stats_title = QLabel("Performance Overview")
        stats_title.setObjectName("SectionTitle")

        stats_subtitle = QLabel("Live academic statistics")
        stats_subtitle.setObjectName("SectionSubtitle")

        stats_heading.addWidget(stats_title)
        stats_heading.addStretch()
        stats_heading.addWidget(stats_subtitle)

        main_layout.addLayout(stats_heading)

        # Statistics Cards
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        self.student_card = StatCard(
            title="Total Students",
            value="0",
            subtitle="Registered students",
            icon="♟",
            accent_color="#22D3EE"
        )

        self.subject_card = StatCard(
            title="Total Subjects",
            value="0",
            subtitle="Available subjects",
            icon="▤",
            accent_color="#A78BFA"
        )

        self.average_card = StatCard(
            title="Class Average",
            value="0%",
            subtitle="Overall academic average",
            icon="◈",
            accent_color="#34D399"
        )

        self.pass_card = StatCard(
            title="Pass Percentage",
            value="0%",
            subtitle="Overall passing rate",
            icon="✓",
            accent_color="#FBBF24"
        )

        stats_grid.addWidget(self.student_card, 0, 0)
        stats_grid.addWidget(self.subject_card, 0, 1)
        stats_grid.addWidget(self.average_card, 0, 2)
        stats_grid.addWidget(self.pass_card, 0, 3)

        main_layout.addLayout(stats_grid)

        # Main Content Section
        content_grid = QGridLayout()
        content_grid.setSpacing(16)

        # Academic Summary
        summary_frame = QFrame()
        summary_frame.setObjectName("ContentCard")

        summary_layout = QVBoxLayout(summary_frame)
        summary_layout.setContentsMargins(22, 20, 22, 20)
        summary_layout.setSpacing(16)

        summary_title = QLabel("Academic Summary")
        summary_title.setObjectName("CardTitle")

        summary_description = QLabel(
            "A quick look at the current academic records."
        )
        summary_description.setObjectName("CardDescription")

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(summary_description)

        self.highest_label = self.create_info_label(
            "Highest Performance", "N/A"
        )

        self.lowest_label = self.create_info_label(
            "Lowest Performance", "N/A"
        )

        self.top_performer_label = self.create_info_label(
            "Top Performer", "N/A"
        )

        self.result_label = self.create_info_label(
            "Overall Result", "No records available"
        )

        summary_layout.addWidget(self.highest_label)
        summary_layout.addWidget(self.lowest_label)
        summary_layout.addWidget(self.top_performer_label)
        summary_layout.addWidget(self.result_label)

        summary_layout.addStretch()

        # Quick Actions
        actions_frame = QFrame()
        actions_frame.setObjectName("ContentCard")

        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(22, 20, 22, 20)
        actions_layout.setSpacing(14)

        actions_title = QLabel("Quick Actions")
        actions_title.setObjectName("CardTitle")

        actions_description = QLabel(
            "Jump directly to frequently used modules."
        )
        actions_description.setObjectName("CardDescription")

        actions_layout.addWidget(actions_title)
        actions_layout.addWidget(actions_description)

        self.students_action = self.create_action_button(
            "♟   Manage Students",
            "students"
        )

        self.subjects_action = self.create_action_button(
            "▤   Manage Subjects",
            "subjects"
        )

        self.marks_action = self.create_action_button(
            "✎   Enter Examination Marks",
            "marks"
        )

        self.analytics_action = self.create_action_button(
            "◈   View Academic Analytics",
            "analytics"
        )

        actions_layout.addWidget(self.students_action)
        actions_layout.addWidget(self.subjects_action)
        actions_layout.addWidget(self.marks_action)
        actions_layout.addWidget(self.analytics_action)

        actions_layout.addStretch()

        content_grid.addWidget(summary_frame, 0, 0)
        content_grid.addWidget(actions_frame, 0, 1)

        content_grid.setColumnStretch(0, 1)
        content_grid.setColumnStretch(1, 1)

        main_layout.addLayout(content_grid)
        main_layout.addStretch()

        # Dashboard Styling
        self.setStyleSheet("""
            QWidget {
                color: #E2E8F0;
                font-family: Segoe UI;
            }

            QFrame#WelcomeFrame {
                background-color: #172D40;
                border: 1px solid #24516A;
                border-radius: 14px;
            }

            QLabel#WelcomeTitle {
                color: #F1F5F9;
                font-size: 25px;
                font-weight: bold;
                background: transparent;
                border: none;
            }

            QLabel#WelcomeSubtitle {
                color: #A8BFD0;
                font-size: 12px;
                background: transparent;
                border: none;
            }

            QLabel#WelcomeBadge {
                color: #67E8F9;
                background-color: #164E63;
                border: 1px solid #0E7490;
                border-radius: 7px;
                padding: 9px 12px;
                font-size: 10px;
                font-weight: bold;
            }

            QLabel#SectionTitle {
                color: #F1F5F9;
                font-size: 18px;
                font-weight: bold;
                background: transparent;
                border: none;
            }

            QLabel#SectionSubtitle {
                color: #8492A6;
                font-size: 11px;
                background: transparent;
                border: none;
            }

            QFrame#ContentCard {
                background-color: #171D29;
                border: 1px solid #293548;
                border-radius: 12px;
            }

            QLabel#CardTitle {
                color: #F1F5F9;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                border: none;
            }

            QLabel#CardDescription {
                color: #8492A6;
                font-size: 11px;
                background: transparent;
                border: none;
            }

            QPushButton#DashboardAction {
                background-color: #202B3B;
                color: #CBD5E1;
                border: 1px solid #344155;
                border-radius: 8px;
                padding: 13px;
                text-align: left;
                font-size: 12px;
            }

            QPushButton#DashboardAction:hover {
                background-color: #263B50;
                border: 1px solid #22D3EE;
                color: #67E8F9;
            }
        """)

    def create_info_label(self, title, value):

        frame = QFrame()
        frame.setObjectName("InfoRow")

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(0, 8, 0, 8)

        title_label = QLabel(title)
        title_label.setObjectName("InfoTitle")

        value_label = QLabel(value)
        value_label.setObjectName("InfoValue")
        value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        frame.value_label = value_label

        frame.setStyleSheet("""
            QFrame#InfoRow {
                background: transparent;
                border-bottom: 1px solid #293548;
            }

            QLabel#InfoTitle {
                color: #A8B3C7;
                font-size: 12px;
                background: transparent;
                border: none;
            }

            QLabel#InfoValue {
                color: #22D3EE;
                font-size: 12px;
                font-weight: bold;
                background: transparent;
                border: none;
            }
        """)

        return frame

    def create_action_button(self, text, page_id):

        button = QPushButton(text)
        button.setObjectName("DashboardAction")
        button.setCursor(Qt.PointingHandCursor)

        button.clicked.connect(
            lambda checked=False, page=page_id:
            self.navigation_requested.emit(page)
        )

        return button

    def load_dashboard_data(self):

        try:

            total_students = StudentController.get_student_count()
            total_subjects = SubjectController.get_subject_count()

            summary = AnalyticsService.get_dashboard_summary()

            self.student_card.set_value(total_students)
            self.subject_card.set_value(total_subjects)

            average = summary.get("class_average", 0)
            pass_percentage = summary.get("pass_percentage", 0)

            self.average_card.set_value(
                f"{average:.2f}%"
            )

            self.pass_card.set_value(
                f"{pass_percentage:.2f}%"
            )

            highest = summary.get("highest_percentage", 0)
            lowest = summary.get("lowest_percentage", 0)

            self.highest_label.value_label.setText(
                f"{highest:.2f}%"
            )

            self.lowest_label.value_label.setText(
                f"{lowest:.2f}%"
            )

            top_performer = summary.get("top_performer")

            if isinstance(top_performer, dict):
                performer_name = top_performer.get(
                    "student_name",
                    top_performer.get("name", "N/A")
                )

                self.top_performer_label.value_label.setText(
                    performer_name
                )

            elif top_performer:
                self.top_performer_label.value_label.setText(
                    str(top_performer)
                )

            else:
                self.top_performer_label.value_label.setText("N/A")

            result = summary.get("result", "No records available")

            self.result_label.value_label.setText(
                str(result)
            )

        except Exception as error:

            self.student_card.set_value("!")
            self.subject_card.set_value("!")
            self.average_card.set_value("!")
            self.pass_card.set_value("!")

            self.result_label.value_label.setText(
                "Unable to load data"
            )

            print(f"Dashboard loading error: {error}")

    def refresh_dashboard(self):

        self.load_dashboard_data()

    def showEvent(self, event):

        super().showEvent(event)
        self.load_dashboard_data()
