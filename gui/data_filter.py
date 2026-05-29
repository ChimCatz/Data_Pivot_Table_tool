from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QHBoxLayout
)

from PySide6.QtCore import Qt

from config import APP_ICON_PATH
from gui.styles import WINDOW_STYLE, button_style


COUNTRY_PRESETS = {
    "SEA only": {
        "Indonesia",
        "ID",
        "Philippines",
        "PH",
        "Thailand",
        "TH",
        "Singapore",
        "SG",
        "Malaysia",
        "MY",
        "Vietnam",
        "VN",
    },
    "AUNZ only": {
        "Australia",
        "AU",
        "New Zealand",
        "NZ",
    },
    "APAC (SEA + AUNZ)": {
        "Indonesia",
        "ID",
        "Philippines",
        "PH",
        "Thailand",
        "TH",
        "Singapore",
        "SG",
        "Malaysia",
        "MY",
        "Vietnam",
        "VN",
        "Australia",
        "AU",
        "New Zealand",
        "NZ",
    },
}

DECISION_MAKER_VALUES = {
    "C-Level",
    "Director",
    "Manager",
    "Vice President",
}


def normalize_values(values):
    return {value.casefold().strip() for value in values}


class DataFilterWindow(QWidget):

    def __init__(
        self,
        df,
        mapping,
        proceed_callback,
        back_to_import_callback,
        back_to_mapping_callback,
        initial_filters=None
    ):
        super().__init__()

        self.df = df
        self.mapping = mapping
        self.proceed_callback = proceed_callback
        self.back_to_import_callback = back_to_import_callback
        self.back_to_mapping_callback = back_to_mapping_callback
        self.initial_filters = initial_filters or {}
        self.on_close_callback = None

        self.setWindowTitle("Filter Data")
        self.setFixedSize(780, 470)
        self.setStyleSheet(WINDOW_STYLE)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))

        main_layout = QVBoxLayout()
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)

        nav_layout = QHBoxLayout()
        nav_layout.addStretch()

        self.back_to_import_btn = QPushButton("Back to Import")
        self.back_to_import_btn.setStyleSheet(button_style("nav_import"))
        self.back_to_import_btn.clicked.connect(self.go_back_to_import)
        nav_layout.addWidget(self.back_to_import_btn)

        self.back_to_mapping_btn = QPushButton("Back to Mapping")
        self.back_to_mapping_btn.setStyleSheet(button_style("nav_mapping"))
        self.back_to_mapping_btn.clicked.connect(self.go_back_to_mapping)
        nav_layout.addWidget(self.back_to_mapping_btn)

        main_layout.addLayout(nav_layout)

        title = QLabel("Select Values to INCLUDE")
        title.setStyleSheet("font-size:12pt; font-weight:bold;")
        main_layout.addWidget(title)

        self.tabs = QTabWidget()
        self.lists = {}

        for field, col in mapping.items():

            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.setSpacing(5)

            list_widget = QListWidget()

            values = (
                df[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .unique()
            )
            initial_allowed = self.initial_filters.get(field)
            normalized_initial = (
                normalize_values(initial_allowed)
                if initial_allowed is not None
                else None
            )

            for val in sorted(values, key=str.casefold):
                item = QListWidgetItem(val)
                is_checked = (
                    True
                    if normalized_initial is None
                    else val.casefold().strip() in normalized_initial
                )
                item.setCheckState(Qt.Checked if is_checked else Qt.Unchecked)
                list_widget.addItem(item)

            header_layout = QHBoxLayout()

            label = QLabel(field)
            label.setStyleSheet("font-weight:bold;")
            header_layout.addWidget(label)

            if field == "Country":
                for preset_name in COUNTRY_PRESETS:
                    preset_btn = QPushButton(preset_name)
                    preset_btn.setMinimumHeight(32)
                    preset_btn.setStyleSheet(button_style("primary"))
                    preset_btn.clicked.connect(
                        lambda checked=False, lw=list_widget, preset=preset_name:
                        self.apply_named_preset(lw, COUNTRY_PRESETS[preset])
                    )
                    header_layout.addWidget(preset_btn)

            if field == "Job Level":
                preset_btn = QPushButton("Decision Makers")
                preset_btn.setMinimumHeight(32)
                preset_btn.setStyleSheet(button_style("warning"))
                preset_btn.clicked.connect(
                    lambda checked=False, lw=list_widget:
                    self.apply_named_preset(lw, DECISION_MAKER_VALUES)
                )
                header_layout.addWidget(preset_btn)

            header_layout.addStretch()
            tab_layout.addLayout(header_layout)
            tab_layout.addWidget(list_widget)

            btn_layout = QHBoxLayout()

            select_all = QPushButton("Select All")
            unselect_all = QPushButton("Unselect All")
            select_all.setStyleSheet(button_style("success"))
            unselect_all.setStyleSheet(button_style("accent"))

            btn_layout.addWidget(select_all)
            btn_layout.addWidget(unselect_all)

            tab_layout.addLayout(btn_layout)

            select_all.clicked.connect(
                lambda checked=False, lw=list_widget: self.set_all(lw, True)
            )

            unselect_all.clicked.connect(
                lambda checked=False, lw=list_widget: self.set_all(lw, False)
            )

            tab.setLayout(tab_layout)

            self.tabs.addTab(tab, field)
            self.lists[field] = list_widget

        main_layout.addWidget(self.tabs)

        self.apply_btn = QPushButton("Apply Filter")
        self.apply_btn.setStyleSheet(button_style("primary"))
        self.apply_btn.clicked.connect(self.apply_filter)

        main_layout.addWidget(self.apply_btn)

        self.setLayout(main_layout)

    def go_back_to_import(self):

        self.back_to_import_callback()

    def go_back_to_mapping(self):

        self.back_to_mapping_callback()

    def closeEvent(self, event):

        super().closeEvent(event)

        if event.isAccepted() and self.on_close_callback:
            self.on_close_callback()

    def set_all(self, list_widget, state):

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setCheckState(
                Qt.Checked if state else Qt.Unchecked
            )

    def apply_named_preset(self, list_widget, allowed_values):

        normalized_allowed = normalize_values(allowed_values)

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setCheckState(
                Qt.Checked
                if item.text().casefold().strip() in normalized_allowed
                else Qt.Unchecked
            )

    def apply_filter(self):

        filtered_df = self.df.copy()
        selected_filters = {}

        for field, col in self.mapping.items():

            list_widget = self.lists[field]

            allowed = []

            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if item.checkState() == Qt.Checked:
                    allowed.append(item.text())

            selected_filters[field] = allowed

            filtered_df = filtered_df[
                filtered_df[col]
                .astype(str)
                .str.strip()
                .isin(allowed)
            ]

        self.proceed_callback(
            filtered_df,
            self.mapping,
            self.df,
            selected_filters
        )
        self.close()
