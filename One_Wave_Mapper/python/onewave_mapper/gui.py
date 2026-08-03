"""Entry points for the One-Wave Mapper UI.

    python -m onewave_mapper.gui            # full MapperWindow (Raw
                                              # waveform, Envelope,
                                              # Spectrum, Spectrogram,
                                              # Phase, Interference,
                                              # Resonance, Modulation)
    python -m onewave_mapper.gui --simple    # the original single-panel
                                              # live oscilloscope window

Requires a real display (or QT_QPA_PLATFORM=offscreen for headless
testing, as tests/test_gui_smoke.py and tests/test_mapper_window.py use).
"""

from __future__ import annotations

import sys


def main() -> None:
    from PySide6 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)

    if "--simple" in sys.argv:
        from onewave_mapper.ui.oscilloscope_window import OscilloscopeWindow
        window = OscilloscopeWindow()
    else:
        from onewave_mapper.ui.mapper_window import MapperWindow
        window = MapperWindow()

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
