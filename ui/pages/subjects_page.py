
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QDoubleSpinBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QFrame
)
from PyQt5.QtCore import Qt

from controllers.subject_controller import SubjectController
from models.subject import Subject
from ui.components.data_table import DataTable


class SubjectFormDialog(QDialog):

    def __init__(self, subject=None, parent=None):
        super().__init__(parent)

        self.subject = subject

        self.setWindowTitle(
            "Edit Subject" if subject else "Add New Subject"
        )
        self.setMinimumWidth(430)

        self.setup_ui()

        if subject:
            self.load_subject_data()

    def setup_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 20)
        layout.setSpacing(16)

        title = QLabel(
            "Edit Subject Details" if self.subject
            else "Create New Subject"
        )
        title.setObjectName("DialogTitle")

        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(14)

        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g. CS101")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter subject name")

        self.marks_input = QDoubleSpinBox()
        self.marks_input.setRange(1, 10000)
        self.marks_input.setDecimals(2)
        self.marks_input.setValue(100)
        self.marks_input.setSuffix(" marks")

        self.credits_input = QDoubleSpinBox()
        self.credits_input.setRange(0.1, 100)
        self.credits_input.setDecimals(2)
        self.credits_input.setSingleStep(0.5)
        self.credits_input.setValue(3)

        form.addRow("Subject Code", self.code_input)
        form.addRow("Subject Name", self.name_input)
        form.addRow("Maximum Marks", self.marks_input)
        form.addRow("Subject Credits", self.credits_input)

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

            QLineEdit, QDoubleSpinBox {
                background-color: #202B3B;
                color: #F1F5F9;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 9px;
                min-height: 18px;
            }

            QLineEdit:focus, QDoubleSpinBox:focus {
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

    def load_subject_data(self):

        self.code_input.setText(self.subject.subject_code)
        self.name_input.setText(self.subject.subject_name)
        self.marks_input.setValue(float(self.subject.max_marks))
        self.credits_input.setValue(float(self.subject.credits))

    def validate_and_accept(self):

        if not self.code_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Subject code is required."
            )
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(
                self,
                "Validation Error",
                "Subject name is required."
            )
            return

        self.accept()

    def get_subject_data(self):

        return Subject(
            subject_code=self.code_input.text().strip(),
            subject_name=self.name_input.text().strip(),
            max_marks=self.marks_input.value(),
            credits=self.credits_input.value()
        )


class SubjectsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_subjects()

    def setup_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(28, 22, 28, 25)
        main_layout.setSpacing(20)

        # Page Heading
        heading_layout = QHBoxLayout()

        heading_left = QVBoxLayout()
        heading_left.setSpacing(5)

        heading = QLabel("Subject Management")
        heading.setObjectName("PageHeading")

        description = QLabel(
            "Manage subjects, maximum marks and credit allocation"
        )
        description.setObjectName("PageDescription")

        heading_left.addWidget(heading)
        heading_left.addWidget(description)

        heading_layout.addLayout(heading_left)
        heading_layout.addStretch()

        self.add_button = QPushButton("+  Add Subject")
        self.add_button.setObjectName("PrimaryButton")
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_subject)

        heading_layout.addWidget(self.add_button)

        main_layout.addLayout(heading_layout)

        # Search Section
        filter_frame = QFrame()
        filter_frame.setObjectName("FilterFrame")

        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setContentsMargins(14, 12, 14, 12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by subject name or subject code..."
        )
        self.search_input.setMinimumHeight(38)

        self.search_input.textChanged.connect(
            self.load_subjects
        )

        self.refresh_button = QPushButton("↻ Refresh")
        self.refresh_button.setCursor(Qt.PointingHandCursor)
        self.refresh_button.clicked.connect(
            self.refresh_data
        )

        filter_layout.addWidget(self.search_input, 1)
        filter_layout.addWidget(self.refresh_button)

        main_layout.addWidget(filter_frame)

        # Subject Table
        self.table = DataTable([
            "ID",
            "Subject Code",
            "Subject Name",
            "Maximum Marks",
            "Credits"
        ])

        self.table.setMinimumHeight(350)
        self.table.set_column_hidden(0, True)

        main_layout.addWidget(self.table)

        # Bottom Actions
        bottom_layout = QHBoxLayout()

        self.count_label = QLabel("Showing 0 subjects")
        self.count_label.setObjectName("CountLabel")

        bottom_layout.addWidget(self.count_label)
        bottom_layout.addStretch()

        self.edit_button = QPushButton("Edit Selected")
        self.delete_button = QPushButton("Delete Selected")

        self.edit_button.clicked.connect(self.edit_subject)
        self.delete_button.clicked.connect(self.delete_subject)

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

            QLineEdit {
                background-color: #202B3B;
                color: #E2E8F0;
                border: 1px solid #344155;
                border-radius: 7px;
                padding: 8px;
            }

            QLineEdit:focus {
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

    def load_subjects(self, *args):

        search = self.search_input.text().strip()

        try:
            subjects = SubjectController.get_all_subjects(
                search=search or None
            )

            rows = [
                [
                    subject.subject_id,
                    subject.subject_code,
                    subject.subject_name,
                    subject.max_marks,
                    subject.credits
                ]
                for subject in subjects
            ]

            self.table.load_data(rows)

            self.count_label.setText(
                f"Showing {len(subjects)} subjects"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Database Error",
                str(error)
            )

    def refresh_data(self):

        self.search_input.clear()
        self.load_subjects()

    def add_subject(self):

        dialog = SubjectFormDialog(parent=self)

        if dialog.exec_() == QDialog.Accepted:

            try:
                subject = dialog.get_subject_data()

                SubjectController.add_subject(subject)

                QMessageBox.information(
                    self,
                    "Success",
                    "Subject added successfully."
                )

                self.load_subjects()

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Unable to Add Subject",
                    str(error)
                )

    def edit_subject(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a subject to edit."
            )
            return

        subject_id = int(row[0])

        subject = SubjectController.get_subject_by_id(
            subject_id
        )

        if not subject:
            QMessageBox.warning(
                self,
                "Not Found",
                "Subject record no longer exists."
            )
            self.load_subjects()
            return

        dialog = SubjectFormDialog(
            subject=subject,
            parent=self
        )

        if dialog.exec_() == QDialog.Accepted:

            try:
                updated_subject = dialog.get_subject_data()

                SubjectController.update_subject(
                    subject_id,
                    updated_subject
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Subject updated successfully."
                )

                self.load_subjects()

            except Exception as error:

                QMessageBox.warning(
                    self,
                    "Update Failed",
                    str(error)
                )

    def delete_subject(self):

        row = self.table.get_selected_row()

        if not row:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a subject to delete."
            )
            return

        subject_id = int(row[0])
        subject_name = row[2]

        confirmation = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {subject_name}?\n\n"
            "Associated grade records will also be deleted.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmation != QMessageBox.Yes:
            return

        try:
            SubjectController.delete_subject(subject_id)

            QMessageBox.information(
                self,
                "Deleted",
                "Subject deleted successfully."
            )

            self.load_subjects()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Deletion Failed",
                str(error)
            )
