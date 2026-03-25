from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QInputDialog,
    QMessageBox
)

from engine.session_manager import (
    list_sessions,
    delete_session,
    rename_session
)


class SessionManagerWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manage Sessions")
        self.setFixedSize(350, 400)

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.rename_btn = QPushButton("Rename")
        self.delete_btn = QPushButton("Delete")

        layout.addWidget(self.rename_btn)
        layout.addWidget(self.delete_btn)

        self.setLayout(layout)

        self.load_sessions()

        self.rename_btn.clicked.connect(self.rename)
        self.delete_btn.clicked.connect(self.delete)

    def load_sessions(self):

        self.list_widget.clear()

        for s in list_sessions():
            self.list_widget.addItem(s)

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

        if ok and new:
            rename_session(old, new)
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