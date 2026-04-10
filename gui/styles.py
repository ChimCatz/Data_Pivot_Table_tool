WINDOW_STYLE = """
QWidget {
    background-color: #F7FAFC;
    color: #243447;
    font-size: 10pt;
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
            background-color: #D8EAF7;
            border: 1px solid #B8D7EC;
            color: #1E4F77;
        }
        QPushButton:hover {
            background-color: #CBE3F4;
        }
    """,
    "success": """
        QPushButton {
            background-color: #DDF3EA;
            border: 1px solid #B9E0CF;
            color: #21674E;
        }
        QPushButton:hover {
            background-color: #D2ECDD;
        }
    """,
    "warning": """
        QPushButton {
            background-color: #F7EFD6;
            border: 1px solid #EADBAA;
            color: #78611B;
        }
        QPushButton:hover {
            background-color: #F2E7C4;
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
}


def button_style(kind):
    return BUTTON_STYLES[kind]
