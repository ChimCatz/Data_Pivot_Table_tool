from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QMessageBox, QHBoxLayout
)

from config import APP_ICON_PATH
from gui.styles import WINDOW_STYLE, button_style


REQUIRED_FIELDS = ["Country", "Job Level", "Industry"]


class ColumnMapper(QWidget):

    def __init__(
        self,
        df,
        proceed_callback,
        back_to_import_callback,
        initial_mapping=None
    ):
        super().__init__()

        self.df = df
        self.proceed_callback = proceed_callback
        self.back_to_import_callback = back_to_import_callback
        self.initial_mapping = initial_mapping or {}
        self.on_close_callback = None

        self.setWindowTitle("Column Mapping")
        self.resize(300, 220)
        self.setStyleSheet(WINDOW_STYLE)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)

        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        self.back_to_import_btn = QPushButton("Back to Import")
        self.back_to_import_btn.setStyleSheet(button_style("nav_import"))
        self.back_to_import_btn.clicked.connect(self.go_back_to_import)
        nav_layout.addWidget(self.back_to_import_btn)

        layout.addLayout(nav_layout)

        self.dropdowns = {}

        columns = df.columns.tolist()

        for field in REQUIRED_FIELDS:

            label = QLabel(field)
            combo = QComboBox()
            combo.addItem("Select Column")
            combo.addItems(columns)
            combo.setMaximumHeight(24)

            auto_col = self.auto_detect(field, columns)
            if auto_col:
                combo.setCurrentText(auto_col)

            if field in self.initial_mapping and self.initial_mapping[field] in columns:
                combo.setCurrentText(self.initial_mapping[field])

            layout.addWidget(label)
            layout.addWidget(combo)

            self.dropdowns[field] = combo

        self.confirm_btn = QPushButton("Confirm Mapping")
        self.confirm_btn.setStyleSheet(button_style("success"))
        self.confirm_btn.clicked.connect(self.confirm_mapping)

        layout.addWidget(self.confirm_btn)

        self.setLayout(layout)

    def go_back_to_import(self):

        self.back_to_import_callback()

    def closeEvent(self, event):

        super().closeEvent(event)

        if event.isAccepted() and self.on_close_callback:
            self.on_close_callback()

    def auto_detect(self, field, columns):

        rules = {
            "Country": [
                "country",
                "country name",
                "country region",
                "geo country"
            ],
            "Job Level": [
                "job level",
                "seniority",
                "title",
                "position"
            ],
            "Industry": [
                "industry",
                "sector",
                "market",
                "vertical"
            ]
        }

        for col in columns:
            col_clean = col.lower().strip()

            for keyword in rules[field]:
                if col_clean == keyword:
                    return col

        for col in columns:
            col_clean = col.lower().strip()

            for keyword in rules[field]:
                if col_clean.startswith(keyword):
                    return col

        for col in columns:
            words = col.lower().replace("/", " ").split()

            for keyword in rules[field]:
                if keyword in words:
                    return col

        return None

    def confirm_mapping(self):

        mapping = {}

        for field, combo in self.dropdowns.items():

            selected = combo.currentText()

            if selected == "Select Column":
                QMessageBox.warning(
                    self,
                    "Missing Field",
                    f"{field} must be mapped."
                )
                return

            mapping[field] = selected

        self.proceed_callback(self.df, mapping)
        self.close()
