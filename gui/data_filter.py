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

from gui.styles import WINDOW_STYLE, button_style


COUNTRY_PRESETS = {
    "SEA only": {
        "Indonesia",
        "Philippines",
        "Thailand",
        "Singapore",
        "Malaysia",
        "Vietnam",
    },
    "AUNZ only": {
        "Australia",
        "New Zealand",
    },
    "APAC (SEA + AUNZ)": {
        "Indonesia",
        "Philippines",
        "Thailand",
        "Singapore",
        "Malaysia",
        "Vietnam",
        "Australia",
        "New Zealand",
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

    def __init__(self, df, mapping, proceed_callback):
        super().__init__()

        self.df = df
        self.mapping = mapping
        self.proceed_callback = proceed_callback

        self.setWindowTitle("Filter Data")
        self.setFixedSize(780, 470)
        self.setStyleSheet(WINDOW_STYLE)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(8, 8, 8, 8)

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

            for val in sorted(values, key=str.casefold):
                item = QListWidgetItem(val)
                item.setCheckState(Qt.Checked)
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

        for field, col in self.mapping.items():

            list_widget = self.lists[field]

            allowed = []

            for i in range(list_widget.count()):
                item = list_widget.item(i)
                if item.checkState() == Qt.Checked:
                    allowed.append(item.text())

            filtered_df = filtered_df[
                filtered_df[col]
                .astype(str)
                .str.strip()
                .isin(allowed)
            ]

        self.proceed_callback(filtered_df, self.mapping, self.df)
        self.close()
