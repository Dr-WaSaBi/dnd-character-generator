"""
SheetView — 4-column character sheet layout replacing the section card list.
Each panel is clickable (opens its editor) and refreshes when data changes.
"""
from PyQt6.QtWidgets import (
    QWidget, QFrame, QHBoxLayout, QVBoxLayout, QGridLayout,
    QLabel, QScrollArea, QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal

from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_SECTION_BORDER_HOVER,
    COLOR_BADGE_BG, COLOR_BADGE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER, COLOR_TEXT_SUBTEXT,
    COLOR_GOLD_RULE, COLOR_WINDOW_BG,
    FONT_HEADER, FONT_BODY,
)

CR   = COLOR_BADGE_BG             # dark red  "#8B1A1A"
CRH  = "#A02020"                  # hover red
CW   = "#FFFFFF"
CG   = COLOR_GOLD_RULE            # gold     "#D4AF37"
CB   = COLOR_SECTION_BORDER       # border   "#5C3A1E"
CP   = COLOR_PARCHMENT            # "#F5E6C8"
CPD  = COLOR_PARCHMENT_DARK       # "#EDD9A3"
CPH  = COLOR_PARCHMENT_HOVER      # "#D9C48A"
CT   = COLOR_TEXT_PRIMARY         # "#2C1810"
CTH  = COLOR_TEXT_HEADER          # "#5C3A1E"
CTS  = COLOR_TEXT_SUBTEXT         # "#7A5230"
CGRN = "#1a6b1a"

