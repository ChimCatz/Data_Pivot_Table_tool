from datetime import datetime

import pandas as pd
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QInputDialog,
    QMessageBox
)

from engine.adjuster import scale_summary
from engine.aggregator import build_summary
from engine.session_manager import (
    save_session,
    load_session,
    list_sessions,
    session_exists,
    normalize_session_name
)
from gui.session_manager_window import SessionManagerWindow
from gui.styles import WINDOW_STYLE, button_style


class PreviewDashboard(QWidget):

    def __init__(self, df, mapping, source_df=None):
        super().__init__()

        self.df = df.copy()
        self.source_df = source_df.copy() if source_df is not None else df.copy()
        self.mapping = mapping
        self.adjusted_total = None

        self.setWindowTitle("Analytics Report")
        self.resize(1200, 650)
        self.setStyleSheet(WINDOW_STYLE)

        main_layout = QVBoxLayout()

        self.total_label = QLabel("")
        self.total_label.setStyleSheet(
            "font-size:14pt; font-weight:bold;"
        )
        main_layout.addWidget(self.total_label)

        btn_row = QHBoxLayout()

        self.manage_btn = QPushButton("Manage Sessions")
        self.manage_btn.setStyleSheet(button_style("primary"))
        self.manage_btn.clicked.connect(self.open_session_manager)

        self.save_btn = QPushButton("Save Session")
        self.save_btn.setStyleSheet(button_style("success"))
        self.save_btn.clicked.connect(self.save_current_session)

        self.load_btn = QPushButton("Load Session")
        self.load_btn.setStyleSheet(button_style("accent"))
        self.load_btn.clicked.connect(self.load_existing_session)

        self.adjust_btn = QPushButton("Adjust Totals")
        self.adjust_btn.setStyleSheet(button_style("warning"))
        self.adjust_btn.clicked.connect(self.adjust_totals)

        self.export_csv_btn = QPushButton("Export CSV")
        self.export_csv_btn.setStyleSheet(button_style("primary"))
        self.export_csv_btn.clicked.connect(self.export_csv)

        btn_row.addWidget(self.manage_btn)
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.load_btn)
        btn_row.addStretch()
        btn_row.addWidget(self.adjust_btn)
        btn_row.addWidget(self.export_csv_btn)

        main_layout.addLayout(btn_row)

        self.report_layout = QHBoxLayout()
        main_layout.addLayout(self.report_layout)

        self.setLayout(main_layout)

        self.build_dashboard()

    def build_dashboard(self):

        while self.report_layout.count():
            child = self.report_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        summary = build_summary(self.df, self.mapping)

        any_field = next(iter(summary))
        original_total = summary[any_field]["total"]

        display_total = (
            self.adjusted_total
            if self.adjusted_total
            else original_total
        )

        self.total_label.setText(
            f"Total Records: {display_total}"
        )

        colors = {
            "Country": "#7FB3D5",
            "Industry": "#73C6B6",
            "Job Level": "#F0C674"
        }

        for field, data in summary.items():

            table_df = data["table"]

            if self.adjusted_total:
                table_df = scale_summary(
                    table_df,
                    self.adjusted_total
                )

            table_df = table_df.reset_index(drop=True)
            table_df.insert(0, "No", table_df.index + 1)

            container = QWidget()
            container.setStyleSheet(
                "background-color:#FFFFFF; border:1px solid #D8E2EC; border-radius:10px;"
            )
            container_layout = QVBoxLayout()

            title = QLabel(field)
            title.setStyleSheet(
                "font-size:12pt; font-weight:bold; padding:4px;"
            )
            container_layout.addWidget(title)

            table = QTableWidget()
            table.setRowCount(table_df.shape[0])
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(
                ["No", field, "Count"]
            )

            color = colors.get(field, "#A9CCE3")

            table.setStyleSheet(f"""
                QHeaderView::section {{
                    background-color: {color};
                    color: #1F2D3D;
                    font-weight: bold;
                    padding: 4px;
                    font-size: 9pt;
                    border: none;
                }}
                QTableWidget {{
                    font-size: 8.5pt;
                    gridline-color: #E5ECF3;
                    background-color: #FFFFFF;
                    border: none;
                }}
            """)

            table.verticalHeader().setDefaultSectionSize(20)
            table.horizontalHeader().setStretchLastSection(True)

            for row in range(table_df.shape[0]):
                for col in range(3):
                    table.setItem(
                        row,
                        col,
                        QTableWidgetItem(
                            str(table_df.iat[row, col])
                        )
                    )

            table.resizeColumnsToContents()

            container_layout.addWidget(table)
            container.setLayout(container_layout)

            self.report_layout.addWidget(container)

    def adjust_totals(self):

        summary = build_summary(self.df, self.mapping)
        minimum_total = max(
            len(data["table"])
            for data in summary.values()
        )

        new_total, ok = QInputDialog.getInt(
            self,
            "Adjust Total",
            f"Enter new total (minimum {minimum_total}):",
            value=self.adjusted_total
            if self.adjusted_total
            else len(self.df),
            minValue=minimum_total
        )

        if ok:
            self.adjusted_total = new_total
            self.build_dashboard()

    def export_csv(self):

        default_name = datetime.now().strftime(
            "DataReportCount_%m%d%Y_%H%M.csv"
        )

        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            default_name,
            "CSV Files (*.csv)"
        )

        if not file:
            return

        summary = build_summary(self.df, self.mapping)

        tables = []
        max_len = 0

        for field, data in summary.items():

            df_field = data["table"]

            if self.adjusted_total:
                df_field = scale_summary(
                    df_field,
                    self.adjusted_total
                )

            df_field = df_field.reset_index(drop=True)

            max_len = max(max_len, len(df_field))

            tables.append((field, df_field))

        combined = pd.DataFrame()
        totals = {}

        for field, df_field in tables:

            df_field = df_field.reindex(range(max_len))

            combined[field] = df_field.iloc[:, 0]
            combined[f"{field} Count"] = df_field.iloc[:, 1]

            totals[field] = "TOTAL"
            totals[f"{field} Count"] = df_field.iloc[:, 1].sum()

        combined = pd.concat(
            [combined, pd.DataFrame([totals])],
            ignore_index=True
        )

        combined.to_csv(file, index=False)

    def save_current_session(self):

        name, ok = QInputDialog.getText(
            self,
            "Save Session",
            "Enter session name:"
        )

        session_name = normalize_session_name(name)

        if not ok or not session_name:
            return

        filters = {}

        for field in self.mapping:
            filters[field] = (
                self.df[self.mapping[field]]
                .dropna()
                .astype(str)
                .str.strip()
                .unique()
                .tolist()
            )

        data = {
            "mapping": self.mapping,
            "adjusted_total": self.adjusted_total,
            "filters": filters
        }

        if session_exists(session_name):
            confirm = QMessageBox.question(
                self,
                "Overwrite Session",
                f"Session '{session_name}' already exists. Overwrite it?"
            )
            if confirm != QMessageBox.Yes:
                return

        saved_name = save_session(session_name, data)
        QMessageBox.information(
            self,
            "Session Saved",
            f"Session '{saved_name}' was saved successfully."
        )

    def load_existing_session(self):

        sessions = list_sessions()

        if not sessions:
            QMessageBox.information(
                self,
                "No Sessions",
                "There are no saved sessions yet."
            )
            return

        name, ok = QInputDialog.getItem(
            self,
            "Load Session",
            "Choose:",
            sessions,
            0,
            False
        )

        if not ok:
            return

        data = load_session(name)

        self.adjusted_total = data.get("adjusted_total")

        df = self.source_df.copy()

        for field, values in data.get("filters", {}).items():

            col = data.get("mapping", {}).get(field, self.mapping.get(field))

            if not col or col not in df.columns:
                continue

            df = df[
                df[col]
                .astype(str)
                .str.strip()
                .isin(values)
            ]

        self.df = df
        self.build_dashboard()

    def open_session_manager(self):

        self.manager = SessionManagerWindow()
        self.manager.show()
