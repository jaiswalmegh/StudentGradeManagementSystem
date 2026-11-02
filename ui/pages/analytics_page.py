
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFrame,
    QMessageBox,
    QGridLayout,
    QScrollArea,
    QSizePolicy
)
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas
)
from matplotlib.figure import Figure

from services.analytics_service import AnalyticsService
from controllers.grade_controller import GradeController
from controllers.student_controller import StudentController
from controllers.subject_controller import SubjectController


class AnalyticsChart(QFrame):

    def __init__(self, title, parent=None):
        super().__init__(parent)

        self.setObjectName("AnalyticsChart")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("ChartTitle")

        layout.addWidget(self.title_label)

        self.figure = Figure(
            figsize=(5, 3),
            dpi=100,
            facecolor="#171D29"
        )

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        layout.addWidget(self.canvas)

        self.setMinimumHeight(310)

    def clear_chart(self):

        self.figure.clear()

    def finish_chart(self):

        self.figure.tight_layout(pad=2)
        self.canvas.draw()


class AnalyticsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_filter_options()
        self.load_analytics()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 22, 28, 25)
        main_layout.setSpacing(18)

        # Heading
        heading_layout = QHBoxLayout()

        heading_left = QVBoxLayout()
        heading_left.setSpacing(5)

        heading = QLabel("Academic Analytics")
        heading.setObjectName("PageHeading")

        description = QLabel(
            "Visual insights into student results and academic performance"
        )
        description.setObjectName("PageDescription")

        heading_left.addWidget(heading)
        heading_left.addWidget(description)

        heading_layout.addLayout(heading_left)
        heading_layout.addStretch()

        self.refresh_button = QPushButton("↻ Refresh Analytics")
        self.refresh_button.clicked.connect(
            self.refresh_analytics
        )

        heading_layout.addWidget(self.refresh_button)

        main_layout.addLayout(heading_layout)

        # Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")

        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(14, 10, 14, 10)
        filter_layout.setSpacing(12)

        filter_label = QLabel("Filters")
        filter_label.setObjectName("FilterLabel")

        self.class_filter = QComboBox()
        self.class_filter.addItem("All Classes")

        self.exam_filter = QComboBox()
        self.exam_filter.addItem("All Exams")

        self.session_filter = QComboBox()
        self.session_filter.addItem("All Sessions")

        for combo in (
            self.class_filter,
            self.exam_filter,
            self.session_filter
        ):
            combo.setMinimumHeight(36)
            combo.currentIndexChanged.connect(
                self.load_analytics
            )

        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.class_filter, 2)
        filter_layout.addWidget(self.exam_filter, 2)
        filter_layout.addWidget(self.session_filter, 2)

        main_layout.addWidget(filter_frame)

        # Summary Cards
        self.summary_layout = QGridLayout()
        self.summary_layout.setSpacing(12)

        self.total_students_card = self.create_summary_card(
            "Total Students", "0", "#22D3EE"
        )

        self.total_subjects_card = self.create_summary_card(
            "Total Subjects", "0", "#A78BFA"
        )

        self.average_card = self.create_summary_card(
            "Class Average", "0%", "#34D399"
        )

        self.pass_card = self.create_summary_card(
            "Pass Percentage", "0%", "#FBBF24"
        )

        self.summary_layout.addWidget(
            self.total_students_card, 0, 0
        )
        self.summary_layout.addWidget(
            self.total_subjects_card, 0, 1
        )
        self.summary_layout.addWidget(
            self.average_card, 0, 2
        )
        self.summary_layout.addWidget(
            self.pass_card, 0, 3
        )

        main_layout.addLayout(self.summary_layout)

        # Charts Scroll Area
        self.chart_scroll = QScrollArea()
        self.chart_scroll.setWidgetResizable(True)
        self.chart_scroll.setFrameShape(QFrame.NoFrame)

        chart_container = QWidget()

        self.chart_layout = QGridLayout(chart_container)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_layout.setSpacing(16)

        self.grade_chart = AnalyticsChart(
            "Grade Distribution"
        )

        self.subject_chart = AnalyticsChart(
            "Subject Performance"
        )

        self.class_chart = AnalyticsChart(
            "Class Performance"
        )

        self.top_chart = AnalyticsChart(
            "Top Performers"
        )

        self.chart_layout.addWidget(
            self.grade_chart, 0, 0
        )

        self.chart_layout.addWidget(
            self.subject_chart, 0, 1
        )

        self.chart_layout.addWidget(
            self.class_chart, 1, 0
        )

        self.chart_layout.addWidget(
            self.top_chart, 1, 1
        )

        self.chart_scroll.setWidget(chart_container)

        main_layout.addWidget(self.chart_scroll, 1)

        self.setStyleSheet("""
            QWidget {
                color: #E2E8F0;
                font-family: Segoe UI;
            }

            QLabel#PageHeading {
                color: #F1F5F9;
                font-size: 23px;
                font-weight: bold;
            }

            QLabel#PageDescription {
                color: #8492A6;
                font-size: 12px;
            }

            QLabel#FilterLabel {
                color: #A8B3C7;
                font-weight: bold;
            }

            QFrame#FilterFrame {
                background-color: #171D29;
                border: 1px solid #293548;
                border-radius: 10px;
            }

            QFrame#AnalyticsChart {
                background-color: #171D29;
                border: 1px solid #293548;
                border-radius: 12px;
            }

            QLabel#ChartTitle {
                color: #F1F5F9;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                border: none;
            }

            QComboBox {
                background-color: #202B3B;
                color: #E2E8F0;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 8px;
            }

            QPushButton {
                background-color: #263448;
                color: #E2E8F0;
                border: none;
                border-radius: 7px;
                padding: 10px 16px;
            }

            QPushButton:hover {
                background-color: #34465E;
            }

            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

    def create_summary_card(self, title, value, accent):

        card = QFrame()
        card.setObjectName("SummaryCard")
        card.setMinimumHeight(105)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(7)

        title_label = QLabel(title)
        title_label.setObjectName("SummaryTitle")

        value_label = QLabel(value)
        value_label.setObjectName("SummaryValue")
        value_label.setStyleSheet(
            f"color: {accent}; font-size: 25px; font-weight: bold;"
        )

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.value_label = value_label

        card.setStyleSheet("""
            QFrame#SummaryCard {
                background-color: #171D29;
                border: 1px solid #293548;
                border-radius: 10px;
            }

            QLabel#SummaryTitle {
                color: #8492A6;
                font-size: 12px;
                background: transparent;
                border: none;
            }

            QLabel#SummaryValue {
                background: transparent;
                border: none;
            }
        """)

        return card

    def load_filter_options(self):

        self.class_filter.blockSignals(True)
        self.exam_filter.blockSignals(True)
        self.session_filter.blockSignals(True)

        current_class = self.class_filter.currentText()
        current_exam = self.exam_filter.currentText()
        current_session = self.session_filter.currentText()

        self.class_filter.clear()
        self.class_filter.addItem("All Classes")
        self.class_filter.addItems(
            StudentController.get_all_classes()
        )

        self.exam_filter.clear()
        self.exam_filter.addItem("All Exams")
        self.exam_filter.addItems(
            GradeController.get_available_exam_types()
        )

        self.session_filter.clear()
        self.session_filter.addItem("All Sessions")
        self.session_filter.addItems(
            GradeController.get_available_sessions()
        )

        for combo, previous in (
            (self.class_filter, current_class),
            (self.exam_filter, current_exam),
            (self.session_filter, current_session)
        ):
            index = combo.findText(previous)

            if index >= 0:
                combo.setCurrentIndex(index)

            combo.blockSignals(False)

    def get_filters(self):

        selected_class = self.class_filter.currentText()
        selected_exam = self.exam_filter.currentText()
        selected_session = self.session_filter.currentText()

        return {
            "class_name": (
                None if selected_class == "All Classes"
                else selected_class
            ),
            "exam_type": (
                None if selected_exam == "All Exams"
                else selected_exam
            ),
            "academic_session": (
                None if selected_session == "All Sessions"
                else selected_session
            )
        }

    def load_analytics(self, *args):

        try:

            filters = self.get_filters()

            summary = AnalyticsService.get_dashboard_summary(
                class_name=filters["class_name"],
                exam_type=filters["exam_type"],
                academic_session=filters["academic_session"]
            )

            self.update_summary_cards(summary)

            self.plot_grade_distribution(filters)
            self.plot_subject_performance(filters)
            self.plot_class_performance(filters)
            self.plot_top_performers(filters)

        except Exception as error:

            QMessageBox.critical(
                self,
                "Analytics Error",
                str(error)
            )

    def update_summary_cards(self, summary):

        self.total_students_card.value_label.setText(
            str(summary.get("total_students", 0))
        )

        self.total_subjects_card.value_label.setText(
            str(summary.get("total_subjects", 0))
        )

        self.average_card.value_label.setText(
            f"{summary.get('class_average', 0):.2f}%"
        )

        self.pass_card.value_label.setText(
            f"{summary.get('pass_percentage', 0):.2f}%"
        )

    def plot_grade_distribution(self, filters):

        chart = self.grade_chart
        chart.clear_chart()

        ax = chart.figure.add_subplot(111)

        distribution = AnalyticsService.get_grade_distribution(
            class_name=filters["class_name"],
            exam_type=filters["exam_type"],
            academic_session=filters["academic_session"]
        )

        if not distribution:

            ax.text(
                0.5, 0.5,
                "No grade data available",
                color="#A8B3C7",
                ha="center",
                va="center",
                transform=ax.transAxes
            )

            ax.set_axis_off()

        else:

            labels = list(distribution.keys())
            values = list(distribution.values())

            ax.bar(
                labels,
                values,
                color="#22D3EE",
                width=0.55
            )

            ax.set_ylabel(
                "Number of Grades",
                color="#A8B3C7"
            )

            ax.tick_params(colors="#A8B3C7")

            ax.set_facecolor("#171D29")

            for spine in ax.spines.values():
                spine.set_color("#344155")

        chart.finish_chart()

    def plot_subject_performance(self, filters):

        chart = self.subject_chart
        chart.clear_chart()

        ax = chart.figure.add_subplot(111)

        records = AnalyticsService.get_subject_performance(
            class_name=filters["class_name"],
            exam_type=filters["exam_type"],
            academic_session=filters["academic_session"]
        )

        if not records:

            ax.text(
                0.5, 0.5,
                "No subject data available",
                color="#A8B3C7",
                ha="center",
                va="center",
                transform=ax.transAxes
            )

            ax.set_axis_off()

        else:

            labels = [
                record["subject_code"]
                for record in records
            ]

            values = [
                record["average_percentage"]
                for record in records
            ]

            ax.barh(
                labels,
                values,
                color="#A78BFA"
            )

            ax.set_xlabel(
                "Average Percentage",
                color="#A8B3C7"
            )

            ax.set_xlim(0, 100)
            ax.tick_params(colors="#A8B3C7")
            ax.set_facecolor("#171D29")

            for spine in ax.spines.values():
                spine.set_color("#344155")

        chart.finish_chart()

    def plot_class_performance(self, filters):

        chart = self.class_chart
        chart.clear_chart()

        ax = chart.figure.add_subplot(111)

        records = AnalyticsService.get_class_performance(
            exam_type=filters["exam_type"],
            academic_session=filters["academic_session"]
        )

        if filters["class_name"]:
            records = [
                record for record in records
                if record["class_name"] == filters["class_name"]
            ]

        if not records:

            ax.text(
                0.5, 0.5,
                "No class data available",
                color="#A8B3C7",
                ha="center",
                va="center",
                transform=ax.transAxes
            )

            ax.set_axis_off()

        else:

            labels = [
                record["class_name"]
                for record in records
            ]

            values = [
                record["average_percentage"]
                for record in records
            ]

            ax.bar(
                labels,
                values,
                color="#34D399"
            )

            ax.set_ylabel(
                "Average Percentage",
                color="#A8B3C7"
            )

            ax.set_ylim(0, 100)
            ax.tick_params(colors="#A8B3C7")
            ax.set_facecolor("#171D29")

            for spine in ax.spines.values():
                spine.set_color("#344155")

        chart.finish_chart()

    def plot_top_performers(self, filters):

        chart = self.top_chart
        chart.clear_chart()

        ax = chart.figure.add_subplot(111)

        records = AnalyticsService.get_top_performers(
            limit=5,
            class_name=filters["class_name"],
            exam_type=filters["exam_type"],
            academic_session=filters["academic_session"]
        )

        if not records:

            ax.text(
                0.5, 0.5,
                "No performer data available",
                color="#A8B3C7",
                ha="center",
                va="center",
                transform=ax.transAxes
            )

            ax.set_axis_off()

        else:

            labels = [
                record["student_name"]
                for record in records
            ]

            values = [
                record["percentage"]
                for record in records
            ]

            ax.barh(
                labels[::-1],
                values[::-1],
                color="#FBBF24"
            )

            ax.set_xlabel(
                "Percentage",
                color="#A8B3C7"
            )

            ax.set_xlim(0, 100)
            ax.tick_params(colors="#A8B3C7")
            ax.set_facecolor("#171D29")

            for spine in ax.spines.values():
                spine.set_color("#344155")

        chart.finish_chart()

    def refresh_analytics(self):

        self.load_filter_options()
        self.load_analytics()
