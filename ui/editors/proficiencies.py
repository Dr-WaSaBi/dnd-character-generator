# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/editors/proficiencies.py                               ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Editor dialog for armor, weapon, tool proficiencies and languages. ║
# ║  Auto-applies class defaults and race languages; all are editable.  ║
# ╚══════════════════════════════════════════════════════════════════════╝

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QLineEdit, QScrollArea, QCheckBox,
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

ARMOR_PROFS = ["Light Armor", "Medium Armor", "Heavy Armor", "Shields"]

WEAPON_PROFS = [
    "Simple Weapons", "Martial Weapons",
    "Hand Crossbows", "Longswords", "Rapiers", "Shortswords",
    "Scimitars", "Daggers", "Darts", "Slings",
    "Quarterstaffs", "Light Crossbows",
]

# Class armor proficiencies
CLASS_ARMOR: dict[str, list[str]] = {
    "Barbarian":  ["Light Armor", "Medium Armor", "Shields"],
    "Bard":       ["Light Armor"],
    "Cleric":     ["Light Armor", "Medium Armor", "Shields"],
    "Druid":      ["Light Armor", "Medium Armor", "Shields"],
    "Fighter":    ["Light Armor", "Medium Armor", "Heavy Armor", "Shields"],
    "Monk":       [],
    "Paladin":    ["Light Armor", "Medium Armor", "Heavy Armor", "Shields"],
    "Ranger":     ["Light Armor", "Medium Armor", "Shields"],
    "Rogue":      ["Light Armor"],
    "Sorcerer":   [],
    "Warlock":    ["Light Armor"],
    "Wizard":     [],
    "Artificer":  ["Light Armor", "Medium Armor", "Shields"],
}

CLASS_WEAPONS: dict[str, list[str]] = {
    "Barbarian":  ["Simple Weapons", "Martial Weapons"],
    "Bard":       ["Simple Weapons", "Hand Crossbows", "Longswords", "Rapiers", "Shortswords"],
    "Cleric":     ["Simple Weapons"],
    "Druid":      ["Daggers", "Darts", "Slings", "Quarterstaffs", "Scimitars"],
    "Fighter":    ["Simple Weapons", "Martial Weapons"],
    "Monk":       ["Simple Weapons", "Shortswords"],
    "Paladin":    ["Simple Weapons", "Martial Weapons"],
    "Ranger":     ["Simple Weapons", "Martial Weapons"],
    "Rogue":      ["Simple Weapons", "Hand Crossbows", "Longswords", "Rapiers", "Shortswords"],
    "Sorcerer":   ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    "Warlock":    ["Simple Weapons"],
    "Wizard":     ["Daggers", "Darts", "Slings", "Quarterstaffs", "Light Crossbows"],
    "Artificer":  ["Simple Weapons", "Martial Weapons"],
}

# Common languages
COMMON_LANGUAGES = [
    "Common", "Dwarvish", "Elvish", "Giant", "Gnomish",
    "Goblin", "Halfling", "Orc", "Abyssal", "Celestial",
    "Draconic", "Deep Speech", "Infernal", "Primordial",
    "Sylvan", "Undercommon",
]

RACE_LANGUAGES: dict[str, list[str]] = {
    "Dragonborn": ["Common", "Draconic"],
    "Dwarf":      ["Common", "Dwarvish"],
    "Elf":        ["Common", "Elvish"],
    "Gnome":      ["Common", "Gnomish"],
    "Half-Elf":   ["Common", "Elvish"],
    "Half-Orc":   ["Common", "Orc"],
    "Halfling":   ["Common", "Halfling"],
    "Human":      ["Common"],
    "Tiefling":   ["Common", "Infernal"],
}


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


_CHECK_CSS = (
    f"QCheckBox{{color:{COLOR_TEXT_PRIMARY};font-family:{FONT_BODY};"
    f"font-size:9pt;background:transparent;spacing:6px;}}"
    f"QCheckBox::indicator{{width:14px;height:14px;"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"background:{COLOR_PARCHMENT_DARK};}}"
    f"QCheckBox::indicator:checked{{background:{COLOR_BADGE_BG};"
    f"border-color:{COLOR_GOLD_RULE};}}"
)

