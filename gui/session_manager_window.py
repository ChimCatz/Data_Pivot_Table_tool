from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QInputDialog,
    QMessageBox,
    QLabel
)

from engine.session_manager import (
    list_sessions,
    delete_session,
    rename_session,
    session_exists,
    normalize_session_name
)
from gui.styles import WINDOW_STYLE, button_style


class SessionManagerWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manage Sessions")
        self.setFixedSize(350, 400)
        self.setStyleSheet(WINDOW_STYLE)

        layout = QVBoxLayout()

        title = QLabel("Saved Sessions")
        title.setStyleSheet("font-size:12pt; font-weight:bold;")
        layout.addWidget(title)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.rename_btn = QPushButton("Rename")
        self.delete_btn = QPushButton("Delete")
        self.rename_btn.setStyleSheet(button_style("warning"))
        self.delete_btn.setStyleSheet(button_style("danger"))

        layout.addWidget(self.rename_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        self.load_sessions()

        self.rename_btn.clicked.connect(self.rename)
        self.delete_btn.clicked.connect(self.delete)

    def load_sessions(self):

        self.list_widget.clear()
        sessions = list_sessions()

        for session_name in sessions:
            self.list_widget.addItem(session_name)

        has_sessions = bool(sessions)
        self.rename_btn.setEnabled(has_sessions)
        self.delete_btn.setEnabled(has_sessions)

    def rename(self):

        item = self.list_widget.currentItem()

        if not item:
            return

        old = item.text()

        new, ok = QInputDialog.getText(
            self,
            "Rename Session",
            "New Name:"
        )

        new_name = normalize_session_name(new)

        if ok and new_name:
            if new_name != old and session_exists(new_name):
                QMessageBox.warning(
                    self,
                    "Session Exists",
                    f"Session '{new_name}' already exists."
                )
                return

            rename_session(old, new_name)
            self.load_sessions()

    def delete(self):

        item = self.list_widget.currentItem()

        if not item:
            return

        name = item.text()

        confirm = QMessageBox.question(
            self,
            "Delete",
            f"Delete session '{name}'?"
        )

        if confirm == QMessageBox.Yes:
            delete_session(name)
            self.load_sessions()
