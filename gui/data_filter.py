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


class DataFilterWindow(QWidget):

    def __init__(self, df, mapping, proceed_callback):
        super().__init__()

        self.df = df
        self.mapping = mapping
        self.proceed_callback = proceed_callback

        self.setWindowTitle("Filter Data")
        self.setFixedSize(420, 420)

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

            label = QLabel(field)
            label.setStyleSheet("font-weight:bold;")
            tab_layout.addWidget(label)

            list_widget = QListWidget()

            values = (
                df[col]
                .fillna("Unknown")
                .astype(str)
                .str.strip()
                .unique()
            )

            values = sorted(values)

            for val in values:
                item = QListWidgetItem(val)
                item.setCheckState(Qt.Checked)
                list_widget.addItem(item)

            tab_layout.addWidget(list_widget)

            # Buttons row
            btn_layout = QHBoxLayout()

            select_all = QPushButton("Select All")
            unselect_all = QPushButton("Unselect All")

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
        self.apply_btn.setStyleSheet("font-weight:bold; padding:6px;")
        self.apply_btn.clicked.connect(self.apply_filter)

        main_layout.addWidget(self.apply_btn)

        self.setLayout(main_layout)

    def set_all(self, list_widget, state):

        for i in range(list_widget.count()):
            item = list_widget.item(i)
            item.setCheckState(
                Qt.Checked if state else Qt.Unchecked
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

        self.proceed_callback(filtered_df, self.mapping)
        self.close()