ABILITY_ABBRS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
SKILL_LIST = [
    ("Acrobatics",      "DEX"), ("Animal Handling", "WIS"), ("Arcana",       "INT"),
    ("Athletics",       "STR"), ("Deception",        "CHA"), ("History",      "INT"),
    ("Insight",         "WIS"), ("Intimidation",      "CHA"), ("Investigation","INT"),
    ("Medicine",        "WIS"), ("Nature",            "INT"), ("Perception",   "WIS"),
    ("Performance",     "CHA"), ("Persuasion",        "CHA"), ("Religion",     "INT"),
    ("Sleight of Hand", "DEX"), ("Stealth",           "DEX"), ("Survival",     "WIS"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _m(s: int) -> int:
    return (s - 10) // 2

def _f(v: int) -> str:
    return f"+{v}" if v >= 0 else str(v)

def _pb(lvl: int) -> int:
    return (max(1, lvl) - 1) // 4 + 2

def _lbl(text, color=CT, sz=8, bold=False, fam=FONT_BODY,
         align=Qt.AlignmentFlag.AlignLeft, wrap=False) -> QLabel:
    w = QLabel(str(text))
    w.setAlignment(align)
    w.setWordWrap(wrap)
    css = (f"color:{color};font-family:{fam};font-size:{sz}pt;"
           "background:transparent;border:none;")
    if bold:
        css += "font-weight:bold;"
    w.setStyleSheet(css)
    return w

def _hrule() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setFixedHeight(1)
    f.setStyleSheet(f"background:{CG};border:none;")
    return f

def _dot(filled: bool, color: str = CR) -> QWidget:
    d = QWidget()
    d.setFixedSize(9, 9)
    d.setStyleSheet(
        f"background:{color};border-radius:4px;border:none;" if filled
        else f"background:transparent;border-radius:4px;border:1.5px solid {CB};"
    )
    return d

def _stat_box(value: str, label: str, fixed_h=52, circle=False) -> QFrame:
    """A white stat box with value (large) and label (small, bottom)."""
    f = QFrame()
    r = "26px" if circle else "4px"
    f.setStyleSheet(f"QFrame{{background:{CW};border:2px solid {CB};border-radius:{r};}}")
    f.setFixedHeight(fixed_h)
    f.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    lo = QVBoxLayout(f)
    lo.setContentsMargins(2, 2, 2, 2)
    lo.setSpacing(0)
    lo.addWidget(_lbl(value, CT, 14, bold=True, fam=FONT_HEADER,
                      align=Qt.AlignmentFlag.AlignCenter), 1)
    lo.addWidget(_lbl(label, CTS, 6,
                      align=Qt.AlignmentFlag.AlignCenter))
    return f

def _mini_box(value: str, label: str) -> QFrame:
    f = QFrame()
    f.setStyleSheet(f"QFrame{{background:{CW};border:1px solid {CB};border-radius:3px;}}")
    f.setFixedHeight(36)
    f.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    lo = QVBoxLayout(f)
    lo.setContentsMargins(2, 2, 2, 2)
    lo.setSpacing(0)
    lo.addWidget(_lbl(value, CT, 13, bold=True, fam=FONT_HEADER,
                      align=Qt.AlignmentFlag.AlignCenter), 1)
    lo.addWidget(_lbl(label, CTS, 6,
                      align=Qt.AlignmentFlag.AlignCenter))
    return f


# ── Base clickable panel ──────────────────────────────────────────────────────

class SectionPanel(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, number: int, title: str, parent=None):
        super().__init__(parent)
        self._n = number
        self.setObjectName("sp")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._set_style(False)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self._hdr = QLabel(title.upper())
        self._hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hdr.setFixedHeight(17)
        self._set_hdr(False)
        root.addWidget(self._hdr)

        rule = QFrame()
        rule.setFixedHeight(1)
        rule.setStyleSheet(f"background:{CG};border:none;")
        root.addWidget(rule)

        self._body = QWidget()
        self._body.setStyleSheet(f"background:{CP};border:none;")
        self._blo = QVBoxLayout(self._body)
        self._blo.setContentsMargins(5, 4, 5, 5)
        self._blo.setSpacing(2)
        root.addWidget(self._body, 1)

    def _set_style(self, hover: bool):
        if hover:
            self.setStyleSheet(f"QFrame#sp{{background:{CPH};border:2px solid {CG};border-radius:5px;}}")
        else:
            self.setStyleSheet(f"QFrame#sp{{background:{CP};border:1.5px solid {CB};border-radius:5px;}}")

    def _set_hdr(self, hover: bool):
        bg = CRH if hover else CR
        self._hdr.setStyleSheet(
            f"background:{bg};color:{CW};font-family:{FONT_HEADER};font-size:7pt;"
            "font-weight:bold;border:none;border-radius:4px 4px 0 0;padding:1px;"
        )

    def _clear(self):
        while self._blo.count():
            item = self._blo.takeAt(0)
            if w := item.widget():
                w.deleteLater()

    def _add(self, w, stretch=0):
        self._blo.addWidget(w, stretch)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._n)
        super().mousePressEvent(e)

    def enterEvent(self, e):
        self._set_style(True)
        self._set_hdr(True)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._set_style(False)
        self._set_hdr(False)
        super().leaveEvent(e)

    def refresh(self, char_data: dict):
        pass


# ── SECTION 1  Character Info (full-width header, not clickable) ──────────────

class CharInfoPanel(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"QFrame{{background:{CPD};border:2px solid {CB};border-radius:5px;}}")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        lo = QVBoxLayout(self)
        lo.setContentsMargins(12, 6, 12, 6)
        lo.setSpacing(4)

        # Name row
        self._name = _lbl("—", CTH, 18, bold=True, fam=FONT_HEADER)
        lo.addWidget(self._name)
        lo.addWidget(_hrule())

        # Two info rows
        self._row1 = QWidget()
        self._row1.setStyleSheet(f"background:transparent;border:none;")
        self._r1lo = QHBoxLayout(self._row1)
        self._r1lo.setContentsMargins(0, 0, 0, 0)
        self._r1lo.setSpacing(16)
        lo.addWidget(self._row1)

        self._row2 = QWidget()
        self._row2.setStyleSheet(f"background:transparent;border:none;")
        self._r2lo = QHBoxLayout(self._row2)
        self._r2lo.setContentsMargins(0, 0, 0, 0)
        self._r2lo.setSpacing(16)
        lo.addWidget(self._row2)

        hint = _lbl("Click to edit character info →", CTS, 7, fam=FONT_BODY,
                    align=Qt.AlignmentFlag.AlignRight)
        lo.addWidget(hint)

    def _field(self, label: str, value: str) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;border:none;")
        lo = QHBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(4)
        lo.addWidget(_lbl(label + ":", CTS, 7))
        lo.addWidget(_lbl(value or "—", CT, 8, bold=True))
        return w

    def refresh(self, char_data: dict):
        info = char_data.get("character_info", {})
        name = info.get("character_name") or info.get("name") or "Unnamed Hero"
        self._name.setText(name)

        # Clear and rebuild row 1 & 2
        while self._r1lo.count():
            if w := self._r1lo.takeAt(0).widget():
                w.deleteLater()
        while self._r2lo.count():
            if w := self._r2lo.takeAt(0).widget():
                w.deleteLater()

        cls_lvl = " ".join(filter(None, [info.get("class", ""), str(info.get("level", ""))]))
        for label, val in [
            ("Class & Level", cls_lvl),
            ("Race",          info.get("race", "")),
            ("Background",    info.get("background", "")),
            ("Player",        info.get("player_name", "")),
        ]:
            self._r1lo.addWidget(self._field(label, val))
        self._r1lo.addStretch()

        for label, val in [
            ("Alignment", info.get("alignment", "")),
            ("XP",        str(info.get("xp", 0) or 0)),
        ]:
            self._r2lo.addWidget(self._field(label, val))
        self._r2lo.addStretch()

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(1)
        super().mousePressEvent(e)

    def enterEvent(self, e):
        self.setStyleSheet(f"QFrame{{background:{CPH};border:2px solid {CG};border-radius:5px;}}")
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.setStyleSheet(f"QFrame{{background:{CPD};border:2px solid {CB};border-radius:5px;}}")
        super().leaveEvent(e)


# ── SECTION 2  Ability Scores ─────────────────────────────────────────────────

class AbilityPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(2, "Ability Scores", parent)

    def refresh(self, char_data: dict):
        self._clear()
        scores = char_data.get("ability_scores", {})

        grid_w = QWidget()
        grid_w.setStyleSheet(f"background:{CP};border:none;")
        glo = QGridLayout(grid_w)
        glo.setContentsMargins(0, 0, 0, 0)
        glo.setSpacing(4)

        for i, ab in enumerate(ABILITY_ABBRS):
            score = scores.get(ab, 10)
            mod   = _m(score)

            cell = QFrame()
            cell.setStyleSheet(f"QFrame{{background:{CW};border:1px solid {CB};border-radius:4px;}}")
            cell.setMinimumSize(60, 56)
            clo = QVBoxLayout(cell)
            clo.setContentsMargins(2, 2, 2, 3)
            clo.setSpacing(0)
            clo.addWidget(_lbl(ab, CTS, 6, bold=True,
                               align=Qt.AlignmentFlag.AlignCenter))
            clo.addWidget(_lbl(str(score), CT, 16, bold=True, fam=FONT_HEADER,
                               align=Qt.AlignmentFlag.AlignCenter), 1)

            # Modifier "circle"
            circ = QLabel(_f(mod))
            circ.setAlignment(Qt.AlignmentFlag.AlignCenter)
            circ.setFixedSize(30, 18)
            circ.setStyleSheet(
                f"color:{CT};font-family:{FONT_HEADER};font-size:8pt;font-weight:bold;"
                f"background:{CPD};border:1px solid {CB};border-radius:9px;"
            )
            clo.addWidget(circ, 0, Qt.AlignmentFlag.AlignCenter)

            glo.addWidget(cell, i // 2, i % 2)

        self._add(grid_w)
        self._blo.addStretch()


# ── SECTION 3  Saving Throws ──────────────────────────────────────────────────

class SavesPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(3, "Saving Throws", parent)

    def refresh(self, char_data: dict):
        self._clear()
        throws = char_data.get("saving_throws", {})
        scores = char_data.get("ability_scores", {})
        lvl    = (char_data.get("character_info") or {}).get("level", 1) or 1
        pb     = _pb(lvl)

        # Prof bonus
        pb_row = QWidget()
        pb_row.setStyleSheet(f"background:{CPD};border-radius:3px;")
        pblo = QHBoxLayout(pb_row)
        pblo.setContentsMargins(4, 2, 4, 2)
        pblo.setSpacing(6)
        pblo.addWidget(_lbl("Prof Bonus", CTS, 7))
        pblo.addStretch()
        pblo.addWidget(_lbl(_f(pb), CT, 9, bold=True))
        self._add(pb_row)
        self._add(_hrule())

        for ab in ABILITY_ABBRS:
            prof  = throws.get(ab, False)
            val   = _m(scores.get(ab, 10)) + (pb if prof else 0)

            row = QWidget()
            row.setStyleSheet(f"background:{CP};border:none;")
            rlo = QHBoxLayout(row)
            rlo.setContentsMargins(0, 1, 0, 1)
            rlo.setSpacing(4)
            rlo.addWidget(_dot(prof))
            rlo.addWidget(_lbl(_f(val), CT, 7, bold=True))
            rlo.addWidget(_lbl(ab, CTH, 7, bold=bool(prof)))
            rlo.addStretch()
            self._add(row)

        self._add(_hrule())
        # Passive perception
        wis  = scores.get("WIS", 10)
        pp   = 10 + _m(wis)
        pp_w = QWidget()
        pp_w.setStyleSheet(f"background:{CPD};border-radius:3px;")
        pplo = QHBoxLayout(pp_w)
        pplo.setContentsMargins(4, 2, 4, 2)
        pplo.addWidget(_lbl("Passive Perception", CTS, 7))
        pplo.addStretch()
        pplo.addWidget(_lbl(str(pp), CT, 8, bold=True))
        self._add(pp_w)
        self._blo.addStretch()


# ── SECTION 4  Skills ─────────────────────────────────────────────────────────

class SkillsPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(4, "Skills", parent)

    def refresh(self, char_data: dict):
        self._clear()
        skills = char_data.get("skills", {})
        scores = char_data.get("ability_scores", {})
        lvl    = (char_data.get("character_info") or {}).get("level", 1) or 1
        pb     = _pb(lvl)

        for i, (name, ab) in enumerate(SKILL_LIST):
            prof = skills.get(name, False)
            val  = _m(scores.get(ab, 10)) + (pb if prof else 0)

            row = QWidget()
            row.setStyleSheet(f"background:{CPD if i%2==0 else CP};border:none;")
            rlo = QHBoxLayout(row)
            rlo.setContentsMargins(2, 1, 2, 1)
            rlo.setSpacing(3)
            rlo.addWidget(_dot(prof))
            rlo.addWidget(_lbl(_f(val), CT, 7, bold=True))
            rlo.addWidget(_lbl(name, CT, 7, bold=bool(prof)), 1)
            rlo.addWidget(_lbl(ab, CTS, 6,
                               align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter))
            self._add(row)

        self._blo.addStretch()


# ── SECTION 5  Combat Stats ───────────────────────────────────────────────────

class CombatPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(5, "Combat Stats", parent)

    def refresh(self, char_data: dict):
        self._clear()
        combat = char_data.get("combat_stats", {})
        info   = char_data.get("character_info", {})
        lvl    = info.get("level", 1) or 1
        cls    = info.get("class", "")

        try:
            from ui.editors.combat_stats import HIT_DICE
            die = HIT_DICE.get(cls, 8)
        except Exception:
            die = 8

        ac      = combat.get("ac", 10)
        ini     = combat.get("initiative", 0)
        speed   = combat.get("speed", 30)
        max_hp  = combat.get("max_hp", 0)
        cur_hp  = combat.get("current_hp", max_hp)
        tmp_hp  = combat.get("temp_hp", 0)
        hd_used = combat.get("hit_dice_used", 0)
        ds_succ = combat.get("death_successes", 0)
        ds_fail = combat.get("death_failures", 0)

        # ── AC | Initiative | Speed
        r1 = QWidget()
        r1.setStyleSheet(f"background:{CP};border:none;")
        r1lo = QHBoxLayout(r1)
        r1lo.setContentsMargins(0, 0, 0, 0)
        r1lo.setSpacing(4)
        r1lo.addWidget(_stat_box(str(ac),     "Armor Class",  fixed_h=52), 1)
        r1lo.addWidget(_stat_box(_f(ini),     "Initiative",   fixed_h=52, circle=True))
        r1lo.addWidget(_stat_box(f"{speed}ft","Speed",        fixed_h=52), 1)
        self._add(r1)

        # ── Max HP
        self._add(_mini_box(str(max_hp) if max_hp else "—", "Hit Point Maximum"))

        # ── Current HP + Temp HP
        r2 = QWidget()
        r2.setStyleSheet(f"background:{CP};border:none;")
        r2lo = QHBoxLayout(r2)
        r2lo.setContentsMargins(0, 0, 0, 0)
        r2lo.setSpacing(4)
        r2lo.addWidget(_mini_box(str(cur_hp) if max_hp else "—", "Current HP"), 3)
        r2lo.addWidget(_mini_box(str(tmp_hp) if tmp_hp else "—", "Temp HP"), 2)
        self._add(r2)

        # ── Hit Dice + Death Saves
        r3 = QWidget()
        r3.setStyleSheet(f"background:{CP};border:none;")
        r3lo = QHBoxLayout(r3)
        r3lo.setContentsMargins(0, 0, 0, 0)
        r3lo.setSpacing(4)

        hd_frame = QFrame()
        hd_frame.setStyleSheet(f"QFrame{{background:{CW};border:1px solid {CB};border-radius:3px;}}")
        hd_frame.setFixedHeight(42)
        hd_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        hdlo = QVBoxLayout(hd_frame)
        hdlo.setContentsMargins(4, 2, 4, 2)
        hdlo.setSpacing(0)
        hdlo.addWidget(_lbl(f"{lvl - hd_used}/{lvl}", CT, 11, bold=True, fam=FONT_HEADER,
                            align=Qt.AlignmentFlag.AlignCenter))
        hdlo.addWidget(_lbl(f"d{die}", CTS, 7,
                            align=Qt.AlignmentFlag.AlignCenter))
        hdlo.addWidget(_lbl("Hit Dice", CTS, 6,
                            align=Qt.AlignmentFlag.AlignCenter))

        ds_frame = QFrame()
        ds_frame.setStyleSheet(f"QFrame{{background:{CW};border:1px solid {CB};border-radius:3px;}}")
        ds_frame.setFixedHeight(42)
        ds_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        dslo = QVBoxLayout(ds_frame)
        dslo.setContentsMargins(4, 2, 4, 2)
        dslo.setSpacing(2)
        dslo.addWidget(_lbl("Death Saves", CTS, 6,
                            align=Qt.AlignmentFlag.AlignCenter))

        for label, count, dot_col in [("Succ", ds_succ, CGRN), ("Fail", ds_fail, CR)]:
            dr = QWidget()
            dr.setStyleSheet("background:transparent;border:none;")
            drlo = QHBoxLayout(dr)
            drlo.setContentsMargins(0, 0, 0, 0)
            drlo.setSpacing(2)
            drlo.addWidget(_lbl(label, CT, 6))
            drlo.addStretch()
            for j in range(3):
                drlo.addWidget(_dot(j < count, dot_col))
            dslo.addWidget(dr)

        r3lo.addWidget(hd_frame, 2)
        r3lo.addWidget(ds_frame, 3)
        self._add(r3)
        self._blo.addStretch()


# ── SECTION 6  Attacks & Spellcasting ────────────────────────────────────────

class AttacksPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(6, "Attacks & Spellcasting", parent)

    def refresh(self, char_data: dict):
        self._clear()
        data  = char_data.get("attacks_spells", {})
        atks  = data.get("attacks", [])
        sab   = data.get("spell_atk_bonus")
        sdc   = data.get("spell_save_dc")

        # Header row
        hdr = QWidget()
        hdr.setStyleSheet(f"background:{CPD};border:none;")
        hdrlo = QHBoxLayout(hdr)
        hdrlo.setContentsMargins(2, 1, 2, 1)
        hdrlo.setSpacing(0)
        hdrlo.addWidget(_lbl("Name",          CTS, 7, bold=True), 3)
        hdrlo.addWidget(_lbl("Atk",           CTS, 7, bold=True,
                             align=Qt.AlignmentFlag.AlignCenter), 1)
        hdrlo.addWidget(_lbl("Damage / Type", CTS, 7, bold=True), 3)
        self._add(hdr)
        self._add(_hrule())

        for i, atk in enumerate(atks[:9]):
            row = QWidget()
            row.setStyleSheet(f"background:{CPD if i%2==0 else CP};border:none;")
            rlo = QHBoxLayout(row)
            rlo.setContentsMargins(2, 1, 2, 1)
            rlo.setSpacing(0)
            name = str(atk.get("name", ""))[:18]
            ab   = str(atk.get("attack_bonus", ""))
            dmg  = f"{atk.get('damage','')}{' '+atk.get('damage_type','') if atk.get('damage_type') else ''}"
            rlo.addWidget(_lbl(name, CT, 7), 3)
            rlo.addWidget(_lbl(ab, CT, 7, bold=True,
                               align=Qt.AlignmentFlag.AlignCenter), 1)
            rlo.addWidget(_lbl(dmg[:22], CT, 7), 3)
            self._add(row)

        if not atks:
            self._add(_lbl("No attacks added.", CTS, 7))

        if sab or sdc:
            self._add(_hrule())
            parts = []
            if sab:
                parts.append(f"Spell Atk: {sab}")
            if sdc:
                parts.append(f"Save DC: {sdc}")
            self._add(_lbl("  ".join(parts), CT, 7))

        self._blo.addStretch()


# ── SECTION 7  Equipment ─────────────────────────────────────────────────────

COIN_LABELS = ["CP", "SP", "EP", "GP", "PP"]

class EquipmentPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(7, "Equipment & Currency", parent)

    def refresh(self, char_data: dict):
        self._clear()
        equip    = char_data.get("equipment", {})
        items    = equip.get("items", [])
        currency = equip.get("currency", {})

        # Currency row
        coins = QWidget()
        coins.setStyleSheet(f"background:{CP};border:none;")
        clo = QHBoxLayout(coins)
        clo.setContentsMargins(0, 0, 0, 0)
        clo.setSpacing(3)
        for label in COIN_LABELS:
            val  = currency.get(label, 0)
            coin = QFrame()
            coin.setStyleSheet(
                f"QFrame{{background:{CW};border:1px solid {CB};border-radius:3px;}}"
            )
            coin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            coin.setFixedHeight(28)
            clo2 = QVBoxLayout(coin)
            clo2.setContentsMargins(1, 1, 1, 1)
            clo2.setSpacing(0)
            clo2.addWidget(_lbl(str(val), CT, 7, bold=True,
                                align=Qt.AlignmentFlag.AlignCenter))
            clo2.addWidget(_lbl(label, CTS, 6,
                                align=Qt.AlignmentFlag.AlignCenter))
            clo.addWidget(coin)
        self._add(coins)
        self._add(_hrule())

        for i, item in enumerate(items[:16]):
            qty  = item.get("qty", item.get("quantity", 1))
            name = str(item.get("name", ""))
            eqp  = item.get("equipped", False)

            row = QWidget()
            row.setStyleSheet(f"background:{CPD if i%2==0 else CP};border:none;")
            rlo = QHBoxLayout(row)
            rlo.setContentsMargins(2, 1, 2, 1)
            rlo.setSpacing(4)

            marker = _lbl("✦" if eqp else "  ", CR if eqp else CTS, 7)
            marker.setFixedWidth(12)
            rlo.addWidget(marker)
            rlo.addWidget(_lbl(f"{qty}×", CTS, 7))
            rlo.addWidget(_lbl(name[:28], CT, 7, bold=eqp), 1)
            self._add(row)

        if not items:
            self._add(_lbl("No items.", CTS, 7))

        self._blo.addStretch()


# ── SECTION 8  Personality ────────────────────────────────────────────────────

class PersonalityPanel(SectionPanel):
    FIELDS = [
        ("personality_traits", "Personality Traits"),
        ("ideals",             "Ideals"),
        ("bonds",              "Bonds"),
        ("flaws",              "Flaws"),
    ]

    def __init__(self, parent=None):
        super().__init__(8, "Personality", parent)

    def refresh(self, char_data: dict):
        self._clear()
        pers = char_data.get("personality", {})

        for key, label in self.FIELDS:
            text = pers.get(key, "") or ""

            banner = QLabel(label.upper())
            banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
            banner.setFixedHeight(14)
            banner.setStyleSheet(
                f"background:{CR};color:{CW};font-family:{FONT_HEADER};"
                "font-size:6pt;font-weight:bold;border:none;border-radius:2px;"
            )
            self._add(banner)

            box = QFrame()
            box.setStyleSheet(f"QFrame{{background:{CW};border:1px solid {CB};border-radius:3px;}}")
            blo = QVBoxLayout(box)
            blo.setContentsMargins(4, 3, 4, 3)
            txt = _lbl(text or "—", CT, 7, wrap=True)
            txt.setMinimumHeight(36)
            blo.addWidget(txt)
            self._add(box, 1)

        self._blo.addStretch()


# ── SECTION 9  Features & Traits ─────────────────────────────────────────────

class FeaturesPanel(SectionPanel):
    def __init__(self, parent=None):
        super().__init__(9, "Features & Traits", parent)

    def refresh(self, char_data: dict):
        self._clear()
        feat_list = (char_data.get("features") or {}).get("features", [])

        for i, feat in enumerate(feat_list[:14]):
            name = feat.get("name", "")
            desc = feat.get("description", "")

            row = QWidget()
            row.setStyleSheet(f"background:{CPD if i%2==0 else CP};border:none;")
            rlo = QVBoxLayout(row)
            rlo.setContentsMargins(4, 2, 4, 2)
            rlo.setSpacing(0)
            rlo.addWidget(_lbl("▸ " + name, CTH, 8, bold=True))
            if desc:
                snippet = desc[:80] + ("…" if len(desc) > 80 else "")
                rlo.addWidget(_lbl(snippet, CT, 6, wrap=True))
            self._add(row)

        if not feat_list:
            self._add(_lbl("No features added.", CTS, 7))

        self._blo.addStretch()


# ── SECTION 10  Proficiencies & Languages ────────────────────────────────────

class ProfPanel(SectionPanel):
    CATS = [
        ("armor",     "Armor"),
        ("weapons",   "Weapons"),
        ("tools",     "Tools"),
        ("languages", "Languages"),
    ]

    def __init__(self, parent=None):
        super().__init__(10, "Proficiencies & Languages", parent)

    def refresh(self, char_data: dict):
        self._clear()
        profs = char_data.get("proficiencies", {})

        for key, label in self.CATS:
            items = profs.get(key, [])
            if not items:
                continue

            banner = QLabel(label.upper())
            banner.setFixedHeight(13)
            banner.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            banner.setStyleSheet(
                f"color:{CTH};font-family:{FONT_HEADER};font-size:7pt;"
                f"font-weight:bold;background:transparent;border:none;padding-left:2px;"
            )
            self._add(banner)
            self._add(_hrule())

            text = ", ".join(items) if isinstance(items, list) else str(items)
            lbl = _lbl(text, CT, 7, wrap=True)
            lbl.setContentsMargins(4, 0, 0, 4)
            self._add(lbl)

        if not any(profs.get(k) for k, _ in self.CATS):
            self._add(_lbl("No proficiencies set.", CTS, 7))

        self._blo.addStretch()


# ── Main SheetView ────────────────────────────────────────────────────────────

class SheetView(QWidget):
    """
    The full character sheet UI. Emits section_clicked(int) when any
    section panel is clicked. Call refresh(char_data) after any data change.
    """
    section_clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{CP};")

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(8)

        # Character info header (full width)
        self._info = CharInfoPanel()
        self._info.clicked.connect(self.section_clicked)
        root.addWidget(self._info)

        # Gold divider
        root.addWidget(_hrule())

        # 4-column body
        body = QHBoxLayout()
        body.setSpacing(8)
        root.addLayout(body, 1)

        # ── Column 1: Ability Scores + Saving Throws
        c1 = QVBoxLayout()
        c1.setSpacing(8)
        self._ability = AbilityPanel()
        self._saves   = SavesPanel()
        self._ability.clicked.connect(self.section_clicked)
        self._saves.clicked.connect(self.section_clicked)
        c1.addWidget(self._ability, 5)
        c1.addWidget(self._saves,   5)
        body.addLayout(c1, 18)

        # ── Column 2: Skills
        c2 = QVBoxLayout()
        c2.setSpacing(8)
        self._skills = SkillsPanel()
        self._skills.clicked.connect(self.section_clicked)
        c2.addWidget(self._skills, 1)
        body.addLayout(c2, 17)

        # ── Column 3: Combat + Attacks + Equipment
        c3 = QVBoxLayout()
        c3.setSpacing(8)
        self._combat  = CombatPanel()
        self._attacks = AttacksPanel()
        self._equip   = EquipmentPanel()
        self._combat.clicked.connect(self.section_clicked)
        self._attacks.clicked.connect(self.section_clicked)
        self._equip.clicked.connect(self.section_clicked)
        c3.addWidget(self._combat,  3)
        c3.addWidget(self._attacks, 3)
        c3.addWidget(self._equip,   4)
        body.addLayout(c3, 30)

        # ── Column 4: Personality + Features + Proficiencies
        c4 = QVBoxLayout()
        c4.setSpacing(8)
        self._pers     = PersonalityPanel()
        self._features = FeaturesPanel()
        self._profs    = ProfPanel()
        self._pers.clicked.connect(self.section_clicked)
        self._features.clicked.connect(self.section_clicked)
        self._profs.clicked.connect(self.section_clicked)
        c4.addWidget(self._pers,     4)
        c4.addWidget(self._features, 4)
        c4.addWidget(self._profs,    2)
        body.addLayout(c4, 25)

    def refresh(self, char_data: dict):
        for panel in (
            self._info, self._ability, self._saves, self._skills,
            self._combat, self._attacks, self._equip,
            self._pers, self._features, self._profs,
        ):
            panel.refresh(char_data)
