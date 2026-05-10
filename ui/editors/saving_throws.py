from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
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

ABILITIES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
FULL_NAMES = {
    "STR": "Strength",    "DEX": "Dexterity",     "CON": "Constitution",
    "INT": "Intelligence","WIS": "Wisdom",         "CHA": "Charisma",
}

# Each class's two saving throw proficiencies
CLASS_SAVES: dict[str, list[str]] = {
    "Barbarian":  ["STR", "CON"],
    "Bard":       ["DEX", "CHA"],
    "Cleric":     ["WIS", "CHA"],
    "Druid":      ["INT", "WIS"],
    "Fighter":    ["STR", "CON"],
    "Monk":       ["STR", "DEX"],
    "Paladin":    ["WIS", "CHA"],
    "Ranger":     ["STR", "DEX"],
    "Rogue":      ["DEX", "INT"],
    "Sorcerer":   ["CON", "CHA"],
    "Warlock":    ["WIS", "CHA"],
    "Wizard":     ["INT", "WIS"],
    "Artificer":  ["CON", "INT"],
}


def _prof_bonus(level: int) -> int:
    return 2 + (level - 1) // 4


def _mod(score: int) -> int:
    return (score - 10) // 2


def _fmt(val: int) -> str:
    return f"+{val}" if val >= 0 else str(val)


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


class SaveRow(QWidget):
    """A single saving throw row with a proficiency toggle."""

    toggled = pyqtSignal(str, bool)   # ability, is_proficient

    _BTN_ON = (
        f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
        f"border:2px solid {COLOR_GOLD_RULE};border-radius:11px;"
        f"font-family:{FONT_HEADER};font-size:11pt;font-weight:bold;}}"
        f"QPushButton:hover{{background:#A02020;}}"
    )
    _BTN_OFF = (
        f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_SUBTEXT};"
        f"border:2px solid {COLOR_SECTION_BORDER};border-radius:11px;"
        f"font-family:{FONT_HEADER};font-size:11pt;}}"
        f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};"
        f"border-color:{COLOR_SECTION_BORDER_HOVER};}}"
    )

    def __init__(self, ability: str, score: int | None, prof: bool,
                 prof_bonus: int, parent=None):
        super().__init__(parent)
        self.ability = ability
        self._score = score
        self._prof = prof
        self._prof_bonus = prof_bonus
        self.setStyleSheet("background:transparent;")
        self._build()

    def _build(self):
        row = QHBoxLayout(self)
        row.setContentsMargins(6, 4, 6, 4)
        row.setSpacing(12)

        # Prof toggle button (circle)
        self._toggle = QPushButton("★" if self._prof else "☆")
        self._toggle.setFixedSize(22, 22)
        self._toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle.setStyleSheet(self._BTN_ON if self._prof else self._BTN_OFF)
        self._toggle.clicked.connect(self._on_toggle)
        row.addWidget(self._toggle)

        # Ability abbreviation
        ab_lbl = _lbl(self.ability, COLOR_TEXT_HEADER, FONT_HEADER, 10, bold=True)
        ab_lbl.setFixedWidth(34)
        row.addWidget(ab_lbl)

        # Full name
        name_lbl = _lbl(FULL_NAMES[self.ability], COLOR_TEXT_PRIMARY, FONT_BODY, 10)
        name_lbl.setFixedWidth(110)
        row.addWidget(name_lbl)

        # Score
        score_txt = str(self._score) if self._score is not None else "—"
        self._score_lbl = _lbl(score_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 9,
                                italic=True, align=Qt.AlignmentFlag.AlignCenter)
        self._score_lbl.setFixedWidth(28)
        row.addWidget(self._score_lbl)

        # Modifier
        mod_txt = _fmt(_mod(self._score)) if self._score is not None else "—"
        self._mod_lbl = _lbl(mod_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 10,
                              align=Qt.AlignmentFlag.AlignCenter)
        self._mod_lbl.setFixedWidth(30)
        row.addWidget(self._mod_lbl)

        # Arrow
        row.addWidget(_lbl("→", COLOR_TEXT_SUBTEXT, FONT_BODY, 9,
                            align=Qt.AlignmentFlag.AlignCenter))

        # Final save bonus (large)
        self._bonus_lbl = _lbl(self._calc_bonus_str(), COLOR_TEXT_HEADER,
                                FONT_HEADER, 14, bold=True,
                                align=Qt.AlignmentFlag.AlignCenter)
        self._bonus_lbl.setFixedWidth(42)
        row.addWidget(self._bonus_lbl)

        # Prof badge label
        self._prof_note = _lbl(
            "(prof)" if self._prof else "",
            COLOR_BADGE_BG, FONT_BODY, 8, italic=True,
        )
        self._prof_note.setFixedWidth(36)
        row.addWidget(self._prof_note)

        row.addStretch()

    def _calc_bonus_str(self) -> str:
        if self._score is None:
            return "—"
        total = _mod(self._score) + (self._prof_bonus if self._prof else 0)
        return _fmt(total)

    def _on_toggle(self):
        self._prof = not self._prof
        self._toggle.setText("★" if self._prof else "☆")
        self._toggle.setStyleSheet(self._BTN_ON if self._prof else self._BTN_OFF)
        self._bonus_lbl.setText(self._calc_bonus_str())
        self._prof_note.setText("(prof)" if self._prof else "")
        self.toggled.emit(self.ability, self._prof)

    def update_score(self, score: int | None):
        self._score = score
        self._score_lbl.setText(str(score) if score is not None else "—")
        self._mod_lbl.setText(_fmt(_mod(score)) if score is not None else "—")
        self._bonus_lbl.setText(self._calc_bonus_str())

    def is_proficient(self) -> bool:
        return self._prof

    def set_proficient(self, v: bool):
        if self._prof != v:
            self._on_toggle()


