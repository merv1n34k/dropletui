"""Small visual demo for the shared component system."""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

import dropletui as ui
from dropletui.controls import apply_stage_state


class DemoWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("dropletui demo")
        self.resize(900, 560)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(
            ui.Theme.WINDOW_PADDING,
            ui.Theme.WINDOW_PADDING,
            ui.Theme.WINDOW_PADDING,
            ui.Theme.WINDOW_PADDING,
        )
        root.setSpacing(6)

        side_toggle = ui.button("Hide Side", variant="neutral")
        bottom_toggle = ui.button("Hide Bottom", variant="neutral")

        root.addWidget(
            ui.toolbar(
                "dropletui",
                ui.button("Connect", variant="success"),
                ui.button("Disconnect", variant="danger"),
                ui.button("Record", variant="neutral"),
                side_toggle,
                bottom_toggle,
            )
        )

        stages = QHBoxLayout()
        stages.setSpacing(1)
        for i, label in enumerate(["1. Geometry", "2. Edges", "3. Phase", "4. Simulate"]):
            btn = ui.stage_button(label, active=i == 0, enabled=i < 3)
            apply_stage_state(btn, active=i == 0, enabled=i < 3)
            stages.addWidget(btn, 1)
        root.addLayout(stages)

        controls_panel, controls_panel_layout = ui.side_panel(minimum_width=260)
        controls, controls_layout = ui.section("Controls")
        controls_layout.addWidget(ui.line_edit(placeholder="Pipeline name"))
        controls_layout.addWidget(ui.int_box(minimum=0, maximum=1000, value=50, suffix=" steps"))
        controls_layout.addWidget(ui.double_box(value=2.5, suffix=" um", decimals=2))
        controls_layout.addWidget(ui.combo_box(["Oil", "Cells", "Beads"]))
        controls_layout.addWidget(ui.button("Apply", variant="primary"))
        controls_panel_layout.addWidget(controls)
        controls_panel_layout.addStretch()

        preview, preview_layout = ui.section("Primary Workspace")
        placeholder = QLabel("plots / camera / geometry")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(260)
        placeholder.setStyleSheet(
            f"background: {ui.Theme.BG_DARKER}; color: {ui.Theme.TEXT_MUTED};"
        )
        preview_layout.addWidget(placeholder)

        status, status_layout = ui.section("Readouts")
        status_layout.addWidget(ui.metric_readout("FPS", "120.0"))
        status_layout.addWidget(ui.metric_readout("REC", "OFF", kind="muted"))
        status_layout.addWidget(ui.separator())
        status_layout.addWidget(ui.status_label("Connected (simulated)", kind="success"))
        status_layout.addWidget(ui.status_label("No flow correction applied", kind="warning"))

        workspace = ui.bottom_split_view(preview, status, sizes=(380, 160), collapsible=True)
        shell = ui.split_view(
            workspace,
            controls_panel,
            side_position="left",
            sizes=(300, 600),
            collapsible=True,
        )
        root.addWidget(shell, stretch=1)

        def toggle_side() -> None:
            shell.toggle_panel()
            side_toggle.setText("Show Side" if shell.is_panel_collapsed() else "Hide Side")

        def toggle_bottom() -> None:
            workspace.toggle_panel()
            bottom_toggle.setText("Show Bottom" if workspace.is_panel_collapsed() else "Hide Bottom")

        side_toggle.clicked.connect(toggle_side)
        bottom_toggle.clicked.connect(toggle_bottom)


def main() -> int:
    app = ui.create_app("dropletui demo", sys.argv)
    window = DemoWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
