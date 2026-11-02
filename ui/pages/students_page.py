
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QFrame,
    QDialog,
    QFormLayout,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt

from controllers.student_controller import StudentController
from models.student import Student
from ui.components.data_table import DataTable


class StudentFormDialog(QDialog):

    def __init__(self, student=None, parent=None):
        super().__init__(parent)

        self.student = student

        self.setWindowTitle(
            "Edit Student" if student else "Add New Student"
        )
        self.setMinimumWidth(430)

        self.setup_ui()

        if student:
            self.load_student_data()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        title = QLabel(
            "Edit Student Details" if self.student
            else "Register New Student"
        )
        title.setObjectName("DialogTitle")

        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)

        self.roll_input = QLineEdit()
        self.roll_input.setPlaceholderText("Enter roll number")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter full name")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")

        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("e.g. B.Tech CSE AI")

        self.section_input = QLineEdit()
        self.section_input.setPlaceholderText("e.g. A")

        form.addRow("Roll Number", self.roll_input)
        form.addRow("Full Name", self.name_input)
        form.addRow("Email", self.email_input)
        form.addRow("Class", self.class_input)
        form.addRow("Section", self.section_input)

        layout.addLayout(form)

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

            QLineEdit {
                background-color: #202B3B;
                color: #F1F5F9;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 10px;
                min-height: 18px;
            }

            QLineEdit:focus {
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

    def load_student_data(self):

        self.roll_input.setText(self.student.roll_number)
        self.name_input.setText(self.student.name)
        self.email_input.setText(self.student.email or "")
        self.class_input.setText(self.student.class_name)
        self.section_input.setText(self.student.section or "")

    def validate_and_accept(self):

        if not self.roll_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Roll number is required."
            )
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Student name is required."
            )
            return

        if not self.class_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Class name is required."
            )
            return

        email = self.email_input.text().strip()

        if email and "@" not in email:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Please enter a valid email address."
            )
            return

        self.accept()

    def get_student_data(self):

        return Student(
            roll_number=self.roll_input.text().strip(),
            name=self.name_input.text().strip(),
            email=self.email_input.text().strip() or None,
            class_name=self.class_input.text().strip(),
            section=self.section_input.text().strip() or None
        )


class StudentsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_students()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 22, 28, 25)
        main_layout.setSpacing(20)

        # Page Heading
        heading_layout = QHBoxLayout()

        heading = QLabel("Student Management")
        heading.setObjectName("PageHeading")

        description = QLabel(
            "Manage student records and academic information"
        )
        description.setObjectName("PageDescription")

        heading_left = QVBoxLayout()
        heading_left.setSpacing(5)
        heading_left.addWidget(heading)
        heading_left.addWidget(description)

        heading_layout.addLayout(heading_left)
        heading_layout.addStretch()

        self.add_button = QPushButton("+  Add Student")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_student)

        heading_layout.addWidget(self.add_button)

        main_layout.addLayout(heading_layout)

        # Search and Filters
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")

        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(14, 12, 14, 12)
        filter_layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by name, roll number or email..."
        )
        self.search_input.setMinimumHeight(38)
        self.search_input.textChanged.connect(
            self.load_students
        )

        self.class_filter = QComboBox()
        self.class_filter.setMinimumHeight(38)
        self.class_filter.addItem("All Classes")
        self.class_filter.currentIndexChanged.connect(
            self.load_students
        )

        self.refresh_button = QPushButton("↻ Refresh")
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.clicked.connect(
            self.refresh_data
        )

        filter_layout.addWidget(self.search_input, 3)
        filter_layout.addWidget(self.class_filter, 1)
        filter_layout.addWidget(self.refresh_button)

        main_layout.addWidget(filter_frame)

        # Student Table
        self.table = DataTable([
            "ID",
            "Roll Number",
            "Student Name",
            "Email",
            "Class",
            "Section"
        ])

        self.table.setMinimumHeight(350)
        self.table.set_column_hidden(0, True)

        main_layout.addWidget(self.table)

        # Bottom Actions
        bottom_layout = QHBoxLayout()

        self.count_label = QLabel("Showing 0 students")
        self.count_label.setObjectName("CountLabel")

        bottom_layout.addWidget(self.count_label)
        bottom_layout.addStretch()

        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")

        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)

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

    def load_students(self, *args):

        search = self.search_input.text().strip()

        selected_class = self.class_filter.currentText()

        class_name = (
            None if selected_class == "All Classes"
            else selected_class
        )

        try:
            students = StudentController.get_all_students(
                search=search or None,
                class_name=class_name
            )

            rows = [
                [
                    student.student_id,
                    student.roll_number,
                    student.name,
                    student.email or "",
                    student.class_name,
                    student.section or ""
                ]
                for student in students
            ]

            self.table.load_data(rows)

            self.count_label.setText(
                f"Showing {len(students)} students"
            )

            self.update_class_filter()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

    def update_class_filter(self):

        current_class = self.class_filter.currentText()

        classes = StudentController.get_all_classes()

        self.class_filter.blockSignals(True)

        self.class_filter.clear()
        self.class_filter.addItem("All Classes")
        self.class_filter.addItems(classes)

        index = self.class_filter.findText(current_class)

        if index >= 0:
            self.class_filter.setCurrentIndex(index)

        self.class_filter.blockSignals(False)

    def refresh_data(self):

        self.search_input.clear()
        self.class_filter.setCurrentIndex(0)
        self.load_students()

    def add_student(self):

        dialog = StudentFormDialog(parent=self)

        if dialog.exec_() == QDialog.Accepted:

            try:
                student = dialog.get_student_data()

                StudentController.add_student(student)

                QMessageBox.information(
                    self,
                    "Success",
                    "Student registered successfully."
                )

                self.load_students()

            except (ValueError, Exception) as error:

                QMessageBox.warning(
                    self,
                    "Unable to Add Student",
                    str(error)
                )

    def edit_student(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a student to edit."
            )
            return

        student_id = int(row[0])

        student = StudentController.get_student_by_id(
            student_id
        )

        if not student:
            QMessageBox.warning(
                self,
                "Not Found",
                "Student record no longer exists."
            )
            self.load_students()
            return

        dialog = StudentFormDialog(
            student=student,
            parent=self
        )

        if dialog.exec_() == QDialog.Accepted:

            try:
                updated_student = dialog.get_student_data()

                StudentController.update_student(
                    student_id,
                    updated_student
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Student details updated successfully."
                )

                self.load_students()

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Update Failed",
                    str(error)
                )

    def delete_student(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a student to delete."
            )
            return

        student_id = int(row[0])
        student_name = row[2]

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {student_name}?\n\n"
            "Associated grade records will also be deleted.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        try:
            StudentController.delete_student(student_id)

            QMessageBox.information(
                self,
                "Deleted",
                "Student record deleted successfully."
            )

            self.load_students()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Deletion Failed",
                str(error)
            )
