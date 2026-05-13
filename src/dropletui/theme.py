"""Design tokens and Qt stylesheet for droplet apps."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class _ControlSize:
    min_height: int
    padding: str
    font_size: int


class Theme:
    """Canonical dark desktop palette and sizing tokens."""

    BG_BLACK = "#000000"
    BG_DARK = "#1a1a1a"
    BG_DARKER = "#141414"
    BG_MEDIUM = "#222222"
    BG_RAISED = "#242424"
    BG_CONTROL = "#2b2b2b"
    BG_CONTROL_HOVER = "#353535"
    BG_CONTROL_PRESSED = "#404040"

    TEXT_WHITE = "#d4d4d4"
    TEXT_MUTED = "#888888"
    TEXT_SUBTLE = "#666666"
    TEXT_DISABLED = "#555555"

    BORDER_COOL = "#333333"
    BORDER_HOVER = "#444444"
    BORDER_DISABLED = "#2a2a2a"

    ACCENT = "#3498db"
    ACCENT_HOVER = "#2980b9"
    SUCCESS = "#27ae60"
    SUCCESS_HOVER = "#2ecc71"
    DANGER = "#c0392b"
    DANGER_HOVER = "#e74c3c"
    WARNING = "#f39c12"
    WARNING_DARK = "#e67e22"
    INFO = "#2980b9"

    INPUT_BG = BG_CONTROL
    INPUT_BORDER = BORDER_COOL
    INPUT_BORDER_HOVER = BORDER_HOVER
    INPUT_BORDER_FOCUS = ACCENT

    DISABLED_BG = BG_MEDIUM
    DISABLED_TEXT = TEXT_DISABLED
    DISABLED_BORDER = BORDER_DISABLED

    FONT_SIZE_SMALL = 11
    FONT_SIZE_BODY = 13
    FONT_SIZE_TITLE = 16

    SPACE_1 = 4
    SPACE_2 = 6
    SPACE_3 = 8
    SPACE_4 = 12
    WINDOW_PADDING = SPACE_4
    PANEL_PADDING = 10
    SPLITTER_PADDING = SPACE_2
    RADIUS = 4
    SPLITTER_HANDLE_WIDTH = 12
    SPLITTER_MARK_THICKNESS = 5
    SPLITTER_MARK_LENGTH_RATIO = 0.5
    SEPARATOR_THICKNESS = SPLITTER_MARK_THICKNESS
    CONTROL_INLINE = _ControlSize(min_height=24, padding="2px 8px", font_size=FONT_SIZE_BODY)
    CONTROL_DEFAULT = _ControlSize(min_height=26, padding="3px 10px", font_size=FONT_SIZE_BODY)
    CONTROL_LARGE = _ControlSize(min_height=36, padding="8px 14px", font_size=FONT_SIZE_BODY)
    CONTROL_STAGE = _ControlSize(min_height=56, padding="10px 16px", font_size=FONT_SIZE_BODY)


STATUS_COLORS = {
    "default": Theme.TEXT_WHITE,
    "muted": Theme.TEXT_MUTED,
    "subtle": Theme.TEXT_SUBTLE,
    "primary": Theme.ACCENT,
    "info": Theme.INFO,
    "success": Theme.SUCCESS,
    "danger": Theme.DANGER_HOVER,
    "warning": Theme.WARNING,
}

BUTTON_COLORS = {
    "neutral": (Theme.BG_CONTROL, Theme.BG_CONTROL_HOVER),
    "primary": (Theme.ACCENT, Theme.ACCENT_HOVER),
    "success": (Theme.SUCCESS, Theme.SUCCESS_HOVER),
    "danger": (Theme.DANGER, Theme.DANGER_HOVER),
    "warning": (Theme.WARNING_DARK, Theme.WARNING),
}

PLOT_COLORS = [Theme.ACCENT, Theme.DANGER_HOVER, Theme.SUCCESS_HOVER]


def control_size(size: str = "default") -> _ControlSize:
    return {
        "inline": Theme.CONTROL_INLINE,
        "default": Theme.CONTROL_DEFAULT,
        "large": Theme.CONTROL_LARGE,
        "stage": Theme.CONTROL_STAGE,
    }.get(size, Theme.CONTROL_DEFAULT)


def text_qss(
    kind: str = "default",
    *,
    font_size: int | None = None,
    bold: bool = False,
    padding: str | None = None,
) -> str:
    parts = [f"color: {STATUS_COLORS.get(kind, kind)};"]
    if font_size is not None:
        parts.append(f"font-size: {font_size}px;")
    if bold:
        parts.append("font-weight: 600;")
    if padding is not None:
        parts.append(f"padding: {padding};")
    return " ".join(parts)


def button_qss(kind: str = "neutral", *, size: str = "default", flat: bool = False) -> str:
    bg, hover = BUTTON_COLORS.get(kind, BUTTON_COLORS["neutral"])
    token = control_size(size)
    radius = "0" if flat else f"{Theme.RADIUS}px"
    padding = "0" if flat else token.padding
    height = "" if flat else f"min-height: {token.min_height}px; max-height: {token.min_height}px;"
    return (
        f"QPushButton {{ background-color: {bg}; border: none; color: {Theme.TEXT_WHITE}; "
        f"border-radius: {radius}; padding: {padding}; font-size: {token.font_size}px; "
        f"font-weight: 600; {height} }}"
        f"QPushButton:hover {{ background-color: {hover}; }}"
        f"QPushButton:pressed {{ background-color: {Theme.BG_CONTROL_PRESSED}; }}"
        f"QPushButton:disabled {{ background-color: {Theme.DISABLED_BG}; "
        f"color: {Theme.DISABLED_TEXT}; border: none; }}"
    )


def value_label_qss(kind: str = "success", *, padding: str = "8px 10px") -> str:
    return f"background: {Theme.BG_DARKER}; {text_qss(kind, padding=padding)}"


def configure_pyqtgraph(pg_module) -> None:
    pg_module.setConfigOptions(
        antialias=True,
        background=Theme.BG_DARK,
        foreground=Theme.TEXT_WHITE,
    )


def configure_monospace_font(font, point_size: int | None = None) -> None:
    """Use Qt's resolved monospace font instead of naming a platform-specific family."""
    style_hint = getattr(getattr(font, "StyleHint", None), "Monospace", None)
    if style_hint is None:
        style_hint = getattr(font, "Monospace")
    font.setStyleHint(style_hint)
    if point_size is not None:
        font.setPointSize(point_size)


