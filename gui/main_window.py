import os

from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QLabel,
)

from engine.data_loader import load_csv
from gui.preview_dashboard import PreviewDashboard
from gui.column_mapper import ColumnMapper
from gui.data_filter import DataFilterWindow
from config import APP_NAME, BUILD_VERSION, CREATOR


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.setFixedSize(520, 220)

        title = QLabel(APP_NAME)
        title.setStyleSheet("font-size:14pt; font-weight:bold;")

        version = QLabel(f"Build Version {BUILD_VERSION}")
        creator = QLabel(CREATOR)

        self.label = QLabel("No file loaded")
        self.file_name_label = QLabel("File Name: -")
        self.file_location_label = QLabel("File Location: -")
        self.file_location_label.setWordWrap(True)

        self.import_btn = QPushButton("Import CSV")
        self.import_btn.clicked.connect(self.import_csv)

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(creator)
        layout.addSpacing(5)
        layout.addWidget(self.label)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.file_location_label)
        layout.addWidget(self.import_btn)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def import_csv(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file:
            self.label.setText("Loading CSV...")
            self.file_name_label.setText(
                f"File Name: {os.path.basename(file)}"
            )
            self.file_location_label.setText(
                f"File Location: {file}"
            )

            try:
                df = load_csv(file)

                self.label.setText(f"Loaded rows: {len(df)}")

                self.mapper_window = ColumnMapper(
                    df,
                    self.open_preview
                )
                self.mapper_window.show()

            except Exception as e:
                self.label.setText(str(e))
                self.file_name_label.setText("File Name: -")
                self.file_location_label.setText("File Location: -")

    def open_preview(self, df, mapping):

        self.filter_window = DataFilterWindow(
            df,
            mapping,
            self.open_dashboard
        )
        self.filter_window.show()

    def open_dashboard(self, df, mapping):

        self.preview_window = PreviewDashboard(df, mapping)
        self.preview_window.show()