class SavingThrowEditor(QDialog):
    throws_saved = pyqtSignal(dict)   # {"STR": True, "DEX": False, ...}

    def __init__(self, char_data: dict, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ③  —  Saving Throws")
        self.setMinimumSize(500, 480)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info    = char_data.get("character_info", {})
        scores  = char_data.get("ability_scores", {})
        cls     = info.get("class", "")
        level   = info.get("level", 1)

        self._scores     = scores
        self._prof_bonus = _prof_bonus(level)
        self._class_prof = set(CLASS_SAVES.get(cls, []))
        self._rows: dict[str, SaveRow] = {}

        # Determine initial proficiencies: existing save > class default > none
        if existing:
            self._proficiencies: dict[str, bool] = dict(existing)
        elif self._class_prof:
            self._proficiencies = {ab: (ab in self._class_prof) for ab in ABILITIES}
        else:
            self._proficiencies = {ab: False for ab in ABILITIES}

        self._cls = cls
        self._level = level
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 20)
        root.setSpacing(12)

        root.addWidget(_lbl("🛡  SAVING  THROWS", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        # Info strip
        info_row = QHBoxLayout()
        cls_txt  = self._cls or "No class set"
        prof_txt = _fmt(self._prof_bonus)
        info_row.addWidget(_lbl(f"Class: {cls_txt}", COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True))
        info_row.addStretch()
        info_row.addWidget(_lbl(f"Level: {self._level}", COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True))
        info_row.addStretch()
        info_row.addWidget(_lbl(f"Proficiency Bonus: {prof_txt}",
                                COLOR_TEXT_HEADER, FONT_HEADER, 10, bold=True))
        root.addLayout(info_row)
        root.addWidget(_rule())

        # Column headers
        hdr = QHBoxLayout()
        hdr.setContentsMargins(6, 0, 6, 0)
        hdr.setSpacing(12)
        for text, width in [("Prof", 22), ("", 34), ("Ability", 110),
                             ("Score", 28), ("Mod", 30), ("", 14), ("Save", 42), ("", 36)]:
            lbl = _lbl(text, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                       align=Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(width)
            hdr.addWidget(lbl)
        hdr.addStretch()
        root.addLayout(hdr)

        # Divider
        root.addWidget(_rule())

        # One row per ability
        for ab in ABILITIES:
            score = self._scores.get(ab)
            prof  = self._proficiencies.get(ab, False)
            row   = SaveRow(ab, score, prof, self._prof_bonus)
            row.toggled.connect(lambda a, v: self._proficiencies.update({a: v}))
            self._rows[ab] = row

            # Alternate row background
            if ABILITIES.index(ab) % 2 == 1:
                row.setStyleSheet(
                    f"background:{COLOR_PARCHMENT_DARK};border-radius:4px;"
                )
            root.addWidget(row)

        root.addWidget(_rule())

        # Class hint
        if self._class_prof:
            names = " & ".join(FULL_NAMES[a] for a in sorted(self._class_prof))
            root.addWidget(_lbl(
                f"{self._cls} proficiencies: {names}  (auto-applied — you can override above)",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))
        else:
            root.addWidget(_lbl(
                "Set a class in Section 1 to auto-apply proficiencies.",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))

        root.addStretch()
        root.addWidget(_rule())

        # Buttons
        btn_row = QHBoxLayout()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        btn_row.addStretch()
        save = self._mk_btn("Save & Close", secondary=False)
        save.clicked.connect(self._on_save)
        btn_row.addWidget(save)
        root.addLayout(btn_row)

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

    def _on_save(self):
        out = {ab: self._rows[ab].is_proficient() for ab in ABILITIES}
        self.throws_saved.emit(out)
        self.accept()
