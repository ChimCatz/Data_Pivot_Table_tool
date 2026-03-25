from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QFileDialog,
    QInputDialog
)
from engine.session_manager import (
    save_session,
    load_session,
    list_sessions
)
from datetime import datetime
import pandas as pd
from gui.session_manager_window import SessionManagerWindow
from engine.aggregator import build_summary
from engine.adjuster import scale_summary


class PreviewDashboard(QWidget):

    def __init__(self, df, mapping):
        super().__init__()

        self.df = df
        self.mapping = mapping
        self.adjusted_total = None

        self.setWindowTitle("Analytics Report")
        self.resize(1200, 650)

        main_layout = QVBoxLayout()

        self.total_label = QLabel("")
        self.total_label.setStyleSheet(
            "font-size:14pt; font-weight:bold;"
        )
        main_layout.addWidget(self.total_label)

        btn_row = QHBoxLayout()

        self.adjust_btn = QPushButton("Adjust Totals")
        self.adjust_btn.clicked.connect(self.adjust_totals)

        self.export_csv_btn = QPushButton("Export CSV")
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.save_btn = QPushButton("Save Session")
        self.save_btn.clicked.connect(self.save_current_session)

        self.load_btn = QPushButton("Load Session")
        self.load_btn.clicked.connect(self.load_existing_session)
        self.manage_btn = QPushButton("Manage Sessions")
        self.manage_btn.clicked.connect(self.open_session_manager)

        btn_row.addWidget(self.manage_btn)  
        btn_row.addWidget(self.save_btn)
        btn_row.addWidget(self.load_btn)

        btn_row.addWidget(self.adjust_btn)
        btn_row.addWidget(self.export_csv_btn)

        main_layout.addLayout(btn_row)

        self.report_layout = QHBoxLayout()
        main_layout.addLayout(self.report_layout)

        self.setLayout(main_layout)

        self.build_dashboard()

    def build_dashboard(self):

        # clear old widgets
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
            "Country": "#1F618D",
            "Industry": "#117A65",
            "Job Level": "#7D6608"
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

            container_layout = QVBoxLayout()

            title = QLabel(f"{field}")
            title.setStyleSheet(
                "font-size:12pt; font-weight:bold;"
            )
            container_layout.addWidget(title)

            table = QTableWidget()
            table.setRowCount(table_df.shape[0])
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels(
                ["No", field, "Count"]
            )

            color = colors.get(field, "#1F618D")

            table.setStyleSheet(f"""
                QHeaderView::section {{
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                    padding: 3px;
                    font-size:9pt;
                }}
                QTableWidget {{
                    font-size:8pt;
                    gridline-color:#D0D3D4;
                }}
            """)

            table.verticalHeader().setDefaultSectionSize(18)
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

            container = QWidget()
            container.setLayout(container_layout)
            container_layout.addWidget(table)

            self.report_layout.addWidget(container)

    def adjust_totals(self):

        new_total, ok = QInputDialog.getInt(
            self,
            "Adjust Total",
            "Enter new total:",
            value=self.adjusted_total
            if self.adjusted_total
            else len(self.df),
            minValue=1
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

        if not ok or not name:
            return

        filters = {}

        summary = build_summary(self.df, self.mapping)

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

        save_session(name, data)

    def load_existing_session(self):

        sessions = list_sessions()

        if not sessions:
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

        # apply filters
        df = self.df

        for field, values in data["filters"].items():

            col = self.mapping[field]

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