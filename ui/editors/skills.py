from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QScrollArea,
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

# (skill name, governing ability)
SKILLS: list[tuple[str, str]] = [
    ("Acrobatics",     "DEX"),
    ("Animal Handling","WIS"),
    ("Arcana",         "INT"),
    ("Athletics",      "STR"),
    ("Deception",      "CHA"),
    ("History",        "INT"),
    ("Insight",        "WIS"),
    ("Intimidation",   "CHA"),
    ("Investigation",  "INT"),
    ("Medicine",       "WIS"),
    ("Nature",         "INT"),
    ("Perception",     "WIS"),
    ("Performance",    "CHA"),
    ("Persuasion",     "CHA"),
    ("Religion",       "INT"),
    ("Sleight of Hand","DEX"),
    ("Stealth",        "DEX"),
    ("Survival",       "WIS"),
]

# Number of class skill picks and the allowed pool
CLASS_SKILLS: dict[str, tuple[int, list[str]]] = {
    "Barbarian": (2, ["Animal Handling","Athletics","Intimidation","Nature","Perception","Survival"]),
    "Bard":      (3, [s for s, _ in SKILLS]),   # any 3
    "Cleric":    (2, ["History","Insight","Medicine","Persuasion","Religion"]),
    "Druid":     (2, ["Arcana","Animal Handling","Insight","Medicine","Nature","Perception","Religion","Survival"]),
    "Fighter":   (2, ["Acrobatics","Animal Handling","Athletics","History","Insight","Intimidation","Perception","Survival"]),
    "Monk":      (2, ["Acrobatics","Athletics","History","Insight","Religion","Stealth"]),
    "Paladin":   (2, ["Athletics","Insight","Intimidation","Medicine","Persuasion","Religion"]),
    "Ranger":    (3, ["Animal Handling","Athletics","Insight","Investigation","Nature","Perception","Stealth","Survival"]),
    "Rogue":     (4, ["Acrobatics","Athletics","Deception","Insight","Intimidation","Investigation","Perception","Performance","Persuasion","Sleight of Hand","Stealth"]),
    "Sorcerer":  (2, ["Arcana","Deception","Insight","Intimidation","Persuasion","Religion"]),
    "Warlock":   (2, ["Arcana","Deception","History","Intimidation","Investigation","Nature","Religion"]),
    "Wizard":    (2, ["Arcana","History","Insight","Investigation","Medicine","Religion"]),
    "Artificer": (2, ["Arcana","History","Investigation","Medicine","Nature","Perception","Sleight of Hand"]),
}

