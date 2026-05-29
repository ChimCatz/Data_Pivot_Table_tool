WINDOW_STYLE = """
QWidget {
    background-color: #F7FAFC;
    color: #243447;
    font-size: 10pt;
    font-family: "Inter", "Proxima Nova", "Segoe UI", sans-serif;
}
QLabel {
    color: #243447;
}
QListWidget, QTabWidget::pane, QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #D8E2EC;
    border-radius: 8px;
}
QTabBar::tab {
    background-color: #EAF1F7;
    border: 1px solid #D8E2EC;
    padding: 6px 12px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    background-color: #FFFFFF;
    font-weight: bold;
}
QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #C9D5E2;
    border-radius: 6px;
    padding: 5px 8px;
}
QPushButton {
    background-color: #E3EDF7;
    border: 1px solid #C8D8E8;
    border-radius: 8px;
    padding: 6px 12px;
    color: #20415F;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #D7E7F4;
}
QPushButton:pressed {
    background-color: #C9DDEE;
}
"""


BUTTON_STYLES = {
    "primary": """
        QPushButton {
            background-color: #E6EAF8;
            border: 1px solid #C6D0EE;
            color: #465A92;
        }
        QPushButton:hover {
            background-color: #D9E0F5;
        }
    """,
    "success": """
        QPushButton {
            background-color: #D9F1E4;
            border: 1px solid #B5DEC9;
            color: #1F6A4A;
        }
        QPushButton:hover {
            background-color: #CCE9D8;
        }
    """,
    "info": """
        QPushButton {
            background-color: #DCEFFD;
            border: 1px solid #B6D8F4;
            color: #245E8A;
        }
        QPushButton:hover {
            background-color: #CDE5FA;
        }
    """,
    "warning": """
        QPushButton {
            background-color: #F8E5CC;
            border: 1px solid #EDCFA0;
            color: #8A5A1F;
        }
        QPushButton:hover {
            background-color: #F4DABD;
        }
    """,
    "accent": """
        QPushButton {
            background-color: #F9E0D9;
            border: 1px solid #EDC1B4;
            color: #8A4A36;
        }
        QPushButton:hover {
            background-color: #F5D2C8;
        }
    """,
    "neutral": """
        QPushButton {
            background-color: #E7EBF2;
            border: 1px solid #CAD3E1;
            color: #44546A;
        }
        QPushButton:hover {
            background-color: #DDE4EE;
        }
    """,
    "danger": """
        QPushButton {
            background-color: #F8DDDF;
            border: 1px solid #EDBEC2;
            color: #8A3C44;
        }
        QPushButton:hover {
            background-color: #F3D0D4;
        }
    """,
    "nav_import": """
        QPushButton {
            background-color: #F9E0D9;
            border: 1px solid #EDC1B4;
            color: #8A4A36;
        }
        QPushButton:hover {
            background-color: #F5D2C8;
        }
    """,
    "nav_mapping": """
        QPushButton {
            background-color: #F6E7D1;
            border: 1px solid #E8C9A4;
            color: #7F5A24;
        }
        QPushButton:hover {
            background-color: #F1DDBF;
        }
    """,
    "nav_filter": """
        QPushButton {
            background-color: #D7F1EF;
            border: 1px solid #B0DDD8;
            color: #256B68;
        }
        QPushButton:hover {
            background-color: #C9E9E6;
        }
    """,
    "export": """
        QPushButton {
            background-color: #E3E6F4;
            border: 1px solid #C3CAE5;
            color: #3F4E87;
        }
        QPushButton:hover {
            background-color: #D7DDEF;
        }
    """,
}


def button_style(kind):
    return BUTTON_STYLES[kind]
