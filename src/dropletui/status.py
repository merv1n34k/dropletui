"""Status and readout widgets."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from dropletui.theme import Theme, control_size, text_qss, value_label_qss


def status_label(text: str = "", *, kind: str = "muted", small: bool = True) -> QLabel:
    label = QLabel(text)
    label.setStyleSheet(text_qss(kind, font_size=Theme.FONT_SIZE_SMALL if small else None))
    return label


def metric_readout(label: str, value: str = "0", *, kind: str = "success") -> QWidget:
    token = control_size("default")
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    name = QLabel(label)
    name.setMinimumHeight(token.height)
    name.setMaximumHeight(token.height)
    name.setStyleSheet(
        f"background: {Theme.BG_CONTROL}; "
        f"{text_qss('muted', bold=True, padding=token.padding)}"
    )
    val = QLabel(value)
    val.setMinimumHeight(token.height)
    val.setMaximumHeight(token.height)
    val.setStyleSheet(value_label_qss(kind, padding=token.padding))

    layout.addWidget(name)
    layout.addWidget(val, 1)
    return container
