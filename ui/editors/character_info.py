# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/editors/character_info.py                              ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Editor dialog for basic character identity (name, class, level,     ║
# ║  race, background, alignment, XP, player name).                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QLineEdit, QComboBox,
    QSpinBox, QWidget,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_SECTION_BORDER_HOVER,
    COLOR_BADGE_BG, COLOR_BADGE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER, COLOR_TEXT_SUBTEXT,
    COLOR_GOLD_RULE,
    FONT_HEADER, FONT_BODY,
)

ALIGNMENTS = [
    "Lawful Good", "Neutral Good", "Chaotic Good",
    "Lawful Neutral", "True Neutral", "Chaotic Neutral",
    "Lawful Evil", "Neutral Evil", "Chaotic Evil",
]

CLASSES = [
    "Barbarian", "Bard", "Cleric", "Druid", "Fighter",
    "Monk", "Paladin", "Ranger", "Rogue", "Sorcerer",
    "Warlock", "Wizard", "Artificer",
]

RACES = [
    "Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf",
    "Half-Orc", "Halfling", "Human", "Tiefling",
]

BACKGROUNDS = [
    "Acolyte", "Charlatan", "Criminal", "Entertainer",
    "Folk Hero", "Guild Artisan", "Hermit", "Noble",
    "Outlander", "Sage", "Sailor", "Soldier", "Urchin",
]


def _lbl(text, color, family, size, bold=False, italic=False,
         align=Qt.AlignmentFlag.AlignLeft) -> QLabel:
    """Create a styled QLabel with the given text, color, font, and alignment."""
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
    """Return a 1px gold horizontal rule widget for visual section separation."""
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    f.setStyleSheet(f"background:{COLOR_GOLD_RULE};border:none;")
    return f


_INPUT_CSS = (
    f"QLineEdit, QComboBox, QSpinBox {{"
    f"background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:2px solid {COLOR_SECTION_BORDER};"
    f"border-radius:4px;"
    f"font-family:{FONT_BODY};"
    f"font-size:10pt;"
    f"padding:3px 6px;"
    f"}}"
    f"QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{"
    f"border:2px solid {COLOR_SECTION_BORDER_HOVER};"
    f"background:{COLOR_PARCHMENT_HOVER};"
    f"}}"
    f"QComboBox::drop-down {{"
    f"border:none;"
    f"}}"
    f"QComboBox QAbstractItemView {{"
    f"background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"selection-background-color:{COLOR_BADGE_BG};"
    f"selection-color:{COLOR_BADGE_TEXT};"
    f"font-family:{FONT_BODY};"
    f"font-size:10pt;"
    f"}}"
    f"QSpinBox::up-button, QSpinBox::down-button {{"
    f"width:18px;"
    f"}}"
)


def _combo(options: list[str], placeholder: str = "") -> QComboBox:
    """Create a styled QComboBox pre-populated with options and an optional placeholder item."""
    c = QComboBox()
    c.setStyleSheet(_INPUT_CSS)
    c.setFixedHeight(32)
    if placeholder:
        c.addItem(placeholder)
        c.setItemData(0, Qt.ItemFlag.NoItemFlags, Qt.ItemDataRole.UserRole - 1)
    c.addItems(options)
    return c


def _line(placeholder: str = "") -> QLineEdit:
    """Create a styled QLineEdit with an optional placeholder string."""
    e = QLineEdit()
    e.setStyleSheet(_INPUT_CSS)
    e.setFixedHeight(32)
    if placeholder:
        e.setPlaceholderText(placeholder)
    return e


