from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QSpinBox, QLineEdit,
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

HIT_DICE: dict[str, int] = {
    "Barbarian": 12,
    "Fighter":   10, "Paladin":  10, "Ranger":   10,
    "Bard":       8, "Cleric":    8, "Druid":     8,
    "Monk":       8, "Rogue":     8, "Warlock":   8,
    "Artificer":  8,
    "Sorcerer":   6, "Wizard":    6,
}
# avg HP per level after 1st (half die + 1)
_AVG: dict[int, int] = {12: 7, 10: 6, 8: 5, 6: 4}

RACE_SPEED: dict[str, int] = {
    "Dwarf": 25, "Gnome": 25, "Halfling": 25,
}
DEFAULT_SPEED = 30


def _mod(score: int) -> int:
    return (score - 10) // 2


def _fmt(val: int) -> str:
    return f"+{val}" if val >= 0 else str(val)


def _calc_max_hp(cls: str, level: int, con: int | None) -> int | None:
    die = HIT_DICE.get(cls)
    if die is None:
        return None
    con_mod = _mod(con) if con is not None else 0
    avg = _AVG[die]
    return die + (level - 1) * avg + con_mod * level


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


_SPIN_CSS = (
    f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_PRIMARY};"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
    f"font-family:{FONT_HEADER};font-size:14pt;font-weight:bold;"
    f"padding:2px 4px;}}"
    f"QSpinBox:focus{{border:2px solid {COLOR_SECTION_BORDER_HOVER};"
    f"background:{COLOR_PARCHMENT_HOVER};}}"
    f"QSpinBox::up-button,QSpinBox::down-button{{width:20px;}}"
)


def _spin(lo: int, hi: int, val: int, w: int = 90) -> QSpinBox:
    s = QSpinBox()
    s.setRange(lo, hi)
    s.setValue(val)
    s.setFixedSize(w, 52)
    s.setAlignment(Qt.AlignmentFlag.AlignCenter)
    s.setStyleSheet(_SPIN_CSS)
    return s


def _stat_box(label: str, widget: QWidget, hint: str = "") -> QWidget:
    """Wrap a widget in a labelled parchment card."""
    outer = QWidget()
    outer.setStyleSheet(
        f"background:{COLOR_PARCHMENT_DARK};"
        f"border:2px solid {COLOR_SECTION_BORDER};"
        f"border-radius:6px;"
    )
    lo = QVBoxLayout(outer)
    lo.setContentsMargins(8, 6, 8, 6)
    lo.setSpacing(2)

    lbl = QLabel(label.upper())
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet(
        f"color:{COLOR_TEXT_HEADER};font-family:{FONT_BODY};"
        "font-size:8pt;font-weight:bold;"
        "background:transparent;border:none;"
    )
    lo.addWidget(lbl)

    widget.setParent(outer)
    lo.addWidget(widget, alignment=Qt.AlignmentFlag.AlignCenter)

    if hint:
        h = QLabel(hint)
        h.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h.setStyleSheet(
            f"color:{COLOR_TEXT_SUBTEXT};font-family:{FONT_BODY};"
            "font-size:7pt;font-style:italic;"
            "background:transparent;border:none;"
        )
        lo.addWidget(h)

    return outer


class DeathSaveWidget(QWidget):
    """Three toggle circles for successes or failures."""

    def __init__(self, kind: str, count: int = 0, parent=None):
        super().__init__(parent)
        self._kind = kind   # "success" or "failure"
        self._count = count
        self.setStyleSheet("background:transparent;")
        self._btns: list[QPushButton] = []
        self._build()

    def _build(self):
        lo = QHBoxLayout(self)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(6)
        for i in range(3):
            btn = QPushButton()
            btn.setFixedSize(22, 22)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setCheckable(True)
            btn.setChecked(i < self._count)
            btn.clicked.connect(self._on_clicked)
            self._btns.append(btn)
            lo.addWidget(btn)
        self._refresh()

    def _refresh(self):
        filled = self._count
        for i, btn in enumerate(self._btns):
            btn.setChecked(i < filled)
            if self._kind == "success":
                css = (
                    f"QPushButton{{background:{'#2E7D32' if i < filled else COLOR_PARCHMENT_DARK};"
                    f"border:2px solid {'#4CAF50' if i < filled else COLOR_SECTION_BORDER};"
                    f"border-radius:11px;}}"
                    f"QPushButton:hover{{border-color:#4CAF50;}}"
                )
            else:
                css = (
                    f"QPushButton{{background:{COLOR_BADGE_BG if i < filled else COLOR_PARCHMENT_DARK};"
                    f"border:2px solid {COLOR_GOLD_RULE if i < filled else COLOR_SECTION_BORDER};"
                    f"border-radius:11px;}}"
                    f"QPushButton:hover{{border-color:{COLOR_BADGE_BG};}}"
                )
            btn.setStyleSheet(css)

    def _on_clicked(self):
        filled = sum(1 for b in self._btns if b.isChecked())
        self._count = filled
        self._refresh()

    def value(self) -> int:
        return self._count

    def set_value(self, v: int):
        self._count = max(0, min(3, v))
        self._refresh()


