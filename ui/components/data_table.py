
from PyQt5.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QMenu
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class DataTable(QTableWidget):

    def __init__(
        self,
        headers=None,
        parent=None
    ):
        super().__init__(parent)

        self.headers = headers or []

        self.setup_ui()

        if self.headers:
            self.set_headers(self.headers)

    def setup_ui(self):

        self.setObjectName("DataTable")

        self.setAlternatingRowColors(True)

        self.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.setSortingEnabled(True)

        self.setShowGrid(False)

        self.verticalHeader().setVisible(False)

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.horizontalHeader().setHighlightSections(False)

        self.setFocusPolicy(Qt.NoFocus)

        self.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.customContextMenuRequested.connect(
            self.show_context_menu
        )

        self.setStyleSheet("""
            QTableWidget#DataTable {
                background-color: #171D29;
                alternate-background-color: #1C2533;
                color: #E2E8F0;
                border: 1px solid #293548;
                border-radius: 10px;
                gridline-color: transparent;
                font-size: 13px;
                selection-background-color: #164E63;
                selection-color: #FFFFFF;
                outline: none;
            }

            QHeaderView::section {
                background-color: #202B3B;
                color: #A8B3C7;
                padding: 13px 10px;
                border: none;
                border-bottom: 1px solid #344155;
                font-size: 12px;
                font-weight: 600;
            }

            QTableWidget::item {
                padding: 10px;
                border: none;
            }

            QTableWidget::item:selected {
                background-color: #164E63;
                color: #FFFFFF;
            }

            QTableWidget QScrollBar:vertical {
                background: #171D29;
                width: 8px;
                margin: 0px;
            }

            QTableWidget QScrollBar::handle:vertical {
                background: #475569;
                min-height: 25px;
                border-radius: 4px;
            }

            QTableWidget QScrollBar::add-line:vertical,
            QTableWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }

            QTableWidget QScrollBar:horizontal {
                background: #171D29;
                height: 8px;
                margin: 0px;
            }

            QTableWidget QScrollBar::handle:horizontal {
                background: #475569;
                min-width: 25px;
                border-radius: 4px;
            }

            QTableWidget QScrollBar::add-line:horizontal,
            QTableWidget QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)

    def set_headers(self, headers):

        self.headers = headers

        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)

    def load_data(self, rows):

        self.setSortingEnabled(False)

        self.setRowCount(0)

        for row_data in rows:

            row_position = self.rowCount()

            self.insertRow(row_position)

            for column, value in enumerate(row_data):

                item = QTableWidgetItem(
                    "" if value is None else str(value)
                )

                item.setTextAlignment(
                    Qt.AlignVCenter | Qt.AlignLeft
                )

                self.setItem(
                    row_position,
                    column,
                    item
                )

        self.setSortingEnabled(True)

    def add_row(self, row_data):

        self.setSortingEnabled(False)

        row_position = self.rowCount()

        self.insertRow(row_position)

        for column, value in enumerate(row_data):

            item = QTableWidgetItem(
                "" if value is None else str(value)
            )

            item.setTextAlignment(
                Qt.AlignVCenter | Qt.AlignLeft
            )

            self.setItem(
                row_position,
                column,
                item
            )

        self.setSortingEnabled(True)

    def update_row(self, row_position, row_data):

        if not 0 <= row_position < self.rowCount():
            return

        for column, value in enumerate(row_data):

            if column >= self.columnCount():
                break

            item = self.item(row_position, column)

            if item is None:
                item = QTableWidgetItem()

                self.setItem(
                    row_position,
                    column,
                    item
                )

            item.setText(
                "" if value is None else str(value)
            )

    def delete_selected_row(self):

        selected_row = self.currentRow()

        if selected_row >= 0:
            self.removeRow(selected_row)
            return True

        return False

    def get_selected_row(self):

        selected_row = self.currentRow()

        if selected_row < 0:
            return None

        row_data = []

        for column in range(self.columnCount()):

            item = self.item(selected_row, column)

            row_data.append(
                item.text() if item else ""
            )

        return row_data

    def get_selected_row_index(self):

        selected_row = self.currentRow()

        if selected_row < 0:
            return None

        return selected_row

    def clear_data(self):

        self.setRowCount(0)

    def set_column_width(self, column, width):

        if 0 <= column < self.columnCount():

            self.horizontalHeader().setSectionResizeMode(
                column,
                QHeaderView.Interactive
            )

            self.setColumnWidth(column, width)

    def set_column_hidden(self, column, hidden=True):

        if 0 <= column < self.columnCount():
            self.setColumnHidden(column, hidden)

    def set_cell_color(
        self,
        row,
        column,
        color
    ):

        item = self.item(row, column)

        if item:
            item.setForeground(QColor(color))

    def set_cell_background(
        self,
        row,
        column,
        color
    ):

        item = self.item(row, column)

        if item:
            item.setBackground(QColor(color))

    def show_context_menu(self, position):

        selected_row = self.currentRow()

        if selected_row < 0:
            return

        menu = QMenu(self)

        menu.setStyleSheet("""
            QMenu {
                background-color: #202B3B;
                color: #E2E8F0;
                border: 1px solid #344155;
                padding: 5px;
            }

            QMenu::item {
                padding: 7px 22px;
                border-radius: 4px;
            }

            QMenu::item:selected {
                background-color: #164E63;
            }
        """)

        copy_action = menu.addAction("Copy Selected Row")

        action = menu.exec_(
            self.viewport().mapToGlobal(position)
        )

        if action == copy_action:

            row_data = self.get_selected_row()

            if row_data:
                from PyQt5.QtWidgets import QApplication

                QApplication.clipboard().setText(
                    "\t".join(row_data)
                )
