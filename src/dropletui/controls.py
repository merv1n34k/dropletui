"""Reusable control constructors."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyle
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QSlider,
    QWidget,
)

from dropletui.theme import Theme, button_qss, control_size, spacing

ButtonVariant = Literal["neutral", "primary", "success", "danger", "warning"]
ControlSize = Literal["inline", "default", "large", "stage"]


class DropletSlider(QSlider):
    """Slider that treats step as valid value granularity, including mouse drags."""

    def __init__(self, orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> None:
        super().__init__(orientation)
        self._step = 1

    def setSingleStep(self, step: int) -> None:  # noqa: N802
        self._step = max(1, int(step))
        super().setSingleStep(self._step)

    def setValue(self, value: int) -> None:  # noqa: N802
        super().setValue(self._snap(value))

    def setRange(self, minimum: int, maximum: int) -> None:  # noqa: N802
        super().setRange(minimum, maximum)
        self.setValue(self.value())

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self.setValue(self._value_from_position(event.position()))
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.setValue(self._value_from_position(event.position()))
            event.accept()
            return
        super().mouseMoveEvent(event)

    def wheelEvent(self, event) -> None:  # noqa: N802
        direction = 1 if event.angleDelta().y() > 0 else -1
        self.setValue(self.value() + direction * self._step)
        event.accept()

    def keyPressEvent(self, event) -> None:  # noqa: N802
        key = event.key()
        if key in {Qt.Key.Key_Left, Qt.Key.Key_Down}:
            self.setValue(self.value() - self._step)
            event.accept()
            return
        if key in {Qt.Key.Key_Right, Qt.Key.Key_Up}:
            self.setValue(self.value() + self._step)
            event.accept()
            return
        if key == Qt.Key.Key_PageDown:
            self.setValue(self.value() - self.pageStep())
            event.accept()
            return
        if key == Qt.Key.Key_PageUp:
            self.setValue(self.value() + self.pageStep())
            event.accept()
            return
        if key == Qt.Key.Key_Home:
            self.setValue(self.minimum())
            event.accept()
            return
        if key == Qt.Key.Key_End:
            self.setValue(self.maximum())
            event.accept()
            return
        super().keyPressEvent(event)

    def _snap(self, value: int) -> int:
        minimum = self.minimum()
        maximum = self.maximum()
        snapped = minimum + round((int(value) - minimum) / self._step) * self._step
        while snapped > maximum:
            snapped -= self._step
        return max(minimum, snapped)

    def _value_from_position(self, position) -> int:
        if self.orientation() == Qt.Orientation.Horizontal:
            pos = int(position.x())
            span = max(1, self.width())
        else:
            pos = int(position.y())
            span = max(1, self.height())

        value = QStyle.sliderValueFromPosition(
            self.minimum(),
            self.maximum(),
            pos,
            span,
            self.invertedAppearance(),
        )
        return self._snap(value)


def apply_button_style(
    widget: QPushButton,
    *,
    variant: ButtonVariant = "neutral",
    size: ControlSize = "default",
    flat: bool = False,
) -> QPushButton:
    widget.setStyleSheet(button_qss(variant, size=size, flat=flat))
    if not flat:
        apply_control_size(widget, size)
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
    widget = button(text, checkable=True)
    apply_stage_state(widget, active=active, enabled=enabled)
    widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return widget


def segmented_control(
    items: Iterable[str],
    *,
    active_index: int = 0,
    enabled_until: int | None = None,
    size: ControlSize = "default",
) -> QWidget:
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    for index, item in enumerate(items):
        enabled = enabled_until is None or index <= enabled_until
        widget = button(item, size=size, checkable=True)
        apply_stage_state(widget, active=index == active_index, enabled=enabled, size=size)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addWidget(widget, 1)
    return container


def line_edit(
    text: str = "",
    *,
    placeholder: str = "",
    width: int | None = None,
    size: ControlSize = "default",
) -> QLineEdit:
    widget = QLineEdit(text)
    widget.setPlaceholderText(placeholder)
    apply_control_size(widget, size)
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
    size: ControlSize = "default",
) -> QSpinBox:
    widget = QSpinBox()
    widget.setRange(minimum, maximum)
    widget.setValue(value)
    widget.setSingleStep(step)
    widget.setSuffix(suffix)
    apply_control_size(widget, size)
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
    size: ControlSize = "default",
) -> QDoubleSpinBox:
    widget = QDoubleSpinBox()
    widget.setRange(minimum, maximum)
    widget.setValue(value)
    widget.setSingleStep(step)
    widget.setDecimals(decimals)
    widget.setSuffix(suffix)
    apply_control_size(widget, size)
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def combo_box(
    items: Iterable[str] = (),
    *,
    width: int | None = None,
    size: ControlSize = "default",
) -> QComboBox:
    widget = QComboBox()
    widget.addItems(list(items))
    apply_control_size(widget, size)
    if width is not None:
        widget.setFixedWidth(width)
    return widget


def slider(
    *,
    orientation: Qt.Orientation = Qt.Orientation.Horizontal,
    minimum: int = 0,
    maximum: int = 100,
    value: int = 0,
    step: int = 1,
    page_step: int | None = None,
) -> QSlider:
    widget = DropletSlider(orientation)
    widget.setRange(minimum, maximum)
    widget.setSingleStep(step)
    widget.setPageStep(page_step if page_step is not None else step)
    widget.setValue(value)
    apply_control_size(widget, "default")
    return widget


def check_box(text: str, *, checked: bool = False) -> QCheckBox:
    widget = QCheckBox(text)
    widget.setChecked(checked)
    return widget


def apply_stage_state(
    widget: QPushButton,
    *,
    active: bool,
    enabled: bool = True,
    size: ControlSize = "default",
) -> None:
    widget.setEnabled(enabled)
    widget.setChecked(active)
    token = control_size(size)
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
        f"border-radius: 0; min-height: {token.height}px; max-height: {token.height}px; "
        "padding: 0; "
        f"font-size: {token.font_size}px; font-weight: {weight}; }}"
        f"QPushButton:hover {{ background-color: {Theme.BG_CONTROL_HOVER}; }}"
    )
    apply_control_size(widget, size)
    widget.setCursor(Qt.CursorShape.PointingHandCursor if enabled else Qt.CursorShape.ArrowCursor)


def apply_control_size(widget: QWidget, size: ControlSize = "default") -> QWidget:
    token = control_size(size)
    widget.setMinimumHeight(token.height)
    widget.setMaximumHeight(token.height)
    return widget


def apply_control_gap(layout, value: str | int = "control") -> None:
    layout.setSpacing(spacing(value))
