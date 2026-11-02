
from PyQt5.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget
)
from PyQt5.QtCore import Qt


class StatCard(QFrame):

    def __init__(
        self,
        title,
        value="0",
        subtitle="",
        icon="●",
        accent_color="#22D3EE",
        parent=None
    ):
        super().__init__(parent)

        self.title = title
        self.accent_color = accent_color

        self.setObjectName("StatCard")
        self.setMinimumHeight(145)

        self.setup_ui(
            value,
            subtitle,
            icon
        )

    def setup_ui(self, value, subtitle, icon):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 18, 20, 18)
        main_layout.setSpacing(12)

        # Top Section
        top_layout = QHBoxLayout()

        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("StatTitle")

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("StatIcon")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedSize(38, 38)

        top_layout.addWidget(self.title_label)
        top_layout.addStretch()
        top_layout.addWidget(self.icon_label)

        main_layout.addLayout(top_layout)

        # Main Value
        self.value_label = QLabel(str(value))
        self.value_label.setObjectName("StatValue")

        main_layout.addWidget(self.value_label)

        # Bottom Section
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("StatSubtitle")
        self.subtitle_label.setWordWrap(True)

        main_layout.addWidget(self.subtitle_label)

        # Accent Border
        self.setStyleSheet(f"""
            QFrame#StatCard {{
                background-color: #171D29;
                border: 1px solid #293548;
                border-left: 4px solid {self.accent_color};
                border-radius: 12px;
            }}

            QLabel#StatTitle {{
                color: #A8B3C7;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
                border: none;
            }}

            QLabel#StatValue {{
                color: #F1F5F9;
                font-size: 29px;
                font-weight: 700;
                background: transparent;
                border: none;
            }}

            QLabel#StatSubtitle {{
                color: #8492A6;
                font-size: 11px;
                background: transparent;
                border: none;
            }}

            QLabel#StatIcon {{
                color: {self.accent_color};
                background-color: #222D3D;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }}
        """)

    def set_value(self, value):

        self.value_label.setText(str(value))

    def set_subtitle(self, subtitle):

        self.subtitle_label.setText(str(subtitle))

    def set_stat(self, value, subtitle=None):

        self.set_value(value)

        if subtitle is not None:
            self.set_subtitle(subtitle)

    def set_title(self, title):

        self.title = title
        self.title_label.setText(title)
