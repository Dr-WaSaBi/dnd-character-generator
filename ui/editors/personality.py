from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QTextEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal

from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_SECTION_BORDER_HOVER,
    COLOR_BADGE_BG, COLOR_BADGE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER, COLOR_TEXT_SUBTEXT,
    COLOR_GOLD_RULE,
    FONT_HEADER, FONT_BODY,
)

FIELDS = [
    ("personality_traits", "Personality Traits",
     "What quirks, mannerisms, or attitudes define your character day-to-day?"),
    ("ideals", "Ideals",
     "What principles does your character live by? What drives them?"),
    ("bonds", "Bonds",
     "What people, places, or things does your character care most about?"),
    ("flaws", "Flaws",
     "What weakness, fear, or vice could be your character's undoing?"),
]


def _lbl(text, color, family, size, bold=False, italic=False,
         align=Qt.AlignmentFlag.AlignLeft) -> QLabel:
    w = QLabel(text)
    w.setAlignment(align)
    css = (f"color:{color};font-family:{family};font-size:{size}pt;"
           "background:transparent;border:none;")
    if bold:
        css += "font-weight:bold;"
    if italic:
        css += "font-style:italic;"
    w.setStyleSheet(css)
    return w


def _rule() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    f.setStyleSheet(f"background:{COLOR_GOLD_RULE};border:none;")
    return f


_TEXTEDIT_CSS = (
    f"QTextEdit{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:5px;"
    f"font-family:{FONT_BODY};font-size:10pt;padding:4px;}}"
    f"QTextEdit:focus{{border:2px solid {COLOR_SECTION_BORDER_HOVER};}}"
)


class PersonalityEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ⑧  —  Personality")
        self.setMinimumSize(560, 560)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._editors: dict[str, QTextEdit] = {}
        self._build_ui(existing or {})

    def _build_ui(self, data: dict):
        root = QVBoxLayout(self)
        root.setContentsMargins(26, 20, 26, 18)
        root.setSpacing(10)

        root.addWidget(_lbl("🎭  PERSONALITY", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))
        root.addWidget(_rule())

        for key, title, hint in FIELDS:
            root.addWidget(_lbl(title.upper(), COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))

            ed = QTextEdit()
            ed.setPlaceholderText(hint)
            ed.setMinimumHeight(90)
            ed.setMaximumHeight(110)
            ed.setStyleSheet(_TEXTEDIT_CSS)
            if data.get(key):
                ed.setPlainText(data[key])
            self._editors[key] = ed
            root.addWidget(ed)

        root.addStretch()
        root.addWidget(_rule())

        btn_row = QHBoxLayout()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        btn_row.addStretch()
        save = self._mk_btn("Save & Close", secondary=False)
        save.clicked.connect(self._on_save)
        btn_row.addWidget(save)
        root.addLayout(btn_row)

    def _on_save(self):
        out = {key: self._editors[key].toPlainText().strip() for key, _, _ in FIELDS}
        self.data_saved.emit(out)
        self.accept()

    @staticmethod
    def _mk_btn(label: str, secondary: bool) -> QPushButton:
        btn = QPushButton(label)
        btn.setFixedHeight(36)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        if secondary:
            btn.setStyleSheet(
                f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
                f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
                f"font-family:{FONT_BODY};font-size:10pt;padding:0 16px;}}"
                f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
            )
        else:
            btn.setStyleSheet(
                f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
                f"border:2px solid {COLOR_GOLD_RULE};border-radius:6px;"
                f"font-family:{FONT_HEADER};font-size:11pt;font-weight:bold;padding:0 20px;}}"
                f"QPushButton:hover{{background:#A02020;}}"
            )
        return btn
