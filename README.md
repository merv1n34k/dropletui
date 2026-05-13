# dropletui

Shared PySide6 UI components for the droplet desktop applications.

`dropletui` centralizes theme tokens, application setup, controls, panels, splitters,
status widgets, and demo components so `droplegen`, `droplesim`, and `pylonguy` can
use the same UI and UX instead of maintaining separate copies.

## Features

- Unified dark PySide6 theme with shared colors, spacing, fonts, and control sizes
- Reusable controls for buttons, line edits, combo boxes, spin boxes, and check boxes
- Shared side and bottom panel constructors
- Rounded draggable splitters with optional panel collapse and restore behavior
- PyQtGraph theme configuration helpers
- Demo app for quickly checking visual changes

## Installation

### From PyPI

```bash
pip install dropletui
```

### From source

```bash
git clone https://github.com/merv1n34k/dropletui.git
cd dropletui
uv sync
```

### Requirements

- Python 3.12+
- PySide6
- pyqtgraph
- uv

## Usage

```bash
uv run dropletui-demo
```

In an application:

```python
import dropletui as ui

app = ui.create_app("my app")
window = ...
window.show()
app.exec()
```

## Release

Publishing to PyPI is handled by the `Publish to PyPI` GitHub Actions workflow when
a GitHub release is published.

## License

Distributed under the MIT License. See `LICENSE` for more information.
