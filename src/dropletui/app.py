"""Application setup helpers."""

from __future__ import annotations

import sys

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from dropletui.theme import Theme, stylesheet


UI_FONT_CANDIDATES = (
    "Helvetica Neue",
    "Segoe UI",
    "Noto Sans",
    "DejaVu Sans",
    "Liberation Sans",
    "Ubuntu",
    ".AppleSystemUIFont",
)


def resolved_ui_font(point_size: int = Theme.FONT_SIZE_BODY) -> QFont:
    families = set(QFontDatabase.families())
    for family in UI_FONT_CANDIDATES:
        if family in families:
            font = QFont(family)
            font.setPointSize(point_size)
            return font

    font = QFontDatabase.systemFont(QFontDatabase.SystemFont.TitleFont)
    font.setPointSize(point_size)
    return font


def apply_app_theme(app: QApplication) -> None:
    app.setStyle("Fusion")
    app.setFont(resolved_ui_font())
    app.setStyleSheet(stylesheet())


def create_app(name: str, argv: list[str] | None = None) -> QApplication:
    app = QApplication(argv if argv is not None else sys.argv)
    app.setApplicationName(name)
    app.setApplicationDisplayName(name)
    apply_app_theme(app)
    return app
