"""Reusable control constructors."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QPushButton,
    QSpinBox,
)

from dropletui.theme import Theme, button_qss, control_size

ButtonVariant = Literal["neutral", "primary", "success", "danger", "warning"]
ControlSize = Literal["inline", "default", "large", "stage"]


def apply_button_style(
    widget: QPushButton,
    *,
    variant: ButtonVariant = "neutral",
    size: ControlSize = "default",
    flat: bool = False,
) -> QPushButton:
    widget.setStyleSheet(button_qss(variant, size=size, flat=flat))
    return widget


def button(
    text: str,
    *,
    variant: ButtonVariant = "neutral",
    size: ControlSize = "default",
    checkable: bool = False,
    flat: bool = False,
) -> QPushButton:
    widget = QPushButton(text)
    widget.setCheckable(checkable)
    apply_button_style(widget, variant=variant, size=size, flat=flat)
    return widget


def stage_button(text: str, *, active: bool = False, enabled: bool = True) -> QPushButton:
    widget = button(text, variant="primary" if active else "neutral", size="stage", checkable=True)
    widget.setChecked(active)
    widget.setEnabled(enabled)
    return widget


def line_edit(
    text: str = "",
    *,
    placeholder: str = "",
    width: int | None = None,
) -> QLineEdit:
    widget = QLineEdit(text)
    widget.setPlaceholderText(placeholder)
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def int_box(
    *,
    minimum: int = 0,
    maximum: int = 100,
    value: int = 0,
    step: int = 1,
    suffix: str = "",
    width: int | None = None,
) -> QSpinBox:
    widget = QSpinBox()
    widget.setRange(minimum, maximum)
    widget.setValue(value)
    widget.setSingleStep(step)
    widget.setSuffix(suffix)
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def double_box(
    *,
    minimum: float = 0.0,
    maximum: float = 100.0,
    value: float = 0.0,
    step: float = 1.0,
    decimals: int = 2,
    suffix: str = "",
    width: int | None = None,
) -> QDoubleSpinBox:
    widget = QDoubleSpinBox()
    widget.setRange(minimum, maximum)
    widget.setValue(value)
    widget.setSingleStep(step)
    widget.setDecimals(decimals)
    widget.setSuffix(suffix)
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def combo_box(items: Iterable[str] = (), *, width: int | None = None) -> QComboBox:
    widget = QComboBox()
    widget.addItems(list(items))
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def check_box(text: str, *, checked: bool = False) -> QCheckBox:
    widget = QCheckBox(text)
    widget.setChecked(checked)
    return widget


def apply_stage_state(widget: QPushButton, *, active: bool, enabled: bool = True) -> None:
    widget.setEnabled(enabled)
    widget.setChecked(active)
    token = control_size("stage")
    if active:
        bg = Theme.ACCENT
        color = Theme.TEXT_WHITE
        weight = "600"
    elif not enabled:
        bg = Theme.BG_MEDIUM
        color = Theme.TEXT_DISABLED
        weight = "400"
    else:
        bg = Theme.BG_CONTROL
        color = Theme.TEXT_WHITE
        weight = "400"
    widget.setStyleSheet(
        f"QPushButton {{ background-color: {bg}; color: {color}; border: none; "
        f"border-radius: 0; min-height: {token.min_height}px; padding: {token.padding}; "
        f"font-size: {token.font_size}px; font-weight: {weight}; }}"
        f"QPushButton:hover {{ background-color: {Theme.BG_CONTROL_HOVER}; }}"
    )
    widget.setCursor(Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor)
