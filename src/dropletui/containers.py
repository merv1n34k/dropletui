"""Layout and container constructors."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QFrame,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QSizePolicy,
    QSplitter,
    QSplitterHandle,
    QVBoxLayout,
    QWidget,
)

from dropletui.theme import Theme


class DropletSplitterHandle(QSplitterHandle):
    """Plain splitter handle with optional double-click panel toggle."""

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(Theme.BG_DARK))

        color = Theme.BORDER_HOVER if self.underMouse() else Theme.BORDER_COOL
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)

        ratio = Theme.SPLITTER_MARK_LENGTH_RATIO
        thickness = Theme.SPLITTER_MARK_THICKNESS
        if self.orientation() == Qt.Orientation.Horizontal:
            length = max(thickness, self.height() * ratio)
            rect = QRectF(
                (self.width() - thickness) / 2,
                (self.height() - length) / 2,
                thickness,
                length,
            )
        else:
            length = max(thickness, self.width() * ratio)
            rect = QRectF(
                (self.width() - length) / 2,
                (self.height() - thickness) / 2,
                length,
                thickness,
            )

        radius = thickness / 2
        painter.drawRoundedRect(rect, radius, radius)

    def enterEvent(self, event) -> None:  # noqa: N802
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802
        self.update()
        super().leaveEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802
        splitter_widget = self.splitter()
        if isinstance(splitter_widget, DropletSplitter) and splitter_widget.collapse_index is not None:
            splitter_widget.toggle_panel()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)


class DropletSplitter(QSplitter):
    """Standard draggable splitter with optional panel collapse/restore behavior."""

    def __init__(
        self,
        orientation: Qt.Orientation,
        *,
        collapse_index: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(orientation, parent)
        self.collapse_index = collapse_index
        self._saved_sizes: dict[int, list[int]] = {}

    def createHandle(self) -> QSplitterHandle:  # noqa: N802
        return DropletSplitterHandle(self.orientation(), self)

    def is_panel_collapsed(self, index: int | None = None) -> bool:
        panel_index = self._panel_index(index)
        sizes = self.sizes()
        return panel_index < len(sizes) and sizes[panel_index] <= 0

    def collapse_panel(self, index: int | None = None) -> None:
        panel_index = self._panel_index(index)
        sizes = self.sizes()
        if panel_index >= len(sizes) or sizes[panel_index] <= 0:
            return

        self._saved_sizes[panel_index] = sizes[:]
        receiver = panel_index - 1 if panel_index > 0 else panel_index + 1
        if receiver < len(sizes):
            sizes[receiver] += sizes[panel_index]
        sizes[panel_index] = 0
        self.setSizes(sizes)

    def expand_panel(self, index: int | None = None) -> None:
        panel_index = self._panel_index(index)
        saved = self._saved_sizes.get(panel_index)
        if saved and len(saved) == self.count():
            self.setSizes(saved)
            return

        sizes = self.sizes()
        if panel_index >= len(sizes) or sizes[panel_index] > 0:
            return
        donor = panel_index - 1 if panel_index > 0 else panel_index + 1
        if donor >= len(sizes) or sizes[donor] <= 1:
            return
        restored = max(240, sizes[donor] // 3)
        restored = min(restored, max(1, sizes[donor] - 1))
        sizes[donor] -= restored
        sizes[panel_index] = restored
        self.setSizes(sizes)

    def toggle_panel(self, index: int | None = None) -> None:
        if self.is_panel_collapsed(index):
            self.expand_panel(index)
        else:
            self.collapse_panel(index)

    def _panel_index(self, index: int | None) -> int:
        panel_index = self.collapse_index if index is None else index
        if panel_index is None:
            raise ValueError("No collapse panel index configured")
        return panel_index


def hbox(*widgets: QWidget, spacing: int = Theme.SPACE_2, margins: int = 0) -> QWidget:
    container = QWidget()
    layout = QHBoxLayout(container)
    layout.setContentsMargins(margins, margins, margins, margins)
    layout.setSpacing(spacing)
    for widget in widgets:
        layout.addWidget(widget)
    return container


def vbox(*widgets: QWidget, spacing: int = Theme.SPACE_2, margins: int = 0) -> QWidget:
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(margins, margins, margins, margins)
    layout.setSpacing(spacing)
    for widget in widgets:
        layout.addWidget(widget)
    return container


def section(title: str, *, spacing: int = Theme.SPACE_2) -> tuple[QGroupBox, QVBoxLayout]:
    group = QGroupBox(title)
    layout = QVBoxLayout(group)
    layout.setContentsMargins(
        Theme.PANEL_PADDING,
        Theme.PANEL_PADDING,
        Theme.PANEL_PADDING,
        Theme.PANEL_PADDING,
    )
    layout.setSpacing(spacing)
    return group, layout


def form_panel(title: str, rows: Iterable[tuple[str, QWidget]]) -> QGroupBox:
    group = QGroupBox(title)
    layout = QFormLayout(group)
    layout.setSpacing(Theme.SPACE_2)
    for label, widget in rows:
        layout.addRow(label, widget)
    return group


def side_panel(
    *widgets: QWidget,
    spacing: int = Theme.SPACE_2,
    margins: int = Theme.PANEL_PADDING,
    minimum_width: int | None = None,
    maximum_width: int | None = None,
) -> tuple[QWidget, QVBoxLayout]:
    """Create a plain droplegen-style side panel without custom splitter handles."""
    panel = QWidget()
    panel.setObjectName("DropletSidePanel")
    panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    if minimum_width is not None:
        panel.setMinimumWidth(minimum_width)
    if maximum_width is not None:
        panel.setMaximumWidth(maximum_width)

    layout = QVBoxLayout(panel)
    layout.setContentsMargins(margins, margins, margins, margins)
    layout.setSpacing(spacing)
    for widget in widgets:
        layout.addWidget(widget)
    return panel, layout


def splitter(
    orientation: Qt.Orientation,
    *widgets: QWidget,
    sizes: Sequence[int] | None = None,
    stretch: Sequence[int] | None = None,
    collapsible: bool | Sequence[bool] = False,
    collapse_index: int | None = None,
    handle_width: int = Theme.SPLITTER_HANDLE_WIDTH,
    pane_margins: int = Theme.SPLITTER_PADDING,
) -> DropletSplitter:
    """Create the shared one-line splitter used across droplet apps."""
    split = DropletSplitter(orientation, collapse_index=collapse_index)
    split.setObjectName("DropletSplitter")
    split.setHandleWidth(handle_width)
    split.setOpaqueResize(True)
    split.setChildrenCollapsible(False)
    split.setContentsMargins(
        Theme.SPLITTER_PADDING,
        Theme.SPLITTER_PADDING,
        Theme.SPLITTER_PADDING,
        Theme.SPLITTER_PADDING,
    )

    for index, widget in enumerate(widgets):
        split.addWidget(_splitter_pane(widget, pane_margins))
        if stretch is not None and index < len(stretch):
            split.setStretchFactor(index, stretch[index])
        if isinstance(collapsible, Sequence):
            split.setCollapsible(index, index < len(collapsible) and collapsible[index])
        else:
            split.setCollapsible(index, collapsible)

    if collapse_index is not None and collapse_index < len(widgets):
        split.setCollapsible(collapse_index, True)

    if sizes is not None:
        split.setSizes(list(sizes))
    return split


def horizontal_splitter(
    *widgets: QWidget,
    sizes: Sequence[int] | None = None,
    stretch: Sequence[int] | None = None,
    collapsible: bool | Sequence[bool] = False,
    collapse_index: int | None = None,
    pane_margins: int = Theme.SPLITTER_PADDING,
) -> DropletSplitter:
    return splitter(
        Qt.Orientation.Horizontal,
        *widgets,
        sizes=sizes,
        stretch=stretch,
        collapsible=collapsible,
        collapse_index=collapse_index,
        pane_margins=pane_margins,
    )


def vertical_splitter(
    *widgets: QWidget,
    sizes: Sequence[int] | None = None,
    stretch: Sequence[int] | None = None,
    collapsible: bool | Sequence[bool] = False,
    collapse_index: int | None = None,
    pane_margins: int = Theme.SPLITTER_PADDING,
) -> DropletSplitter:
    return splitter(
        Qt.Orientation.Vertical,
        *widgets,
        sizes=sizes,
        stretch=stretch,
        collapsible=collapsible,
        collapse_index=collapse_index,
        pane_margins=pane_margins,
    )


def split_view(
    primary: QWidget,
    secondary: QWidget,
    *,
    side_position: str = "right",
    sizes: Sequence[int] | None = None,
    collapsible: bool = False,
) -> DropletSplitter:
    """Create a standard primary-content plus side-panel split view."""
    if side_position not in {"left", "right"}:
        raise ValueError("side_position must be 'left' or 'right'")
    if side_position == "left":
        return horizontal_splitter(
            secondary,
            primary,
            sizes=sizes or (360, 1000),
            stretch=(0, 1),
            collapse_index=0 if collapsible else None,
        )
    return horizontal_splitter(
        primary,
        secondary,
        sizes=sizes or (1000, 360),
        stretch=(1, 0),
        collapse_index=1 if collapsible else None,
    )


def bottom_split_view(
    primary: QWidget,
    bottom: QWidget,
    *,
    sizes: Sequence[int] | None = None,
    collapsible: bool = False,
) -> DropletSplitter:
    """Create a standard primary-content plus bottom-panel split view."""
    return vertical_splitter(
        primary,
        bottom,
        sizes=sizes or (1000, 360),
        stretch=(1, 0),
        collapse_index=1 if collapsible else None,
    )


def separator(orientation: Qt.Orientation = Qt.Orientation.Horizontal) -> QFrame:
    line = QFrame()
    line.setObjectName("DropletSeparator")
    line.setFrameShape(
        QFrame.Shape.HLine
        if orientation == Qt.Orientation.Horizontal
        else QFrame.Shape.VLine
    )
    line.setFrameShadow(QFrame.Shadow.Plain)
    if orientation == Qt.Orientation.Horizontal:
        line.setFixedHeight(Theme.SEPARATOR_THICKNESS)
    else:
        line.setFixedWidth(Theme.SEPARATOR_THICKNESS)
    return line


def _splitter_pane(widget: QWidget, margins: int) -> QWidget:
    if margins <= 0:
        return widget

    pane = QWidget()
    pane.setObjectName("DropletSplitterPane")
    pane.setSizePolicy(widget.sizePolicy())
    layout = QVBoxLayout(pane)
    layout.setContentsMargins(margins, margins, margins, margins)
    layout.setSpacing(0)
    layout.addWidget(widget)
    return pane


def toolbar(title: str, *widgets: QWidget) -> QWidget:
    container = QWidget()
    container.setMinimumHeight(44)
    layout = QHBoxLayout(container)
    layout.setContentsMargins(Theme.SPACE_3, Theme.SPACE_2, Theme.SPACE_3, Theme.SPACE_2)
    layout.setSpacing(Theme.SPACE_2)

    title_label = QLabel(title)
    font = QFont()
    font.setPointSize(Theme.FONT_SIZE_TITLE)
    font.setWeight(QFont.Weight.DemiBold)
    title_label.setFont(font)
    layout.addWidget(title_label)
    layout.addSpacing(Theme.SPACE_4)

    for widget in widgets:
        layout.addWidget(widget)
    layout.addStretch()
    return container


def clear_layout(layout: QLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget() is not None:
            item.widget().deleteLater()
        elif item.layout() is not None:
            clear_layout(item.layout())