def stylesheet() -> str:
    default = Theme.CONTROL_DEFAULT
    return f"""
QWidget {{
    background-color: {Theme.BG_DARK};
    color: {Theme.TEXT_WHITE};
    font-size: {Theme.FONT_SIZE_BODY}px;
}}
QMainWindow {{
    background-color: {Theme.BG_DARK};
}}
QLabel {{
    background: transparent;
}}
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {Theme.INPUT_BG};
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: {Theme.RADIUS}px;
    min-height: {default.min_height}px;
    padding: {default.padding};
    color: {Theme.TEXT_WHITE};
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
    border-color: {Theme.INPUT_BORDER_HOVER};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {Theme.INPUT_BORDER_FOCUS};
}}
QPushButton {{
    background-color: {Theme.BG_CONTROL};
    border: none;
    border-radius: {Theme.RADIUS}px;
    min-height: {default.min_height}px;
    padding: {default.padding};
    color: {Theme.TEXT_WHITE};
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {Theme.BG_CONTROL_HOVER};
}}
QPushButton:pressed {{
    background-color: {Theme.BG_CONTROL_PRESSED};
}}
QPushButton:disabled {{
    color: {Theme.DISABLED_TEXT};
    background-color: {Theme.DISABLED_BG};
}}
QComboBox {{
    background-color: {Theme.INPUT_BG};
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: {Theme.RADIUS}px;
    min-height: {default.min_height}px;
    padding: {default.padding};
    color: {Theme.TEXT_WHITE};
    min-width: 80px;
}}
QComboBox:hover {{
    border-color: {Theme.INPUT_BORDER_HOVER};
}}
QComboBox:focus {{
    border-color: {Theme.INPUT_BORDER_FOCUS};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox::down-arrow {{
    image: none;
}}
QComboBox QAbstractItemView {{
    background-color: {Theme.BG_CONTROL};
    border: 1px solid {Theme.INPUT_BORDER_HOVER};
    color: {Theme.TEXT_WHITE};
    selection-background-color: {Theme.ACCENT};
    selection-color: {Theme.TEXT_WHITE};
}}
QSpinBox, QDoubleSpinBox {{
    background-color: {Theme.INPUT_BG};
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: {Theme.RADIUS}px;
    min-height: {default.min_height}px;
    padding: 3px 24px 3px 10px;
    color: {Theme.TEXT_WHITE};
    selection-background-color: {Theme.ACCENT};
    selection-color: {Theme.TEXT_WHITE};
}}
QSpinBox:hover, QDoubleSpinBox:hover {{
    border-color: {Theme.INPUT_BORDER_HOVER};
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {Theme.INPUT_BORDER_FOCUS};
}}
QSpinBox::up-button, QDoubleSpinBox::up-button {{
    subcontrol-origin: border;
    subcontrol-position: top right;
    width: 20px;
    background: {Theme.BG_RAISED};
    border: none;
    margin: 1px 1px 0 0;
    border-top-right-radius: 3px;
}}
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    subcontrol-origin: border;
    subcontrol-position: bottom right;
    width: 20px;
    background: {Theme.BG_RAISED};
    border: none;
    margin: 0 1px 1px 0;
    border-bottom-right-radius: 3px;
}}
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover {{
    background: {Theme.BG_CONTROL_HOVER};
}}
QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed,
QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed {{
    background: {Theme.BG_CONTROL_PRESSED};
}}
QSpinBox::up-button:disabled, QDoubleSpinBox::up-button:disabled,
QSpinBox::down-button:disabled, QDoubleSpinBox::down-button:disabled {{
    background: {Theme.DISABLED_BG};
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow,
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    width: 7px;
    height: 7px;
}}
QCheckBox {{
    spacing: 6px;
    background: transparent;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: 3px;
    background: {Theme.INPUT_BG};
}}
QCheckBox::indicator:hover {{
    border-color: {Theme.INPUT_BORDER_HOVER};
}}
QCheckBox::indicator:checked {{
    background: {Theme.ACCENT};
    border-color: {Theme.ACCENT};
}}
QGroupBox {{
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 14px;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 6px;
    color: {Theme.ACCENT};
}}
QTabWidget::pane {{
    border: none;
    background: {Theme.BG_DARK};
}}
QTabBar::tab {{
    background: {Theme.BG_MEDIUM};
    border: none;
    border-bottom: 2px solid transparent;
    padding: 7px 16px;
    color: {Theme.TEXT_MUTED};
    border-top-left-radius: {Theme.RADIUS}px;
    border-top-right-radius: {Theme.RADIUS}px;
}}
QTabBar::tab:selected {{
    background: {Theme.BG_DARK};
    color: {Theme.TEXT_WHITE};
    border-bottom: 2px solid {Theme.ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background: {Theme.BG_CONTROL};
    color: {Theme.TEXT_WHITE};
}}
QTabBar::tab:disabled {{
    color: {Theme.TEXT_DISABLED};
}}
QListWidget {{
    background-color: {Theme.BG_MEDIUM};
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: {Theme.RADIUS}px;
    color: {Theme.TEXT_WHITE};
}}
QListWidget::item:selected {{
    background-color: {Theme.ACCENT};
    color: {Theme.TEXT_WHITE};
}}
QProgressBar {{
    border: 1px solid {Theme.INPUT_BORDER};
    border-radius: 3px;
    background: {Theme.BG_MEDIUM};
    text-align: center;
    max-height: 8px;
}}
QProgressBar::chunk {{
    background: {Theme.ACCENT};
    border-radius: 2px;
}}
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
QScrollBar:horizontal, QScrollBar:vertical {{
    background: transparent;
    border: none;
    width: 0;
    height: 0;
}}
QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
    background: transparent;
    border: none;
    min-width: 0;
    min-height: 0;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    width: 0;
    height: 0;
    border: none;
    background: transparent;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: transparent;
}}
QScrollBar:vertical {{
    background: {Theme.BG_DARK};
    width: 0;
    border: none;
}}
QScrollBar::handle:vertical {{
    background: transparent;
    border-radius: 4px;
    min-height: 0;
}}
QScrollBar::handle:vertical:hover {{
    background: transparent;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
#DropletSidePanel {{
    background-color: {Theme.BG_DARK};
}}
#DropletSeparator {{
    background-color: {Theme.BORDER_COOL};
    border: none;
    border-radius: {Theme.SEPARATOR_THICKNESS // 2}px;
}}
QSplitter::handle {{
    background: {Theme.BG_DARK};
}}
QSplitter::handle:horizontal {{
    width: {Theme.SPLITTER_HANDLE_WIDTH}px;
}}
QSplitter::handle:vertical {{
    height: {Theme.SPLITTER_HANDLE_WIDTH}px;
}}
QStatusBar {{
    background-color: {Theme.BG_DARK};
    color: {Theme.TEXT_MUTED};
    font-size: {Theme.FONT_SIZE_SMALL}px;
}}
QMessageBox {{
    background: {Theme.BG_DARK};
}}
QMessageBox QLabel {{
    color: {Theme.TEXT_WHITE};
}}
"""
