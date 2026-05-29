import os

from PySide6.QtGui import QIcon
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
from gui.styles import WINDOW_STYLE, button_style
from config import APP_NAME, BUILD_VERSION, BUILD_DATE, CREATOR, APP_ICON_PATH


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.current_df = None
        self.active_window = None

        self.setWindowTitle(APP_NAME)
        self.setFixedSize(520, 220)
        self.setStyleSheet(WINDOW_STYLE)
        if APP_ICON_PATH.exists():
            self.setWindowIcon(QIcon(str(APP_ICON_PATH)))

        title = QLabel(APP_NAME)
        title.setStyleSheet("font-size:14pt; font-weight:bold;")

        version = QLabel(f"{BUILD_VERSION} | Build Date: {BUILD_DATE}")
        creator = QLabel(CREATOR)

        self.label = QLabel("No file loaded")
        self.file_name_label = QLabel("File Name: -")
        self.file_location_label = QLabel("File Location: -")
        self.file_location_label.setWordWrap(True)

        self.import_btn = QPushButton("Import CSV")
        self.import_btn.setStyleSheet(button_style("primary"))
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
                self.current_df = df

                self.label.setText(f"Loaded rows: {len(df)}")
                self.open_mapping(df)

            except Exception as e:
                self.current_df = None
                self.label.setText(str(e))
                self.file_name_label.setText("File Name: -")
                self.file_location_label.setText("File Location: -")

    def show_import_window(self):

        if self.active_window:
            if hasattr(self.active_window, "on_close_callback"):
                self.active_window.on_close_callback = None
            self.active_window.close()
            self.active_window = None

        self.show()
        self.raise_()
        self.activateWindow()

    def show_child_window(self, window):

        if self.active_window and self.active_window is not window:
            if hasattr(self.active_window, "on_close_callback"):
                self.active_window.on_close_callback = None
            self.active_window.close()

        self.active_window = window
        if hasattr(window, "on_close_callback"):
            window.on_close_callback = self.show_import_window
        self.hide()
        window.show()
        window.raise_()
        window.activateWindow()

    def open_mapping(self, df=None, initial_mapping=None):

        df = df if df is not None else self.current_df

        if df is None:
            self.show_import_window()
            return

        self.mapper_window = ColumnMapper(
            df,
            self.open_filter,
            self.show_import_window,
            initial_mapping=initial_mapping
        )
        self.show_child_window(self.mapper_window)

    def open_filter(self, df, mapping, initial_filters=None):

        self.filter_window = DataFilterWindow(
            df,
            mapping,
            self.open_dashboard,
            self.show_import_window,
            lambda: self.open_mapping(df, initial_mapping=mapping),
            initial_filters=initial_filters
        )
        self.show_child_window(self.filter_window)

    def open_dashboard(
        self,
        df,
        mapping,
        source_df=None,
        selected_filters=None
    ):
        base_df = source_df if source_df is not None else df

        self.preview_window = PreviewDashboard(
            df,
            mapping,
            source_df=base_df,
            selected_filters=selected_filters,
            back_to_import_callback=self.show_import_window,
            back_to_mapping_callback=lambda: self.open_mapping(
                base_df,
                initial_mapping=mapping
            )
        )
        self.preview_window.back_to_filter_callback = lambda: self.open_filter(
            base_df,
            mapping,
            initial_filters=self.preview_window.selected_filters
        )
        self.show_child_window(self.preview_window)
