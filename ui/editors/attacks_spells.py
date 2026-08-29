# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/editors/attacks_spells.py                              ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Editor dialog for attacks/cantrips and spellcasting. Shows weapon  ║
# ║  rows on one tab and spell-slot tracker on a second tab.            ║
# ╚══════════════════════════════════════════════════════════════════════╝

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QWidget, QTabWidget,
    QLineEdit, QComboBox, QSpinBox, QScrollArea,
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

# ── Data tables ───────────────────────────────────────────────────────────────

DAMAGE_TYPES = [
    "Slashing", "Piercing", "Bludgeoning",
    "Fire", "Cold", "Lightning", "Thunder",
    "Acid", "Poison", "Necrotic", "Radiant",
    "Psychic", "Force",
]

SPELL_ABILITY: dict[str, str] = {
    "Bard": "CHA", "Cleric": "WIS", "Druid": "WIS",
    "Paladin": "CHA", "Ranger": "WIS", "Sorcerer": "CHA",
    "Warlock": "CHA", "Wizard": "INT", "Artificer": "INT",
}

NON_CASTERS = {"Barbarian", "Fighter", "Monk", "Rogue"}

# Spell slots [level-1][spell_level-1] for full casters (Bard/Cleric/Druid/Sorcerer/Wizard)
_FULL_SLOTS = [
    [2,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0],
    [4,2,0,0,0,0,0,0,0],
    [4,3,0,0,0,0,0,0,0],
    [4,3,2,0,0,0,0,0,0],
    [4,3,3,0,0,0,0,0,0],
    [4,3,3,1,0,0,0,0,0],
    [4,3,3,2,0,0,0,0,0],
    [4,3,3,3,1,0,0,0,0],
    [4,3,3,3,2,0,0,0,0],
    [4,3,3,3,2,1,0,0,0],
    [4,3,3,3,2,1,0,0,0],
    [4,3,3,3,2,1,1,0,0],
    [4,3,3,3,2,1,1,0,0],
    [4,3,3,3,2,1,1,1,0],
    [4,3,3,3,2,1,1,1,0],
    [4,3,3,3,2,1,1,1,1],
    [4,3,3,3,3,1,1,1,1],
    [4,3,3,3,3,2,1,1,1],
    [4,3,3,3,3,2,2,1,1],
]

# Half casters (Paladin/Ranger) — no slots at level 1
_HALF_SLOTS = [
    [0,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0],
    [4,2,0,0,0,0,0,0,0],
    [4,2,0,0,0,0,0,0,0],
    [4,3,0,0,0,0,0,0,0],
    [4,3,0,0,0,0,0,0,0],
    [4,3,2,0,0,0,0,0,0],
    [4,3,2,0,0,0,0,0,0],
    [4,3,3,0,0,0,0,0,0],
    [4,3,3,0,0,0,0,0,0],
    [4,3,3,1,0,0,0,0,0],
    [4,3,3,1,0,0,0,0,0],
    [4,3,3,2,0,0,0,0,0],
    [4,3,3,2,0,0,0,0,0],
    [4,3,3,3,1,0,0,0,0],
    [4,3,3,3,1,0,0,0,0],
    [4,3,3,3,2,0,0,0,0],
    [4,3,3,3,2,0,0,0,0],
]

# Artificer — half caster but starts at level 1
_ARTIFICER_SLOTS = [
    [2,0,0,0,0,0,0,0,0],
    [2,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0],
    [4,2,0,0,0,0,0,0,0],
    [4,2,0,0,0,0,0,0,0],
    [4,3,0,0,0,0,0,0,0],
    [4,3,0,0,0,0,0,0,0],
    [4,3,2,0,0,0,0,0,0],
    [4,3,2,0,0,0,0,0,0],
    [4,3,3,0,0,0,0,0,0],
    [4,3,3,0,0,0,0,0,0],
    [4,3,3,1,0,0,0,0,0],
    [4,3,3,1,0,0,0,0,0],
    [4,3,3,2,0,0,0,0,0],
    [4,3,3,2,0,0,0,0,0],
    [4,3,3,3,1,0,0,0,0],
    [4,3,3,3,1,0,0,0,0],
    [4,3,3,3,2,0,0,0,0],
    [4,3,3,3,2,0,0,0,0],
]