BACKGROUND_SKILLS: dict[str, list[str]] = {
    "Acolyte":      ["Insight", "Religion"],
    "Charlatan":    ["Deception", "Sleight of Hand"],
    "Criminal":     ["Deception", "Stealth"],
    "Entertainer":  ["Acrobatics", "Performance"],
    "Folk Hero":    ["Animal Handling", "Survival"],
    "Guild Artisan":["Insight", "Persuasion"],
    "Hermit":       ["Medicine", "Religion"],
    "Noble":        ["History", "Persuasion"],
    "Outlander":    ["Athletics", "Survival"],
    "Sage":         ["Arcana", "History"],
    "Sailor":       ["Athletics", "Perception"],
    "Soldier":      ["Athletics", "Intimidation"],
    "Urchin":       ["Sleight of Hand", "Stealth"],
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


class SkillRow(QWidget):
    toggled = pyqtSignal(str, bool)   # skill name, proficient

    _BTN_CLASS = (
        f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
        f"border:2px solid {COLOR_GOLD_RULE};border-radius:10px;"
        f"font-family:{FONT_HEADER};font-size:10pt;font-weight:bold;}}"
        f"QPushButton:hover{{background:#A02020;}}"
    )
    _BTN_BG = (
        f"QPushButton{{background:#4A6741;color:{COLOR_BADGE_TEXT};"
        f"border:2px solid #7AAA70;border-radius:10px;"
        f"font-family:{FONT_HEADER};font-size:10pt;font-weight:bold;}}"
        f"QPushButton:hover{{background:#3A5231;}}"
    )
    _BTN_OFF = (
        f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_SUBTEXT};"
        f"border:2px solid {COLOR_SECTION_BORDER};border-radius:10px;"
        f"font-family:{FONT_HEADER};font-size:10pt;}}"
        f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};"
        f"border-color:{COLOR_SECTION_BORDER_HOVER};}}"
    )

    def __init__(self, skill: str, ability: str, score: int | None,
                 prof: bool, from_bg: bool, in_class_pool: bool,
                 prof_bonus: int, parent=None):
        super().__init__(parent)
        self.skill = skill
        self._ability = ability
        self._score = score
        self._prof = prof
        self._from_bg = from_bg       # background-granted (shown in green)
        self._in_class_pool = in_class_pool
        self._prof_bonus = prof_bonus
        self.setStyleSheet("background:transparent;")
        self._build()

    def _build(self):
        row = QHBoxLayout(self)
        row.setContentsMargins(6, 3, 6, 3)
        row.setSpacing(10)

        self._toggle = QPushButton("★" if self._prof else "☆")
        self._toggle.setFixedSize(20, 20)
        self._toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle.setStyleSheet(self._btn_style())
        self._toggle.clicked.connect(self._on_toggle)
        row.addWidget(self._toggle)

        name_lbl = _lbl(self.skill, COLOR_TEXT_PRIMARY, FONT_BODY, 10)
        name_lbl.setFixedWidth(130)
        row.addWidget(name_lbl)

        ab_lbl = _lbl(f"({self._ability})", COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True)
        ab_lbl.setFixedWidth(36)
        row.addWidget(ab_lbl)

        score_txt = str(self._score) if self._score is not None else "—"
        self._score_lbl = _lbl(score_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 8,
                                align=Qt.AlignmentFlag.AlignCenter)
        self._score_lbl.setFixedWidth(22)
        row.addWidget(self._score_lbl)

        row.addWidget(_lbl("→", COLOR_TEXT_SUBTEXT, FONT_BODY, 8,
                            align=Qt.AlignmentFlag.AlignCenter))

        self._bonus_lbl = _lbl(self._calc_bonus(), COLOR_TEXT_HEADER,
                                FONT_HEADER, 12, bold=True,
                                align=Qt.AlignmentFlag.AlignCenter)
        self._bonus_lbl.setFixedWidth(36)
        row.addWidget(self._bonus_lbl)

        row.addStretch()

    def _btn_style(self) -> str:
        if not self._prof:
            return self._BTN_OFF
        return self._BTN_BG if self._from_bg else self._BTN_CLASS

    def _calc_bonus(self) -> str:
        if self._score is None:
            return "—"
        return _fmt(_mod(self._score) + (self._prof_bonus if self._prof else 0))

    def _on_toggle(self):
        self._prof = not self._prof
        # if manually toggled off a bg skill, it's no longer "from bg"
        if not self._prof:
            self._from_bg = False
        self._toggle.setText("★" if self._prof else "☆")
        self._toggle.setStyleSheet(self._btn_style())
        self._bonus_lbl.setText(self._calc_bonus())
        self.toggled.emit(self.skill, self._prof)

    def is_proficient(self) -> bool:
        return self._prof

    def update_score(self, score: int | None):
        self._score = score
        self._score_lbl.setText(str(score) if score is not None else "—")
        self._bonus_lbl.setText(self._calc_bonus())


