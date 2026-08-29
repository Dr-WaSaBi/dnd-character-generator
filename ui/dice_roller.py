# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/dice_roller.py                                         ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Sidebar dice roller panel. Handles manual NdX rolls and weapon      ║
# ║  attack rolls (d20 + attack bonus, damage dice) with a scrolling     ║
# ║  card log that highlights crits and natural 1s.                      ║
# ╚══════════════════════════════════════════════════════════════════════╝

import re
import random

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QSpinBox, QComboBox, QPushButton, QScrollArea,
    QWidget, QSizePolicy,
)
from PyQt6.QtCore import Qt

from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER,
    COLOR_TEXT_SUBTEXT, COLOR_GOLD_RULE, FONT_HEADER, FONT_BODY,
)

_CR  = "#8B1A1A"
_CRH = "#A02020"
_CW  = "#FFFFFF"
_CG  = COLOR_GOLD_RULE
_CB  = COLOR_SECTION_BORDER
_CP  = COLOR_PARCHMENT
_CPD = COLOR_PARCHMENT_DARK
_CT  = COLOR_TEXT_PRIMARY
_CTH = COLOR_TEXT_HEADER
_CTS = COLOR_TEXT_SUBTEXT
_GRN = "#1a6b1a"


def _lbl(text, color=_CT, sz=8, bold=False, fam=FONT_BODY,
         align=Qt.AlignmentFlag.AlignLeft, wrap=False) -> QLabel:
    """Create a styled QLabel with the given text, color, size, weight, and alignment."""
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
    """Return a 1px gold horizontal rule widget for visual section separation."""
    f = QFrame()
    f.setFixedHeight(1)
    f.setStyleSheet(f"background:{_CG};border:none;")
    return f


def _parse_bonus(s) -> int:
    """Parse a string like '+5' or '-2' into an integer, returning 0 on failure."""
    try:
        return int(str(s).strip().replace(" ", ""))
    except (ValueError, TypeError):
        return 0


def _parse_damage(s: str) -> tuple[int, int, int]:
    """Parse a damage expression like '2d6+3' into (num_dice, sides, modifier)."""
    s = str(s).strip().lower()
    m = re.match(r'(\d*)d(\d+)\s*([+-]\s*\d+)?', s)
    if not m:
        return (1, 6, 0)
    num   = int(m.group(1)) if m.group(1) else 1
    sides = int(m.group(2))
    mod   = int(m.group(3).replace(" ", "")) if m.group(3) else 0
    return (num, sides, mod)


