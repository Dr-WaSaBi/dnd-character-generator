import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D Character Generator")
        self.setMinimumSize(900, 700)

        label = QLabel("D&D Character Generator\n\nComing soon...", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