class SkillsEditor(QDialog):
    skills_saved = pyqtSignal(dict)   # {"Acrobatics": True, "Athletics": False, ...}

    def __init__(self, char_data: dict, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ④  —  Skills")
        self.setMinimumSize(460, 620)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info   = char_data.get("character_info", {})
        scores = char_data.get("ability_scores", {})
        cls    = info.get("class", "")
        bg     = info.get("background", "")
        level  = info.get("level", 1)

        self._scores     = scores
        self._prof_bonus = _prof_bonus(level)
        self._cls        = cls
        self._bg         = bg

        num_picks, cls_pool = CLASS_SKILLS.get(cls, (0, []))
        self._num_picks  = num_picks
        self._cls_pool   = set(cls_pool)
        self._bg_skills  = set(BACKGROUND_SKILLS.get(bg, []))

        self._rows: dict[str, SkillRow] = {}
        self._proficiencies: dict[str, bool] = {}

        # Build initial proficiency state
        if existing:
            self._proficiencies = dict(existing)
        else:
            # Auto-apply background first, then class picks (first n in pool)
            auto: dict[str, bool] = {s: False for s, _ in SKILLS}
            for s in self._bg_skills:
                auto[s] = True
            cls_applied = 0
            for s, _ in SKILLS:
                if cls_applied >= num_picks:
                    break
                if s in self._cls_pool and not auto[s]:
                    auto[s] = True
                    cls_applied += 1
            self._proficiencies = auto

        self._build_ui()

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 20)
        root.setSpacing(10)

        root.addWidget(_lbl("🎯  SKILLS", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        # Info strip
        info_row = QHBoxLayout()
        info_row.addWidget(_lbl(
            f"Class: {self._cls or '—'}",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True))
        info_row.addStretch()
        info_row.addWidget(_lbl(
            f"Background: {self._bg or '—'}",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True))
        info_row.addStretch()
        pb_txt = _fmt(self._prof_bonus)
        info_row.addWidget(_lbl(
            f"Prof Bonus: {pb_txt}",
            COLOR_TEXT_HEADER, FONT_HEADER, 10, bold=True))
        root.addLayout(info_row)

        # Slot counter
        self._slot_lbl = QLabel()
        self._slot_lbl.setStyleSheet(
            f"color:{COLOR_TEXT_HEADER};font-family:{FONT_HEADER};"
            "font-size:10pt;background:transparent;border:none;"
        )
        self._slot_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._update_slot_label()
        root.addWidget(self._slot_lbl)

        root.addWidget(_rule())

        # Legend
        legend = QHBoxLayout()
        legend.setSpacing(16)
        for color, label in [
            (COLOR_BADGE_BG,  "Class proficiency"),
            ("#4A6741",       "Background proficiency"),
            (COLOR_TEXT_SUBTEXT, "Not proficient"),
        ]:
            dot = QLabel("★")
            dot.setStyleSheet(
                f"color:{color};font-size:11pt;"
                "background:transparent;border:none;"
            )
            legend.addWidget(dot)
            legend.addWidget(_lbl(label, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True))
        legend.addStretch()
        root.addLayout(legend)

        root.addWidget(_rule())

        # Scrollable skill list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:none;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea > QWidget > QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        inner = QWidget()
        inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)

        for i, (skill, ability) in enumerate(SKILLS):
            from_bg = skill in self._bg_skills and self._proficiencies.get(skill, False)
            row = SkillRow(
                skill=skill,
                ability=ability,
                score=self._scores.get(ability),
                prof=self._proficiencies.get(skill, False),
                from_bg=from_bg,
                in_class_pool=skill in self._cls_pool,
                prof_bonus=self._prof_bonus,
            )
            row.toggled.connect(self._on_row_toggled)
            self._rows[skill] = row
            if i % 2 == 1:
                row.setStyleSheet(
                    f"background:{COLOR_PARCHMENT_DARK};border-radius:3px;"
                )
            inner_layout.addWidget(row)

        inner_layout.addStretch()
        scroll.setWidget(inner)
        root.addWidget(scroll, 1)

        root.addWidget(_rule())

        hint_parts = []
        if self._cls:
            hint_parts.append(f"{self._cls}: {self._num_picks} picks from {len(self._cls_pool)} options")
        if self._bg:
            hint_parts.append(f"{self._bg}: {', '.join(sorted(self._bg_skills))}")
        if hint_parts:
            root.addWidget(_lbl(
                "  ·  ".join(hint_parts),
                COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))

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

    # ── Slot counter ──────────────────────────────────────────────────────────

    def _update_slot_label(self):
        if not self._cls or self._num_picks == 0:
            self._slot_lbl.setText("") if hasattr(self, '_slot_lbl') else None
            return
        used = sum(
            1 for s, _ in SKILLS
            if self._proficiencies.get(s) and s in self._cls_pool
               and s not in self._bg_skills
        )
        remaining = self._num_picks - used
        color = COLOR_BADGE_BG if remaining == 0 else COLOR_TEXT_HEADER
        self._slot_lbl.setText(
            f"Class picks used: <span style='color:{color};font-weight:bold;'>"
            f"{used} / {self._num_picks}</span>"
        )
        self._slot_lbl.setTextFormat(Qt.TextFormat.RichText)

    # ── Events ────────────────────────────────────────────────────────────────

    def _on_row_toggled(self, skill: str, prof: bool):
        self._proficiencies[skill] = prof
        self._update_slot_label()

    # ── Save ─────────────────────────────────────────────────────────────────

    def _on_save(self):
        out = {s: self._rows[s].is_proficient() for s, _ in SKILLS}
        self.skills_saved.emit(out)
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