class DiceRollerPanel(QFrame):
    DICE     = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]
    _MAX_LOG = 100

    def __init__(self, parent=None):
        """Set up the panel frame and build all child widgets."""
        super().__init__(parent)
        self.setObjectName("drp")
        self.setStyleSheet(
            f"QFrame#drp{{background:{_CPD};"
            f"border:1.5px solid {_CB};border-radius:5px;}}"
        )
        self.setFixedWidth(235)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self._entry_count = 0
        self._build_ui()

    # ── Construction ──────────────────────────────────────────────────────────

    def _build_ui(self):
        """Build the Quick Roll control card, log header with Clear button, and scrollable roll log."""
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Red header bar
        hdr = QLabel("DICE ROLLER")
        hdr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hdr.setFixedHeight(20)
        hdr.setStyleSheet(
            f"background:{_CR};color:{_CW};font-family:{FONT_HEADER};"
            "font-size:8pt;font-weight:bold;border:none;"
            "border-radius:4px 4px 0 0;padding:1px;"
        )
        root.addWidget(hdr)
        root.addWidget(_hrule())

        body = QWidget()
        body.setStyleSheet(f"background:{_CPD};border:none;")
        blo = QVBoxLayout(body)
        blo.setContentsMargins(8, 8, 8, 8)
        blo.setSpacing(6)
        root.addWidget(body, 1)

        # ── Quick Roll card ───────────────────────────────────────────────────
        ctrl = QFrame()
        ctrl.setObjectName("qr")
        ctrl.setStyleSheet(
            f"QFrame#qr{{background:{_CP};border:1px solid {_CB};border-radius:4px;}}"
        )
        clo = QVBoxLayout(ctrl)
        clo.setContentsMargins(7, 6, 7, 7)
        clo.setSpacing(5)

        clo.addWidget(_lbl("QUICK ROLL", _CTH, 7, bold=True, fam=FONT_HEADER,
                           align=Qt.AlignmentFlag.AlignCenter))
        clo.addWidget(_hrule())

        row1 = QWidget()
        row1.setStyleSheet("background:transparent;border:none;")
        r1lo = QHBoxLayout(row1)
        r1lo.setContentsMargins(0, 0, 0, 0)
        r1lo.setSpacing(4)

        self._count_spin = QSpinBox()
        self._count_spin.setRange(1, 20)
        self._count_spin.setValue(1)
        self._count_spin.setFixedWidth(46)
        self._count_spin.setStyleSheet(
            f"QSpinBox{{background:{_CW};color:{_CT};border:1px solid {_CB};"
            f"border-radius:3px;font-family:{FONT_BODY};font-size:9pt;padding:1px;}}"
            "QSpinBox::up-button,QSpinBox::down-button{width:14px;}"
        )

        self._die_combo = QComboBox()
        self._die_combo.addItems(self.DICE)
        self._die_combo.setCurrentText("d20")
        self._die_combo.setStyleSheet(
            f"QComboBox{{background:{_CW};color:{_CT};border:1px solid {_CB};"
            f"border-radius:3px;font-family:{FONT_BODY};font-size:9pt;padding:1px 4px;}}"
            "QComboBox::drop-down{border:none;width:16px;}"
            f"QComboBox QAbstractItemView{{background:{_CW};color:{_CT};"
            f"selection-background-color:{_CPD};}}"
        )

        r1lo.addWidget(_lbl("#", _CTS, 8))
        r1lo.addWidget(self._count_spin)
        r1lo.addWidget(self._die_combo, 1)
        clo.addWidget(row1)

        roll_btn = QPushButton("Roll Dice")
        roll_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        roll_btn.setFixedHeight(28)
        roll_btn.setStyleSheet(
            f"QPushButton{{background:{_CR};color:{_CW};border:none;border-radius:4px;"
            f"font-family:{FONT_HEADER};font-size:9pt;font-weight:bold;}}"
            f"QPushButton:hover{{background:{_CRH};}}"
            "QPushButton:pressed{background:#6B1010;}"
        )
        roll_btn.clicked.connect(self.manual_roll)
        clo.addWidget(roll_btn)
        blo.addWidget(ctrl)

        # ── Log label + clear ─────────────────────────────────────────────────
        log_hdr = QWidget()
        log_hdr.setStyleSheet("background:transparent;border:none;")
        lhlo = QHBoxLayout(log_hdr)
        lhlo.setContentsMargins(0, 0, 0, 0)
        lhlo.addWidget(_lbl("ROLL LOG", _CTH, 7, bold=True, fam=FONT_HEADER))
        lhlo.addStretch()
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedSize(42, 18)
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.setStyleSheet(
            f"QPushButton{{background:transparent;color:{_CTS};border:1px solid {_CB};"
            f"border-radius:3px;font-family:{FONT_BODY};font-size:6pt;}}"
            f"QPushButton:hover{{background:{_CPD};}}"
        )
        clear_btn.clicked.connect(self._clear_log)
        lhlo.addWidget(clear_btn)
        blo.addWidget(log_hdr)

        # ── Scroll log ────────────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            f"QScrollArea{{border:1px solid {_CB};border-radius:3px;background:{_CP};}}"
            "QScrollBar:vertical{width:8px;background:transparent;}"
            f"QScrollBar::handle:vertical{{background:{_CB};border-radius:4px;}}"
        )

        self._log_container = QWidget()
        self._log_container.setStyleSheet(f"background:{_CP};border:none;")
        self._log_lo = QVBoxLayout(self._log_container)
        self._log_lo.setContentsMargins(4, 4, 4, 4)
        self._log_lo.setSpacing(5)
        self._log_lo.addStretch()

        scroll.setWidget(self._log_container)
        blo.addWidget(scroll, 1)

    # ── Public rolling API ────────────────────────────────────────────────────

    def manual_roll(self):
        """Read the count spinner and die selector, roll the dice, and add a card to the log."""
        count = self._count_spin.value()
        die   = self._die_combo.currentText()
        sides = int(die[1:])
        rolls = [random.randint(1, sides) for _ in range(count)]
        self._add_manual_card(count, sides, rolls)

    def weapon_attack(self, name: str, atk_bonus: str, damage: str):
        """Roll d20 + attack bonus and damage dice for a weapon, then push the result card. Called by clicking a weapon row."""
        atk_mod = _parse_bonus(atk_bonus)
        d20     = random.randint(1, 20)
        nat20   = d20 == 20
        nat1    = d20 == 1
        atk_tot = d20 + atk_mod

        num, sides, mod = _parse_damage(damage)
        if nat20:
            dmg_rolls = [random.randint(1, sides) for _ in range(num * 2)]
        else:
            dmg_rolls = [random.randint(1, sides) for _ in range(max(1, num))]
        dmg_total = sum(dmg_rolls) + mod

        self._add_weapon_card(
            name=name, atk_mod=atk_mod, d20=d20, atk_tot=atk_tot,
            nat20=nat20, nat1=nat1,
            dmg_rolls=dmg_rolls, dmg_sides=sides,
            dmg_mod=mod, dmg_total=dmg_total,
        )

    # ── Card builders ─────────────────────────────────────────────────────────

    def _add_manual_card(self, count: int, sides: int, rolls: list[int]):
        """Build a roll-log card for a manual NdX roll, with crit/nat-1 highlighting."""
        self._entry_count += 1
        label = f"{count}d{sides}"
        total = sum(rolls)

        nat20 = (sides == 20 and len(rolls) == 1 and rolls[0] == 20)
        nat1  = (sides == 20 and len(rolls) == 1 and rolls[0] == 1)

        if nat20:
            bg, border = "#f0fff0", _GRN
        elif nat1:
            bg, border = "#fff0f0", _CR
        else:
            bg, border = _CW, _CB

        card = self._make_card(bg, border)
        clo  = card.layout()

        clo.addWidget(_lbl(
            f"#{self._entry_count}  {label}",
            _CTH, 8, bold=True, fam=FONT_HEADER,
        ))
        clo.addWidget(_hrule())

        # Individual dice in rows of 5
        chunks = [rolls[i:i+5] for i in range(0, len(rolls), 5)]
        for chunk in chunks:
            clo.addWidget(_lbl(
                "  ".join(f"[{r}]" for r in chunk),
                _CTS, 8, wrap=True,
            ))

        mod_note = ""
        total_lbl_text = f"Total:  {total}"
        clo.addWidget(_lbl(total_lbl_text, _CT, 13, bold=True, fam=FONT_HEADER,
                           align=Qt.AlignmentFlag.AlignRight))

        if nat20:
            clo.addWidget(_lbl("NATURAL 20!", _GRN, 8, bold=True, fam=FONT_HEADER,
                               align=Qt.AlignmentFlag.AlignCenter))
        elif nat1:
            clo.addWidget(_lbl("NATURAL 1", _CR, 8, bold=True, fam=FONT_HEADER,
                               align=Qt.AlignmentFlag.AlignCenter))

        self._push_card(card)

    def _add_weapon_card(self, *, name, atk_mod, d20, atk_tot,
                         nat20, nat1, dmg_rolls, dmg_sides,
                         dmg_mod, dmg_total):
        """Build a roll-log card showing the attack roll result and damage breakdown for a weapon."""
        self._entry_count += 1

        if nat20:
            bg, border = "#f0fff0", _GRN
            result_color = _GRN
            result_text  = "CRITICAL HIT!"
        elif nat1:
            bg, border = "#fff0f0", _CR
            result_color = _CR
            result_text  = "CRITICAL MISS"
        else:
            bg, border = _CW, _CB
            result_color = _CT
            result_text  = f"= {atk_tot}"

        card = self._make_card(bg, border)
        clo  = card.layout()

        clo.addWidget(_lbl(
            f"#{self._entry_count}  ⚔  {name}",
            _CTH, 8, bold=True, fam=FONT_HEADER,
        ))
        clo.addWidget(_hrule())

        # Attack roll
        sign = "+" if atk_mod >= 0 else ""
        clo.addWidget(_lbl("ATTACK ROLL", _CTS, 6, bold=True, fam=FONT_HEADER))
        clo.addWidget(_lbl(
            f"d20[{d20}]  {sign}{atk_mod}  {result_text}",
            result_color, 9, bold=True,
        ))

        # Damage roll
        crit_note = "  (CRIT — doubled dice)" if nat20 else ""
        clo.addWidget(_lbl(f"DAMAGE{crit_note}", _CTS, 6, bold=True, fam=FONT_HEADER))
        rolls_str = "  ".join(f"[{r}]" for r in dmg_rolls)
        mod_str   = (f" +{dmg_mod}" if dmg_mod > 0
                     else (f" {dmg_mod}" if dmg_mod < 0 else ""))
        clo.addWidget(_lbl(
            f"{rolls_str}{mod_str}  =  {dmg_total}",
            _CT, 9, bold=True,
        ))

        self._push_card(card)

    def _make_card(self, bg: str, border: str) -> QFrame:
        """Create a styled QFrame card with the given background and border color."""
        card = QFrame()
        card.setStyleSheet(
            f"QFrame{{background:{bg};border:1.5px solid {border};border-radius:4px;}}"
        )
        clo = QVBoxLayout(card)
        clo.setContentsMargins(7, 5, 7, 6)
        clo.setSpacing(3)
        return card

    def _push_card(self, card: QFrame):
        """Insert the newest card at the top of the log and trim the oldest if over _MAX_LOG."""
        self._log_lo.insertWidget(0, card)
        # Trim oldest entries (index count-2 is oldest card; count-1 is stretch)
        while self._log_lo.count() - 1 > self._MAX_LOG:
            item = self._log_lo.takeAt(self._log_lo.count() - 2)
            if w := item.widget():
                w.deleteLater()

    def _clear_log(self):
        """Remove all cards from the log and reset the entry counter."""
        while self._log_lo.count() > 1:
            item = self._log_lo.takeAt(0)
            if w := item.widget():
                w.deleteLater()
        self._entry_count = 0