class CharacterInfoEditor(QDialog):
    info_saved = pyqtSignal(dict)

    def __init__(self, existing: dict | None = None, parent=None):
        """Initialize the dialog, build the grid of input fields, and populate from existing data."""
        super().__init__(parent)
        self.setWindowTitle("Section ①  —  Character Info")
        self.setMinimumSize(560, 440)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._build_ui()
        if existing:
            self._load(existing)

    def _build_ui(self):
        """Build the character info grid (name, class, level, race, background, alignment, XP, player)."""
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 20)
        root.setSpacing(14)

        root.addWidget(_lbl("⚔  CHARACTER  INFO", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))
        root.addWidget(_rule())

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(10)

        # Row 0 — Character Name (full width)
        grid.addWidget(_lbl("Character Name", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 0, 0, 1, 4)
        self._name = _line("e.g. Aldric Stormveil")
        self._name.setStyleSheet(_INPUT_CSS)
        grid.addWidget(self._name, 1, 0, 1, 4)

        # Row 2 — Class | Level
        grid.addWidget(_lbl("Class", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 2, 0, 1, 3)
        grid.addWidget(_lbl("Level", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 2, 3)

        self._class = _combo(CLASSES, "— Select Class —")
        grid.addWidget(self._class, 3, 0, 1, 3)

        self._level = QSpinBox()
        self._level.setRange(1, 20)
        self._level.setValue(1)
        self._level.setFixedHeight(32)
        self._level.setStyleSheet(_INPUT_CSS)
        grid.addWidget(self._level, 3, 3)

        # Row 4 — Race | Background
        grid.addWidget(_lbl("Race", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 4, 0, 1, 2)
        grid.addWidget(_lbl("Background", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 4, 2, 1, 2)

        self._race = _combo(RACES, "— Select Race —")
        grid.addWidget(self._race, 5, 0, 1, 2)

        self._background = _combo(BACKGROUNDS, "— Select Background —")
        grid.addWidget(self._background, 5, 2, 1, 2)

        # Row 6 — Alignment | XP
        grid.addWidget(_lbl("Alignment", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 6, 0, 1, 2)
        grid.addWidget(_lbl("Experience Points", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 6, 2, 1, 2)

        self._alignment = _combo(ALIGNMENTS, "— Select Alignment —")
        grid.addWidget(self._alignment, 7, 0, 1, 2)

        self._xp = _line("0")
        self._xp.setValidator(QIntValidator(0, 999_999))
        grid.addWidget(self._xp, 7, 2, 1, 2)

        # Row 8 — Player Name
        grid.addWidget(_lbl("Player Name", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True), 8, 0, 1, 4)
        self._player = _line("Your name")
        grid.addWidget(self._player, 9, 0, 1, 4)

        root.addLayout(grid)
        root.addStretch()
        root.addWidget(_rule())

        # Buttons
        row = QHBoxLayout()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        row.addWidget(cancel)
        row.addStretch()
        save = self._mk_btn("Save & Close", secondary=False)
        save.clicked.connect(self._on_save)
        row.addWidget(save)
        root.addLayout(row)

    @staticmethod
    def _mk_btn(label: str, secondary: bool) -> QPushButton:
        """Create a styled primary (dark red) or secondary (parchment) push button."""
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

    def _on_save(self):
        """Collect all field values into a dict, emit info_saved, and close the dialog."""
        out = {
            "character_name": self._name.text().strip(),
            "class":          self._class.currentText() if self._class.currentIndex() > 0 else "",
            "level":          self._level.value(),
            "race":           self._race.currentText() if self._race.currentIndex() > 0 else "",
            "background":     self._background.currentText() if self._background.currentIndex() > 0 else "",
            "alignment":      self._alignment.currentText() if self._alignment.currentIndex() > 0 else "",
            "xp":             int(self._xp.text()) if self._xp.text().strip() else 0,
            "player_name":    self._player.text().strip(),
        }
        self.info_saved.emit(out)
        self.accept()

    def _load(self, data: dict):
        """Populate all input widgets from the supplied existing character-info dict."""
        if v := data.get("character_name"):
            self._name.setText(v)

        if v := data.get("class"):
            idx = self._class.findText(v)
            if idx >= 0:
                self._class.setCurrentIndex(idx)

        if v := data.get("level"):
            self._level.setValue(v)

        if v := data.get("race"):
            idx = self._race.findText(v)
            if idx >= 0:
                self._race.setCurrentIndex(idx)

        if v := data.get("background"):
            idx = self._background.findText(v)
            if idx >= 0:
                self._background.setCurrentIndex(idx)

        if v := data.get("alignment"):
            idx = self._alignment.findText(v)
            if idx >= 0:
                self._alignment.setCurrentIndex(idx)

        if (v := data.get("xp")) is not None:
            self._xp.setText(str(v))

        if v := data.get("player_name"):
            self._player.setText(v)