# Warlock pact magic: [level-1] = (num_slots, slot_level)
_WARLOCK_SLOTS = [
    (1,1),(2,1),(2,2),(2,2),(2,3),(2,3),(2,4),(2,4),(2,5),(2,5),
    (3,5),(3,5),(3,5),(3,5),(3,5),(3,5),(4,5),(4,5),(4,5),(4,5),
]


def _get_slots(cls: str, level: int) -> list[int]:
    """Return a 9-element list of max spell slots per level for the given class and character level."""
    idx = max(0, min(level - 1, 19))
    if cls in {"Bard", "Cleric", "Druid", "Sorcerer", "Wizard"}:
        return list(_FULL_SLOTS[idx])
    if cls in {"Paladin", "Ranger"}:
        return list(_HALF_SLOTS[idx])
    if cls == "Artificer":
        return list(_ARTIFICER_SLOTS[idx])
    if cls == "Warlock":
        n, sl = _WARLOCK_SLOTS[idx]
        slots = [0] * 9
        slots[sl - 1] = n
        return slots
    return [0] * 9


def _prof_bonus(level: int) -> int:
    """Return the proficiency bonus for the given character level."""
    return 2 + (level - 1) // 4


def _mod(score: int) -> int:
    """Return the D&D ability modifier for the given score: (score - 10) // 2."""
    return (score - 10) // 2


def _fmt(val: int) -> str:
    """Format an integer as a signed string (e.g. 3 → '+3', -1 → '-1')."""
    return f"+{val}" if val >= 0 else str(val)


# ── Helpers ───────────────────────────────────────────────────────────────────

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


_FIELD_CSS = (
    f"QLineEdit,QComboBox{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"font-family:{FONT_BODY};font-size:9pt;padding:2px 4px;}}"
    f"QLineEdit:focus,QComboBox:focus{{border:1px solid {COLOR_SECTION_BORDER_HOVER};}}"
    f"QComboBox::drop-down{{border:none;}}"
    f"QComboBox QAbstractItemView{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"selection-background-color:{COLOR_BADGE_BG};"
    f"selection-color:{COLOR_BADGE_TEXT};"
    f"font-family:{FONT_BODY};font-size:9pt;}}"
)


# ── Attack row ────────────────────────────────────────────────────────────────

class AttackRow(QWidget):
    remove_requested = pyqtSignal(object)

    def __init__(self, data: dict | None = None, parent=None):
        """Build a single attack/cantrip row, optionally pre-filled from a data dict."""
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        self._build(data or {})

    def _build(self, d: dict):
        """Lay out name, attack bonus, damage, damage-type combo, notes, and remove button fields."""
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(6)

        self._name   = QLineEdit(d.get("name", ""))
        self._name.setPlaceholderText("Weapon / spell name")
        self._name.setFixedHeight(26)
        self._name.setStyleSheet(_FIELD_CSS)

        self._bonus  = QLineEdit(d.get("attack_bonus", ""))
        self._bonus.setPlaceholderText("+0")
        self._bonus.setFixedSize(52, 26)
        self._bonus.setStyleSheet(_FIELD_CSS)

        self._dmg    = QLineEdit(d.get("damage", ""))
        self._dmg.setPlaceholderText("1d8+3")
        self._dmg.setFixedSize(72, 26)
        self._dmg.setStyleSheet(_FIELD_CSS)

        self._dtype  = QComboBox()
        self._dtype.setFixedHeight(26)
        self._dtype.setFixedWidth(100)
        self._dtype.setStyleSheet(_FIELD_CSS)
        self._dtype.addItem("— Type —")
        self._dtype.addItems(DAMAGE_TYPES)
        if d.get("damage_type"):
            idx = self._dtype.findText(d["damage_type"])
            if idx >= 0:
                self._dtype.setCurrentIndex(idx)

        self._notes  = QLineEdit(d.get("notes", ""))
        self._notes.setPlaceholderText("Notes (optional)")
        self._notes.setFixedHeight(26)
        self._notes.setStyleSheet(_FIELD_CSS)

        rm = QPushButton("✕")
        rm.setFixedSize(24, 24)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
            f"font-size:9pt;}}"
            f"QPushButton:hover{{color:{COLOR_BADGE_BG};"
            f"border-color:{COLOR_BADGE_BG};}}"
        )
        rm.clicked.connect(lambda: self.remove_requested.emit(self))

        row.addWidget(self._name, 3)
        row.addWidget(self._bonus)
        row.addWidget(self._dmg)
        row.addWidget(self._dtype)
        row.addWidget(self._notes, 2)
        row.addWidget(rm)

    def to_dict(self) -> dict:
        """Return a dict representation of this attack row's field values."""
        dtype = self._dtype.currentText()
        return {
            "name":         self._name.text().strip(),
            "attack_bonus": self._bonus.text().strip(),
            "damage":       self._dmg.text().strip(),
            "damage_type":  dtype if dtype != "— Type —" else "",
            "notes":        self._notes.text().strip(),
        }


