"""Entry point for the live oscilloscope UI.

    python -m onewave_mapper.gui

Requires a real display (or QT_QPA_PLATFORM=offscreen for headless
testing, as tests/test_gui_smoke.py uses).
"""

from __future__ import annotations

import sys


def main() -> None:
    from PySide6 import QtWidgets
    from onewave_mapper.ui.oscilloscope_window import OscilloscopeWindow

    app = QtWidgets.QApplication(sys.argv)
    window = OscilloscopeWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