_TAG_CSS = (
    f"QLineEdit{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"font-family:{FONT_BODY};font-size:9pt;padding:2px 6px;}}"
    f"QLineEdit:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
)


class TagListWidget(QWidget):
    """Editable list of text tags (languages, tools, etc.)."""

    def __init__(self, items: list[str] | None = None, parent=None):
        """Build the tag list, optionally pre-populated with the given string items."""
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        self._tags: list[QLineEdit] = []
        self._lo = QVBoxLayout(self)
        self._lo.setContentsMargins(0, 0, 0, 0)
        self._lo.setSpacing(4)
        self._lo.addStretch()
        for item in (items or []):
            self._add_tag(item)

    def _add_tag(self, text: str = ""):
        """Append a new editable tag field and its remove button before the trailing stretch."""
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(4)

        field = QLineEdit(text)
        field.setPlaceholderText("Enter name…")
        field.setFixedHeight(26)
        field.setStyleSheet(_TAG_CSS)
        self._tags.append(field)

        rm = QPushButton("✕")
        rm.setFixedSize(22, 22)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;font-size:8pt;}}"
            f"QPushButton:hover{{color:{COLOR_BADGE_BG};border-color:{COLOR_BADGE_BG};}}"
        )

        container = QWidget()
        container.setStyleSheet("background:transparent;")
        container.setLayout(row)
        row.addWidget(field, 1)
        row.addWidget(rm)

        rm.clicked.connect(lambda: self._remove(field, container))
        self._lo.insertWidget(self._lo.count() - 1, container)

    def _remove(self, field: QLineEdit, container: QWidget):
        """Remove the tag field and its container widget from the layout."""
        self._tags.remove(field)
        self._lo.removeWidget(container)
        container.deleteLater()

    def add_entry(self):
        """Append a new empty tag field (called by the external Add button)."""
        self._add_tag()

    def values(self) -> list[str]:
        """Return a list of non-empty stripped strings from all tag fields."""
        return [f.text().strip() for f in self._tags if f.text().strip()]


class ProficienciesEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, char_data: dict, existing: dict | None = None, parent=None):
        """Initialize from char_data class/race defaults, apply any saved overrides, and build the UI."""
        super().__init__(parent)
        self.setWindowTitle("Section ⑩  —  Proficiencies & Languages")
        self.setMinimumSize(580, 620)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info = char_data.get("character_info", {})
        self._cls  = info.get("class", "")
        self._race = info.get("race", "")

        self._armor_checks:  dict[str, QCheckBox] = {}
        self._weapon_checks: dict[str, QCheckBox] = {}

        self._build_ui(existing or {})

    def _build_ui(self, data: dict):
        """Build the scrollable armor/weapon checkboxes, tools and language TagListWidgets, and buttons."""
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(0)

        root.addWidget(_lbl("📜  PROFICIENCIES  &  LANGUAGES", COLOR_TEXT_HEADER,
                             FONT_HEADER, 15, bold=True,
                             align=Qt.AlignmentFlag.AlignCenter))
        root.addSpacing(6)

        if self._cls:
            root.addWidget(_lbl(
                f"Auto-applied from {self._cls} — toggle to adjust",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))
        root.addSpacing(8)
        root.addWidget(_rule())
        root.addSpacing(8)

        # Scroll everything
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:none;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        inner = QWidget()
        inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        inner_lo = QVBoxLayout(inner)
        inner_lo.setContentsMargins(2, 0, 2, 0)
        inner_lo.setSpacing(14)

        # ── Armor ─────────────────────────────────────────────────────────────
        inner_lo.addWidget(_lbl("ARMOR", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))
        armor_grid = QGridLayout()
        armor_grid.setSpacing(6)
        cls_armor = set(CLASS_ARMOR.get(self._cls, []))
        saved_armor = set(data.get("armor", cls_armor if self._cls else set()))
        for i, prof in enumerate(ARMOR_PROFS):
            cb = QCheckBox(prof)
            cb.setChecked(prof in saved_armor)
            cb.setStyleSheet(_CHECK_CSS)
            self._armor_checks[prof] = cb
            armor_grid.addWidget(cb, i // 2, i % 2)
        inner_lo.addLayout(armor_grid)

        inner_lo.addWidget(_rule())

        # ── Weapons ───────────────────────────────────────────────────────────
        inner_lo.addWidget(_lbl("WEAPONS", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))
        weapon_grid = QGridLayout()
        weapon_grid.setSpacing(6)
        cls_weapons = set(CLASS_WEAPONS.get(self._cls, []))
        saved_weapons = set(data.get("weapons", cls_weapons if self._cls else set()))
        for i, prof in enumerate(WEAPON_PROFS):
            cb = QCheckBox(prof)
            cb.setChecked(prof in saved_weapons)
            cb.setStyleSheet(_CHECK_CSS)
            self._weapon_checks[prof] = cb
            weapon_grid.addWidget(cb, i // 2, i % 2)
        inner_lo.addLayout(weapon_grid)

        inner_lo.addWidget(_rule())

        # ── Tools ─────────────────────────────────────────────────────────────
        tools_hdr = QHBoxLayout()
        tools_hdr.addWidget(_lbl("TOOLS", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))
        tools_hdr.addStretch()
        tools_add = self._small_add_btn()
        tools_hdr.addWidget(tools_add)
        inner_lo.addLayout(tools_hdr)

        self._tools_list = TagListWidget(data.get("tools", []))
        self._tools_list.setMinimumHeight(40)
        tools_add.clicked.connect(self._tools_list.add_entry)
        inner_lo.addWidget(self._tools_list)

        inner_lo.addWidget(_rule())

        # ── Languages ─────────────────────────────────────────────────────────
        lang_hdr = QHBoxLayout()
        lang_hdr.addWidget(_lbl("LANGUAGES", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))
        lang_hdr.addStretch()
        lang_add = self._small_add_btn()
        lang_hdr.addWidget(lang_add)
        inner_lo.addLayout(lang_hdr)

        # Auto-populate race languages if no saved data
        default_langs = RACE_LANGUAGES.get(self._race, ["Common"])
        saved_langs = data.get("languages", default_langs if self._race else [])
        self._lang_list = TagListWidget(saved_langs)
        self._lang_list.setMinimumHeight(40)
        lang_add.clicked.connect(self._lang_list.add_entry)
        inner_lo.addWidget(self._lang_list)

        inner_lo.addStretch()
        scroll.setWidget(inner)
        root.addWidget(scroll, 1)

        root.addSpacing(8)
        root.addWidget(_rule())
        root.addSpacing(6)

        btn_row = QHBoxLayout()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        btn_row.addStretch()
        save = self._mk_btn("Save & Close", secondary=False)
        save.clicked.connect(self._on_save)
        btn_row.addWidget(save)
        root.addLayout(btn_row)

    def _small_add_btn(self) -> QPushButton:
        """Create a compact styled add-entry button for the tools and languages sections."""
        btn = QPushButton("＋ Add")
        btn.setFixedHeight(24)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:4px;"
            f"font-family:{FONT_BODY};font-size:8pt;padding:0 8px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        return btn

    def _on_save(self):
        """Collect checked armor/weapons and tag-list values into a dict, emit data_saved, and close."""
        out = {
            "armor":     [p for p, cb in self._armor_checks.items()  if cb.isChecked()],
            "weapons":   [p for p, cb in self._weapon_checks.items() if cb.isChecked()],
            "tools":     self._tools_list.values(),
            "languages": self._lang_list.values(),
        }
        self.data_saved.emit(out)
        self.accept()

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
