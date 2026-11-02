
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QFrame
)
from PyQt5.QtCore import Qt

from controllers.grade_controller import GradeController
from controllers.student_controller import StudentController
from controllers.subject_controller import SubjectController
from models.grade import Grade
from ui.components.data_table import DataTable


class MarksFormDialog(QDialog):

    def __init__(self, grade=None, parent=None):
        super().__init__(parent)

        self.grade = grade
        self.students = []
        self.subjects = []

        self.setWindowTitle(
            "Edit Marks" if grade else "Add Marks"
        )
        self.setMinimumWidth(450)

        self.setup_ui()
        self.load_dropdown_data()

        if grade:
            self.load_grade_data()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        title = QLabel(
            "Edit Examination Record" if self.grade
            else "Add Examination Record"
        )
        title.setObjectName("DialogTitle")

        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(13)

        self.student_combo = QComboBox()
        self.subject_combo = QComboBox()

        self.exam_combo = QComboBox()
        self.exam_combo.setEditable(True)
        self.exam_combo.addItems([
            "Internal Assessment",
            "Mid Term",
            "End Term",
            "Practical",
            "Assignment",
            "Quiz"
        ])

        self.session_input = QLineEdit()
        self.session_input.setPlaceholderText(
            "e.g. 2026-27"
        )

        self.marks_input = QDoubleSpinBox()
        self.marks_input.setRange(0, 10000)
        self.marks_input.setDecimals(2)
        self.marks_input.setSingleStep(1)

        self.max_marks_label = QLabel("Maximum Marks: 100")

        form.addRow("Student", self.student_combo)
        form.addRow("Subject", self.subject_combo)
        form.addRow("Exam Type", self.exam_combo)
        form.addRow("Academic Session", self.session_input)
        form.addRow("Marks Obtained", self.marks_input)
        form.addRow("", self.max_marks_label)

        layout.addLayout(form)

        self.subject_combo.currentIndexChanged.connect(
            self.update_max_marks
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.setStyleSheet("""
            QDialog {
                background-color: #171D29;
                color: #E2E8F0;
            }

            QLabel {
                color: #CBD5E1;
                font-size: 12px;
            }

            QLabel#DialogTitle {
                color: #F1F5F9;
                font-size: 20px;
                font-weight: bold;
            }

            QLineEdit, QComboBox, QDoubleSpinBox {
                background-color: #202B3B;
                color: #F1F5F9;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 9px;
                min-height: 18px;
            }

            QLineEdit:focus, QComboBox:focus,
            QDoubleSpinBox:focus {
                border: 1px solid #22D3EE;
            }

            QPushButton {
                background-color: #263448;
                color: #E2E8F0;
                border: none;
                border-radius: 7px;
                padding: 9px 18px;
                min-width: 75px;
            }

            QPushButton:hover {
                background-color: #34465E;
            }
        """)

    def load_dropdown_data(self):

        self.students = StudentController.get_all_students()
        self.subjects = SubjectController.get_all_subjects()

        self.student_combo.clear()

        for student in self.students:
            self.student_combo.addItem(
                f"{student.roll_number} - {student.name}",
                student.student_id
            )

        self.subject_combo.clear()

        for subject in self.subjects:
            self.subject_combo.addItem(
                f"{subject.subject_code} - {subject.subject_name}",
                subject.subject_id
            )

        self.update_max_marks()

    def update_max_marks(self, *args):

        subject_id = self.subject_combo.currentData()

        if subject_id is None:
            self.max_marks_label.setText(
                "Maximum Marks: Not available"
            )
            self.marks_input.setMaximum(10000)
            return

        subject = SubjectController.get_subject_by_id(
            subject_id
        )

        if subject:
            maximum = float(subject.max_marks)

            self.max_marks_label.setText(
                f"Maximum Marks: {maximum:g}"
            )

            self.marks_input.setMaximum(maximum)

    def load_grade_data(self):

        record = GradeController.get_grade_by_id(
            self.grade.grade_id
        )

        if not record:
            return

        student_index = self.student_combo.findData(
            record["student_id"]
        )

        subject_index = self.subject_combo.findData(
            record["subject_id"]
        )

        if student_index >= 0:
            self.student_combo.setCurrentIndex(student_index)

        if subject_index >= 0:
            self.subject_combo.setCurrentIndex(subject_index)

        self.exam_combo.setCurrentText(
            record["exam_type"]
        )

        self.session_input.setText(
            record["academic_session"]
        )

        self.marks_input.setValue(
            float(record["marks_obtained"])
        )

    def validate_and_accept(self):

        if self.student_combo.currentData() is None:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please add a student before entering marks."
            )
            return

        if self.subject_combo.currentData() is None:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please add a subject before entering marks."
            )
            return

        if not self.exam_combo.currentText().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Exam type is required."
            )
            return

        if not self.session_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Academic session is required."
            )
            return

        subject_id = self.subject_combo.currentData()

        subject = SubjectController.get_subject_by_id(
            subject_id
        )

        if subject and self.marks_input.value() > float(
            subject.max_marks
        ):
            QMessageBox.warning(
                self,
                "Invalid Marks",
                f"Marks cannot exceed {subject.max_marks}."
            )
            return

        self.accept()

    def get_grade_data(self):

        return Grade(
            student_id=self.student_combo.currentData(),
            subject_id=self.subject_combo.currentData(),
            marks_obtained=self.marks_input.value(),
            exam_type=self.exam_combo.currentText().strip(),
            academic_session=self.session_input.text().strip()
        )


class MarksPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_filter_options()
        self.load_marks()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 22, 28, 25)
        main_layout.setSpacing(20)

        # Page Heading
        heading_layout = QHBoxLayout()

        heading_left = QVBoxLayout()
        heading_left.setSpacing(5)

        heading = QLabel("Marks Management")
        heading.setObjectName("PageHeading")

        description = QLabel(
            "Record examination marks and manage academic results"
        )
        description.setObjectName("PageDescription")

        heading_left.addWidget(heading)
        heading_left.addWidget(description)

        heading_layout.addLayout(heading_left)
        heading_layout.addStretch()

        self.add_button = QPushButton("+  Add Marks")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_marks)

        heading_layout.addWidget(self.add_button)

        main_layout.addLayout(heading_layout)

        # Search and Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")

        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(14, 12, 14, 12)
        filter_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search student, roll number or subject..."
        )
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(
            self.load_marks
        )

        self.exam_filter = QComboBox()
        self.exam_filter.addItem("All Exams")
        self.exam_filter.currentIndexChanged.connect(
            self.load_marks
        )

        self.session_filter = QComboBox()
        self.session_filter.addItem("All Sessions")
        self.session_filter.currentIndexChanged.connect(
            self.load_marks
        )

        self.refresh_button = QPushButton("↻ Refresh")
        self.refresh_button.clicked.connect(
            self.refresh_data
        )

        filter_layout.addWidget(self.search_input, 3)
        filter_layout.addWidget(self.exam_filter, 1)
        filter_layout.addWidget(self.session_filter, 1)
        filter_layout.addWidget(self.refresh_button)

        main_layout.addWidget(filter_frame)

        # Marks Table
        self.table = DataTable([
            "ID",
            "Roll Number",
            "Student Name",
            "Subject Code",
            "Subject Name",
            "Exam Type",
            "Session",
            "Marks",
            "Maximum Marks",
            "Percentage"
        ])

        self.table.setMinimumHeight(350)
        self.table.set_column_hidden(0, True)

        main_layout.addWidget(self.table)

        # Bottom Actions
        bottom_layout = QHBoxLayout()

        self.count_label = QLabel("Showing 0 records")
        self.count_label.setObjectName("CountLabel")

        bottom_layout.addWidget(self.count_label)
        bottom_layout.addStretch()

        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")

        self.edit_button.clicked.connect(self.edit_marks)
        self.delete_button.clicked.connect(self.delete_marks)

        bottom_layout.addWidget(self.edit_button)
        bottom_layout.addWidget(self.delete_button)

        main_layout.addLayout(bottom_layout)

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

            QLabel#CountLabel {
                color: #8492A6;
                font-size: 12px;
            }

            QFrame#FilterFrame {
                background-color: #171D29;
                border: 1px solid #293548;
                border-radius: 10px;
            }

            QLineEdit, QComboBox {
                background-color: #202B3B;
                color: #E2E8F0;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 8px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #22D3EE;
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

            QPushButton#PrimaryButton {
                background-color: #0891B2;
                color: white;
                font-weight: bold;
            }

            QPushButton#PrimaryButton:hover {
                background-color: #0E7490;
            }
        """)

    def load_filter_options(self):

        self.exam_filter.blockSignals(True)
        self.session_filter.blockSignals(True)

        current_exam = self.exam_filter.currentText()
        current_session = self.session_filter.currentText()

        self.exam_filter.clear()
        self.exam_filter.addItem("All Exams")

        for exam in GradeController.get_available_exam_types():
            self.exam_filter.addItem(exam)

        self.session_filter.clear()
        self.session_filter.addItem("All Sessions")

        for session in GradeController.get_available_sessions():
            self.session_filter.addItem(session)

        exam_index = self.exam_filter.findText(current_exam)
        session_index = self.session_filter.findText(current_session)

        if exam_index >= 0:
            self.exam_filter.setCurrentIndex(exam_index)

        if session_index >= 0:
            self.session_filter.setCurrentIndex(session_index)

        self.exam_filter.blockSignals(False)
        self.session_filter.blockSignals(False)

    def load_marks(self, *args):

        search = self.search_input.text().strip()

        selected_exam = self.exam_filter.currentText()
        selected_session = self.session_filter.currentText()

        exam_type = (
            None if selected_exam == "All Exams"
            else selected_exam
        )

        academic_session = (
            None if selected_session == "All Sessions"
            else selected_session
        )

        try:

            records = GradeController.get_all_grades(
                search=search or None,
                exam_type=exam_type,
                academic_session=academic_session
            )

            rows = []

            for record in records:

                maximum = float(record["max_marks"])
                obtained = float(record["marks_obtained"])

                percentage = (
                    (obtained / maximum) * 100
                    if maximum > 0 else 0
                )

                rows.append([
                    record["grade_id"],
                    record["roll_number"],
                    record["student_name"],
                    record["subject_code"],
                    record["subject_name"],
                    record["exam_type"],
                    record["academic_session"],
                    f"{obtained:g}",
                    f"{maximum:g}",
                    f"{percentage:.2f}%"
                ])

            self.table.load_data(rows)

            self.count_label.setText(
                f"Showing {len(records)} records"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

    def refresh_data(self):

        self.search_input.clear()
        self.load_filter_options()
        self.load_marks()

    def add_marks(self):

        if not StudentController.get_all_students():
            QMessageBox.warning(
                self,
                "No Students",
                "Please register students before entering marks."
            )
            return

        if not SubjectController.get_all_subjects():
            QMessageBox.warning(
                self,
                "No Subjects",
                "Please add subjects before entering marks."
            )
            return

        dialog = MarksFormDialog(parent=self)

        if dialog.exec_() == QDialog.Accepted:

            try:

                grade = dialog.get_grade_data()

                GradeController.add_grade(grade)

                QMessageBox.information(
                    self,
                    "Success",
                    "Marks recorded successfully."
                )

                self.load_filter_options()
                self.load_marks()

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Unable to Save Marks",
                    str(error)
                )

    def edit_marks(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a marks record to edit."
            )
            return

        grade_id = int(row[0])

        grade = GradeController.get_grade_by_id(grade_id)

        if not grade:
            QMessageBox.warning(
                self,
                "Not Found",
                "Marks record no longer exists."
            )
            self.load_marks()
            return

        grade_model = Grade(
            student_id=grade["student_id"],
            subject_id=grade["subject_id"],
            marks_obtained=grade["marks_obtained"],
            exam_type=grade["exam_type"],
            academic_session=grade["academic_session"],
            grade_id=grade_id
        )

        dialog = MarksFormDialog(
            grade=grade_model,
            parent=self
        )

        if dialog.exec_() == QDialog.Accepted:

            try:

                updated_grade = dialog.get_grade_data()

                GradeController.update_grade(
                    grade_id,
                    updated_grade
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Marks updated successfully."
                )

                self.load_filter_options()
                self.load_marks()

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Update Failed",
                    str(error)
                )

    def delete_marks(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a marks record to delete."
            )
            return

        grade_id = int(row[0])

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this marks record?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        try:

            GradeController.delete_grade(grade_id)

            QMessageBox.information(
                self,
                "Deleted",
                "Marks record deleted successfully."
            )

            self.load_filter_options()
            self.load_marks()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Deletion Failed",
                str(error)
            )