# ── Main dialog ───────────────────────────────────────────────────────────────

class AttacksSpellsEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, char_data: dict, existing: dict | None = None, parent=None):
        """Derive spell stats from char_data, load any existing attacks/slots, and build the tabbed UI."""
        super().__init__(parent)
        self.setWindowTitle("Section ⑥  —  Attacks & Spellcasting")
        self.setMinimumSize(640, 580)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info   = char_data.get("character_info", {})
        scores = char_data.get("ability_scores", {})
        self._cls   = info.get("class", "")
        self._level = info.get("level", 1)
        self._scores = scores

        pb = _prof_bonus(self._level)
        sp_ab = SPELL_ABILITY.get(self._cls, "")
        sp_score = scores.get(sp_ab)
        self._sp_mod = _mod(sp_score) if sp_score is not None else 0
        self._sp_atk = self._sp_mod + pb if sp_ab else None
        self._sp_dc  = 8 + self._sp_mod + pb if sp_ab else None
        self._max_slots = _get_slots(self._cls, self._level)

        self._attack_rows: list[AttackRow] = []
        self._slot_used: list[QSpinBox] = []

        self._existing = existing or {}
        self._build_ui()

    def _build_ui(self):
        """Build the title, tabbed Attacks/Spellcasting widget, and Save/Cancel buttons."""
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 18, 22, 18)
        root.setSpacing(10)

        root.addWidget(_lbl("⚔  ATTACKS  &  SPELLCASTING", COLOR_TEXT_HEADER,
                             FONT_HEADER, 15, bold=True,
                             align=Qt.AlignmentFlag.AlignCenter))

        tabs = QTabWidget()
        tabs.setStyleSheet(
            f"QTabWidget::pane{{background:{COLOR_PARCHMENT};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;}}"
            f"QTabBar::tab{{background:{COLOR_PARCHMENT_DARK};"
            f"color:{COLOR_TEXT_HEADER};"
            f"font-family:{FONT_BODY};font-size:10pt;"
            f"padding:6px 18px;border:1px solid {COLOR_SECTION_BORDER};"
            f"border-bottom:none;border-radius:4px 4px 0 0;margin-right:2px;}}"
            f"QTabBar::tab:selected{{background:{COLOR_PARCHMENT};"
            f"color:{COLOR_TEXT_HEADER};font-weight:bold;}}"
            f"QTabBar::tab:hover:!selected{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        tabs.addTab(self._build_attacks_tab(), "⚔  Attacks")
        tabs.addTab(self._build_spells_tab(),  "✨  Spellcasting")
        root.addWidget(tabs, 1)

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

    # ── Attacks tab ───────────────────────────────────────────────────────────

    def _build_attacks_tab(self) -> QWidget:
        """Build the attacks tab with column headers, a scrollable row list, and an Add button."""
        w = QWidget()
        w.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(12, 12, 12, 12)
        lo.setSpacing(8)

        # Column headers
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        for text, stretch, fixed in [
            ("Name / Weapon",  3, None),
            ("Atk Bonus", None, 52),
            ("Damage",    None, 72),
            ("Type",      None, 100),
            ("Notes",      2, None),
            ("",          None, 24),
        ]:
            lbl = _lbl(text, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True)
            if fixed:
                lbl.setFixedWidth(fixed)
            hdr.addWidget(lbl, stretch or 0)
        lo.addLayout(hdr)
        lo.addWidget(_rule())

        # Scrollable rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:none;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        self._attacks_inner = QWidget()
        self._attacks_inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        self._attacks_layout = QVBoxLayout(self._attacks_inner)
        self._attacks_layout.setContentsMargins(0, 0, 0, 0)
        self._attacks_layout.setSpacing(4)
        self._attacks_layout.addStretch()
        scroll.setWidget(self._attacks_inner)
        lo.addWidget(scroll, 1)

        # Load existing attacks
        for atk in self._existing.get("attacks", []):
            self._add_attack_row(atk)

        # Add button
        add_btn = QPushButton("＋  Add Attack / Cantrip")
        add_btn.setFixedHeight(32)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:5px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 14px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        add_btn.clicked.connect(lambda: self._add_attack_row())
        lo.addWidget(add_btn)

        # Hint for auto-calc
        pb = _prof_bonus(self._level)
        str_mod = _mod(self._scores.get("STR", 10))
        dex_mod = _mod(self._scores.get("DEX", 10))
        hint = (f"STR attacks: {_fmt(str_mod + pb)}   ·   "
                f"DEX/Finesse attacks: {_fmt(dex_mod + pb)}   ·   "
                f"Proficiency bonus: {_fmt(pb)}")
        lo.addWidget(_lbl(hint, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                           align=Qt.AlignmentFlag.AlignCenter))
        return w

    def _add_attack_row(self, data: dict | None = None):
        """Append a new AttackRow to the scrollable list, optionally pre-filled with data."""
        row = AttackRow(data)
        row.remove_requested.connect(self._remove_attack_row)
        self._attack_rows.append(row)
        # Insert before the stretch
        self._attacks_layout.insertWidget(
            self._attacks_layout.count() - 1, row)

    def _remove_attack_row(self, row: AttackRow):
        """Remove an AttackRow from the layout and internal list when its remove button is clicked."""
        self._attacks_layout.removeWidget(row)
        row.deleteLater()
        self._attack_rows.remove(row)

    # ── Spells tab ────────────────────────────────────────────────────────────

    def _build_spells_tab(self) -> QWidget:
        """Build the spellcasting tab with stat cards and a spell-slot tracker grid (or non-caster notice)."""
        w = QWidget()
        w.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(16, 12, 16, 12)
        lo.setSpacing(10)

        is_caster = self._cls not in NON_CASTERS and bool(self._cls)

        if not is_caster:
            lo.addStretch()
            lo.addWidget(_lbl(
                f"{self._cls or 'This class'} does not use spellcasting.",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 11, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))
            lo.addStretch()
            return w

        sp_ab = SPELL_ABILITY.get(self._cls, "")

        # Spellcasting summary row
        summary = QHBoxLayout()
        summary.setSpacing(20)

        def _stat_card(title: str, value: str) -> QWidget:
            card = QWidget()
            card.setStyleSheet(
                f"background:{COLOR_PARCHMENT_DARK};"
                f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
            )
            cl = QVBoxLayout(card)
            cl.setContentsMargins(10, 6, 10, 6)
            cl.setSpacing(2)
            cl.addWidget(_lbl(title, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                               align=Qt.AlignmentFlag.AlignCenter))
            cl.addWidget(_lbl(value, COLOR_TEXT_HEADER, FONT_HEADER, 18, bold=True,
                               align=Qt.AlignmentFlag.AlignCenter))
            return card

        summary.addWidget(_stat_card("Spellcasting Ability", sp_ab or "—"))
        atk_txt = _fmt(self._sp_atk) if self._sp_atk is not None else "—"
        summary.addWidget(_stat_card("Spell Attack Bonus", atk_txt))
        dc_txt  = str(self._sp_dc) if self._sp_dc is not None else "—"
        summary.addWidget(_stat_card("Spell Save DC", dc_txt))
        lo.addLayout(summary)

        score_txt = ""
        if sp_ab and sp_ab in self._scores:
            score_txt = (f"{sp_ab} {self._scores[sp_ab]}  (mod {_fmt(self._sp_mod)})  ·  "
                         f"Prof bonus {_fmt(_prof_bonus(self._level))}")
        lo.addWidget(_lbl(score_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                           align=Qt.AlignmentFlag.AlignCenter))
        lo.addWidget(_rule())

        # Spell slot tracker
        is_warlock = self._cls == "Warlock"
        lo.addWidget(_lbl(
            "SPELL SLOTS" + ("  (Pact Magic — all slots same level)" if is_warlock else ""),
            COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True,
        ))

        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(6)

        for col, hdr_txt in enumerate(["Level", "Max", "Used", "Remaining"]):
            grid.addWidget(_lbl(hdr_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 8,
                                 italic=True, align=Qt.AlignmentFlag.AlignCenter), 0, col)

        existing_used = self._existing.get("spell_slots_used", [0]*9)

        _SPIN_CSS = (
            f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};"
            f"color:{COLOR_TEXT_PRIMARY};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
            f"font-family:{FONT_BODY};font-size:10pt;"
            f"padding:1px 4px;}}"
            f"QSpinBox:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
            f"QSpinBox::up-button,QSpinBox::down-button{{width:16px;}}"
        )

        ordinals = ["1st","2nd","3rd","4th","5th","6th","7th","8th","9th"]
        self._slot_used = []
        self._slot_remaining: list[QLabel] = []

        for i, max_slots in enumerate(self._max_slots):
            row_idx = i + 1
            if max_slots == 0:
                continue

            used_val = existing_used[i] if i < len(existing_used) else 0
            used_val = min(used_val, max_slots)

            level_lbl = _lbl(ordinals[i], COLOR_TEXT_HEADER, FONT_HEADER, 10,
                              bold=True, align=Qt.AlignmentFlag.AlignCenter)
            max_lbl   = _lbl(str(max_slots), COLOR_TEXT_PRIMARY, FONT_BODY, 10,
                              align=Qt.AlignmentFlag.AlignCenter)
            rem_lbl   = _lbl(str(max_slots - used_val),
                              COLOR_TEXT_HEADER, FONT_HEADER, 10, bold=True,
                              align=Qt.AlignmentFlag.AlignCenter)

            used_spin = QSpinBox()
            used_spin.setRange(0, max_slots)
            used_spin.setValue(used_val)
            used_spin.setFixedSize(60, 26)
            used_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            used_spin.setStyleSheet(_SPIN_CSS)
            used_spin.valueChanged.connect(
                lambda v, ml=max_slots, rl=rem_lbl: rl.setText(str(ml - v))
            )

            grid.addWidget(level_lbl, row_idx, 0)
            grid.addWidget(max_lbl,   row_idx, 1)
            grid.addWidget(used_spin, row_idx, 2)
            grid.addWidget(rem_lbl,   row_idx, 3)

            self._slot_used.append(used_spin)
            self._slot_remaining.append(rem_lbl)

        grid_w = QWidget()
        grid_w.setStyleSheet("background:transparent;")
        grid_w.setLayout(grid)
        lo.addWidget(grid_w)
        lo.addStretch()
        return w

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        """Collect attacks and used spell-slot counts, emit data_saved, and close the dialog."""
        attacks = [r.to_dict() for r in self._attack_rows if r.to_dict()["name"]]

        used_list = [0] * 9
        spin_idx = 0
        for i, max_s in enumerate(self._max_slots):
            if max_s > 0 and spin_idx < len(self._slot_used):
                used_list[i] = self._slot_used[spin_idx].value()
                spin_idx += 1

        out = {
            "attacks":          attacks,
            "spell_slots_max":  self._max_slots,
            "spell_slots_used": used_list,
            "spell_atk_bonus":  self._sp_atk,
            "spell_save_dc":    self._sp_dc,
            "spell_ability":    SPELL_ABILITY.get(self._cls, ""),
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
