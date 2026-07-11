# -*- coding: utf-8 -*-
"""Main application window: sidebar + top bar + stacked pages."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QStackedWidget,
    QMessageBox, QApplication,
)

from core.translations import lang
from core.styles import build_stylesheet
from widgets.sidebar import Sidebar
from pages.dashboard_page import DashboardPage
from pages.books_page import BooksPage
from pages.members_page import MembersPage
from pages.borrow_page import BorrowPage
from pages.reports_page import ReportsPage
from pages.settings_page import SettingsPage

NAV_TITLES = {
    "dashboard": "nav_dashboard",
    "books": "nav_books",
    "members": "nav_members",
    "borrow": "nav_borrow",
    "reports": "nav_reports",
    "settings": "nav_settings",
}


class MainWindow(QMainWindow):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.theme = self.db.get_setting("theme", "light")
        self.library_name = self.db.get_setting("library_name", "LibraSys")
        self.current_key = "dashboard"
        self.logout_flag = False

        self.setWindowTitle(lang.tr("app_title"))
        self.resize(1280, 800)
        self.setMinimumSize(1040, 640)

        central = QWidget()
        central.setObjectName("CentralHost")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(library_name=self.library_name)
        self.sidebar.navigate.connect(self.navigate)
        self.sidebar.logout_requested.connect(self.request_logout)
        root.addWidget(self.sidebar)

        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(0)

        self.topbar = self._build_topbar()
        right_col.addWidget(self.topbar)

        self.stack = QStackedWidget()
        right_col.addWidget(self.stack, 1)

        right_host = QWidget()
        right_host.setLayout(right_col)
        root.addWidget(right_host, 1)

        # ---- Build pages ----
        self.dashboard_page = DashboardPage(self.db, theme=self.theme)
        self.books_page = BooksPage(self.db)
        self.members_page = MembersPage(self.db)
        self.borrow_page = BorrowPage(self.db)
        self.reports_page = ReportsPage(self.db)
        self.settings_page = SettingsPage(self.db, self.user, theme=self.theme)
        self.settings_page.theme_changed.connect(self.apply_theme)
        self.settings_page.library_name_changed.connect(self._on_library_name_changed)

        for key, page in [
            ("dashboard", self.dashboard_page), ("books", self.books_page),
            ("members", self.members_page), ("borrow", self.borrow_page),
            ("reports", self.reports_page), ("settings", self.settings_page),
        ]:
            self.stack.addWidget(page)
        self._page_map = {
            "dashboard": self.dashboard_page, "books": self.books_page,
            "members": self.members_page, "borrow": self.borrow_page,
            "reports": self.reports_page, "settings": self.settings_page,
        }

        self.statusBar().showMessage(f"{lang.tr('logged_in_as')}: {self.user['full_name'] or self.user['username']}")

        self.apply_theme(self.theme, persist=False)
        self.navigate("dashboard")

        lang.language_changed.connect(self.retranslate_ui)

    # ------------------------------------------------------------------
    def _build_topbar(self):
        bar = QWidget()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(64)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(24, 0, 24, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        self.page_title_label = QLabel()
        self.page_title_label.setObjectName("PageTitle")
        title_col.addWidget(self.page_title_label)
        layout.addLayout(title_col)
        layout.addStretch()

        self.lang_toggle_btn = QPushButton("EN / \u0639\u0631")
        self.lang_toggle_btn.setObjectName("IconButton")
        self.lang_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.lang_toggle_btn.clicked.connect(lambda: lang.toggle())
        layout.addWidget(self.lang_toggle_btn)

        self.theme_toggle_btn = QPushButton()
        self.theme_toggle_btn.setObjectName("IconButton")
        self.theme_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        layout.addWidget(self.theme_toggle_btn)

        self.user_label = QLabel(f"\U0001F464  {self.user['full_name'] or self.user['username']}")
        self.user_label.setStyleSheet("font-size: 12.5px; font-weight: 600; margin-left: 10px;")
        layout.addWidget(self.user_label)

        return bar

    # ------------------------------------------------------------------
    def navigate(self, key):
        self.current_key = key
        page = self._page_map.get(key)
        if page:
            self.stack.setCurrentWidget(page)
            if hasattr(page, "refresh"):
                page.refresh()
        self.sidebar.set_active(key)
        self.page_title_label.setText(lang.tr(NAV_TITLES.get(key, "")))

    def _toggle_theme(self):
        new_theme = "dark" if self.theme == "light" else "light"
        self.apply_theme(new_theme)
        # keep the settings page radio buttons in sync
        if new_theme == "dark":
            self.settings_page.radio_dark.setChecked(True)
        else:
            self.settings_page.radio_light.setChecked(True)

    def apply_theme(self, theme, persist=True):
        self.theme = theme
        QApplication.instance().setStyleSheet(build_stylesheet(theme))
        self.dashboard_page.set_theme(theme)
        self.theme_toggle_btn.setText("\u2600" if theme == "dark" else "\U0001F319")
        if persist:
            self.db.set_setting("theme", theme)

    def _on_library_name_changed(self, name):
        self.library_name = name
        self.sidebar.set_library_name(name)

    def request_logout(self):
        reply = QMessageBox.question(
            self, lang.tr("nav_logout"), lang.tr("logout_confirm"), QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.logout_flag = True
            QApplication.instance().quit()

    def retranslate_ui(self):
        self.setWindowTitle(lang.tr("app_title"))
        self.page_title_label.setText(lang.tr(NAV_TITLES.get(self.current_key, "")))
        self.statusBar().showMessage(f"{lang.tr('logged_in_as')}: {self.user['full_name'] or self.user['username']}")
        QApplication.instance().setLayoutDirection(Qt.RightToLeft if lang.is_rtl else Qt.LeftToRight)