class CombatStatsEditor(QDialog):
    stats_saved = pyqtSignal(dict)

    def __init__(self, char_data: dict, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ⑤  —  Combat Stats")
        self.setMinimumSize(580, 560)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info   = char_data.get("character_info", {})
        scores = char_data.get("ability_scores", {})
        cls    = info.get("class", "")
        race   = info.get("race", "")
        level  = info.get("level", 1)
        dex    = scores.get("DEX")
        con    = scores.get("CON")

        self._cls   = cls
        self._level = level

        die = HIT_DICE.get(cls, 8)
        calc_hp  = _calc_max_hp(cls, level, con)
        calc_ini = _mod(dex) if dex is not None else 0
        calc_spd = RACE_SPEED.get(race, DEFAULT_SPEED)
        ac_hint  = f"Base: {10 + (_mod(dex) if dex is not None else 0)} (10 + DEX mod)"

        if existing:
            d = existing
        else:
            d = {
                "ac":            10 + (_mod(dex) if dex is not None else 0),
                "initiative":    calc_ini,
                "speed":         calc_spd,
                "max_hp":        calc_hp or 0,
                "current_hp":    calc_hp or 0,
                "temp_hp":       0,
                "hit_dice_used": 0,
                "death_successes": 0,
                "death_failures":  0,
            }

        self._die     = die
        self._calc_hp = calc_hp

        self._build_ui(d, ac_hint, calc_ini, calc_spd, die, level)

    def _build_ui(self, d: dict, ac_hint: str, calc_ini: int,
                  calc_spd: int, die: int, level: int):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 22, 28, 20)
        root.setSpacing(14)

        root.addWidget(_lbl("⚔  COMBAT  STATS", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        info_txt = f"Class: {self._cls or '—'}   ·   Level: {level}   ·   Hit Die: d{die}"
        root.addWidget(_lbl(info_txt, COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
                             align=Qt.AlignmentFlag.AlignCenter))
        root.addWidget(_rule())

        # ── Row 1: AC · Initiative · Speed ───────────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(12)

        self._ac   = _spin(0, 30, d["ac"])
        self._ini  = _spin(-5, 20, d["initiative"])
        self._spd  = _spin(0, 120, d["speed"])

        row1.addWidget(_stat_box("Armor Class",  self._ac,  ac_hint))
        row1.addWidget(_stat_box("Initiative",   self._ini, f"DEX mod: {_fmt(calc_ini)}"))
        row1.addWidget(_stat_box("Speed",        self._spd, f"{calc_spd} ft (race default)"))
        root.addLayout(row1)

        root.addWidget(_rule())

        # ── Row 2: Max HP · Current HP · Temp HP ─────────────────────────────
        row2 = QHBoxLayout()
        row2.setSpacing(12)

        hp_hint = ""
        if self._calc_hp is not None:
            hp_hint = f"Calc: {self._calc_hp} (d{die}+CON×lvl)"

        self._max_hp  = _spin(0, 9999, d["max_hp"])
        self._cur_hp  = _spin(-999, 9999, d["current_hp"])
        self._tmp_hp  = _spin(0, 9999, d["temp_hp"])

        row2.addWidget(_stat_box("Max HP",      self._max_hp,  hp_hint))
        row2.addWidget(_stat_box("Current HP",  self._cur_hp,  ""))
        row2.addWidget(_stat_box("Temporary HP",self._tmp_hp,  ""))
        root.addLayout(row2)

        # Recalc HP button
        if self._calc_hp is not None:
            recalc = QPushButton(f"↺  Reset Max HP to calculated ({self._calc_hp})")
            recalc.setFixedHeight(28)
            recalc.setCursor(Qt.CursorShape.PointingHandCursor)
            recalc.setStyleSheet(
                f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
                f"border:1px solid {COLOR_SECTION_BORDER};border-radius:4px;"
                f"font-family:{FONT_BODY};font-size:8pt;padding:0 10px;}}"
                f"QPushButton:hover{{color:{COLOR_TEXT_HEADER};"
                f"border-color:{COLOR_SECTION_BORDER_HOVER};}}"
            )
            recalc.clicked.connect(self._on_recalc_hp)
            root.addWidget(recalc, alignment=Qt.AlignmentFlag.AlignRight)

        root.addWidget(_rule())

        # ── Row 3: Hit Dice · Death Saves ────────────────────────────────────
        row3 = QHBoxLayout()
        row3.setSpacing(12)

        # Hit dice card
        hd_card = QWidget()
        hd_card.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:2px solid {COLOR_SECTION_BORDER};"
            f"border-radius:6px;"
        )
        hd_lo = QVBoxLayout(hd_card)
        hd_lo.setContentsMargins(10, 8, 10, 8)
        hd_lo.setSpacing(4)
        hd_lo.addWidget(_lbl("HIT DICE", COLOR_TEXT_HEADER, FONT_BODY, 8,
                              bold=True, align=Qt.AlignmentFlag.AlignCenter))
        hd_lo.addWidget(_lbl(f"d{die}", COLOR_TEXT_HEADER, FONT_HEADER, 22,
                              bold=True, align=Qt.AlignmentFlag.AlignCenter))

        used_row = QHBoxLayout()
        used_row.addWidget(_lbl("Used:", COLOR_TEXT_SUBTEXT, FONT_BODY, 9))
        self._hd_used = QSpinBox()
        self._hd_used.setRange(0, level)
        self._hd_used.setValue(min(d["hit_dice_used"], level))
        self._hd_used.setFixedSize(60, 28)
        self._hd_used.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hd_used.setStyleSheet(
            f"QSpinBox{{background:{COLOR_PARCHMENT};color:{COLOR_TEXT_PRIMARY};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
            f"font-family:{FONT_BODY};font-size:10pt;}}"
            f"QSpinBox::up-button,QSpinBox::down-button{{width:16px;}}"
        )
        used_row.addWidget(self._hd_used)
        used_row.addWidget(_lbl(f"/ {level}", COLOR_TEXT_SUBTEXT, FONT_BODY, 9))
        hd_lo.addLayout(used_row)

        row3.addWidget(hd_card)

        # Death saves card
        ds_card = QWidget()
        ds_card.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:2px solid {COLOR_SECTION_BORDER};"
            f"border-radius:6px;"
        )
        ds_lo = QVBoxLayout(ds_card)
        ds_lo.setContentsMargins(12, 8, 12, 8)
        ds_lo.setSpacing(6)
        ds_lo.addWidget(_lbl("DEATH SAVING THROWS", COLOR_TEXT_HEADER, FONT_BODY, 8,
                              bold=True, align=Qt.AlignmentFlag.AlignCenter))

        suc_row = QHBoxLayout()
        suc_row.addWidget(_lbl("Successes", COLOR_TEXT_SUBTEXT, FONT_BODY, 9))
        suc_row.addStretch()
        self._death_suc = DeathSaveWidget("success", d["death_successes"])
        suc_row.addWidget(self._death_suc)
        ds_lo.addLayout(suc_row)

        fail_row = QHBoxLayout()
        fail_row.addWidget(_lbl("Failures", COLOR_TEXT_SUBTEXT, FONT_BODY, 9))
        fail_row.addStretch()
        self._death_fail = DeathSaveWidget("failure", d["death_failures"])
        fail_row.addWidget(self._death_fail)
        ds_lo.addLayout(fail_row)

        ds_lo.addWidget(_lbl(
            "3 successes = stable   ·   3 failures = dead",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 7, italic=True,
            align=Qt.AlignmentFlag.AlignCenter,
        ))
        row3.addWidget(ds_card, 1)

        root.addLayout(row3)
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

    def _on_recalc_hp(self):
        if self._calc_hp is not None:
            self._max_hp.setValue(self._calc_hp)
            self._cur_hp.setValue(self._calc_hp)

    def _on_save(self):
        out = {
            "ac":              self._ac.value(),
            "initiative":      self._ini.value(),
            "speed":           self._spd.value(),
            "max_hp":          self._max_hp.value(),
            "current_hp":      self._cur_hp.value(),
            "temp_hp":         self._tmp_hp.value(),
            "hit_dice_used":   self._hd_used.value(),
            "hit_die":         self._die,
            "death_successes": self._death_suc.value(),
            "death_failures":  self._death_fail.value(),
        }
        self.stats_saved.emit(out)
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
