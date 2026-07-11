# -*- coding: utf-8 -*-
"""
LibraSys \u2013 Bilingual Library Management System
Entry point: boots the Qt application, shows the login dialog, then the
main window on successful authentication.
"""

import os
import sys

# Qt 6 and newer PyQt5 builds may not ship a bundled font directory.
# Point Qt to the system fonts directory before importing any Qt modules.
if "QT_QPA_FONTDIR" not in os.environ:
    win_fonts = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")
    if os.path.isdir(win_fonts):
        os.environ["QT_QPA_FONTDIR"] = win_fonts

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

# Make sure local package imports (core, widgets, dialogs, pages) resolve
# regardless of the working directory the app is launched from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.database import Database
from core.translations import lang
from core.styles import build_stylesheet
from dialogs.login_dialog import LoginDialog
from main_window import MainWindow

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "librasys.db")


def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("LibraSys")

    base_font = QFont("Segoe UI", 10)
    app.setFont(base_font)

    db = Database(DB_PATH)

    # Restore saved language & theme preferences
    saved_lang = db.get_setting("language", "en")
    lang.set_language(saved_lang)
    theme = db.get_setting("theme", "light")

    app.setLayoutDirection(Qt.RightToLeft if lang.is_rtl else Qt.LeftToRight)
    app.setStyleSheet(build_stylesheet(theme))

    # Persist language choice whenever it changes
    lang.language_changed.connect(lambda code: db.set_setting("language", code))

    # Loop so that "Logout" returns to the sign-in screen instead of
    # closing the whole application.
    while True:
        current_theme = db.get_setting("theme", "light")
        login = LoginDialog(db, theme=current_theme)
        if login.exec_() != LoginDialog.Accepted or not login.user:
            break

        window = MainWindow(db, login.user)
        window.show()
        app.exec_()

        if not window.logout_flag:
            break

    db.close()
    sys.exit(0)


if __name__ == "__main__":
    main()
