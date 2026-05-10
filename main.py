import sys
from PyQt6.QtWidgets import QApplication
from ui import CharacterSheetWindow
from ui.styles import SHEET_STYLE


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(SHEET_STYLE)
    window = CharacterSheetWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
