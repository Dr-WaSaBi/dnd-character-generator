import random
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QButtonGroup,
    QWidget, QSizePolicy,
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
    "STR": "Strength", "DEX": "Dexterity", "CON": "Constitution",
    "INT": "Intelligence", "WIS": "Wisdom", "CHA": "Charisma",
}
STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]
PB_COSTS = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
PB_BUDGET = 27
PB_MIN, PB_MAX = 8, 15


def _roll() -> int:
    dice = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(dice)[1:])


def _mod(score: int) -> str:
    m = (score - 10) // 2
    return f"+{m}" if m >= 0 else str(m)


def _lbl(text, color, family, size, bold=False, italic=False,
         align=Qt.AlignmentFlag.AlignLeft, wrap=False) -> QLabel:
    w = QLabel(text)
    w.setAlignment(align)
    w.setWordWrap(wrap)
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


# ── Ability card ────────────────────────────────────────────────────────────

class AbilityCard(QFrame):
    card_clicked = pyqtSignal(str)
    minus_clicked = pyqtSignal(str)
    plus_clicked  = pyqtSignal(str)

    _S_EMPTY    = (f"QFrame{{background:{COLOR_PARCHMENT};"
                   f"border:2px dashed {COLOR_SECTION_BORDER};border-radius:8px;}}")
    _S_FILLED   = (f"QFrame{{background:{COLOR_PARCHMENT_DARK};"
                   f"border:2px solid {COLOR_SECTION_BORDER};border-radius:8px;}}")
    _S_SELECTED = (f"QFrame{{background:#F0E098;"
                   f"border:3px solid {COLOR_GOLD_RULE};border-radius:8px;}}")
    _S_HOVER    = (f"QFrame{{background:{COLOR_PARCHMENT_HOVER};"
                   f"border:2px solid {COLOR_SECTION_BORDER_HOVER};border-radius:8px;}}")

    def __init__(self, ability: str, parent=None):
        super().__init__(parent)
        self.ability = ability
        self._score: int | None = None
        self._selected = False
        self._mode = "roll"
        self.setFixedSize(112, 155)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._build()
        self.setStyleSheet(self._S_EMPTY)

    def _build(self):
        lo = QVBoxLayout(self)
        lo.setContentsMargins(6, 8, 6, 8)
        lo.setSpacing(2)

        self.name_lbl = _lbl(self.ability, COLOR_TEXT_HEADER, FONT_HEADER, 11,
                              bold=True, align=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(self.name_lbl)
        lo.addWidget(_rule())
        lo.addStretch()

        self.score_lbl = _lbl("—", COLOR_TEXT_PRIMARY, FONT_HEADER, 28,
                               bold=True, align=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(self.score_lbl)

        self.mod_lbl = _lbl("", COLOR_TEXT_SUBTEXT, FONT_BODY, 11,
                             italic=True, align=Qt.AlignmentFlag.AlignCenter)
        lo.addWidget(self.mod_lbl)
        lo.addStretch()

        _btn = (f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
                f"border:none;border-radius:4px;font-size:16pt;font-weight:bold;}}"
                f"QPushButton:hover{{background:#A02525;}}"
                f"QPushButton:disabled{{background:{COLOR_PARCHMENT_HOVER};"
                f"color:{COLOR_TEXT_SUBTEXT};}}")
        self.minus_btn = QPushButton("−")
        self.minus_btn.setFixedSize(34, 26)
        self.minus_btn.setStyleSheet(_btn)
        self.minus_btn.clicked.connect(lambda: self.minus_clicked.emit(self.ability))

        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedSize(34, 26)
        self.plus_btn.setStyleSheet(_btn)
        self.plus_btn.clicked.connect(lambda: self.plus_clicked.emit(self.ability))

        pb = QHBoxLayout()
        pb.setContentsMargins(0, 0, 0, 0)
        pb.setSpacing(6)
        pb.addWidget(self.minus_btn)
        pb.addWidget(self.plus_btn)
        self.pb_widget = QWidget()
        self.pb_widget.setStyleSheet("background:transparent;")
        self.pb_widget.setLayout(pb)
        self.pb_widget.hide()
        lo.addWidget(self.pb_widget)

    # public API
    def set_score(self, score: int | None):
        self._score = score
        if score is not None:
            self.score_lbl.setText(str(score))
            self.mod_lbl.setText(_mod(score))
        else:
            self.score_lbl.setText("—")
            self.mod_lbl.setText("")
        self._refresh()

    def score(self) -> int | None:
        return self._score

    def set_selected(self, v: bool):
        self._selected = v
        self._refresh()

    def set_mode(self, mode: str):
        self._mode = mode
        if mode == "pointbuy":
            self.pb_widget.show()
            if self._score is None:
                self.set_score(PB_MIN)
        else:
            self.pb_widget.hide()
            if mode in ("roll", "array"):
                self.set_score(None)
        self._refresh()

    def _refresh(self):
        if self._selected:
            self.setStyleSheet(self._S_SELECTED)
        elif self._score is not None:
            self.setStyleSheet(self._S_FILLED)
        else:
            self.setStyleSheet(self._S_EMPTY)

    def enterEvent(self, e):
        if not self._selected and self._mode != "pointbuy":
            self.setStyleSheet(self._S_HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        if not self._selected:
            self._refresh()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self._mode != "pointbuy":
            self.card_clicked.emit(self.ability)
        super().mousePressEvent(e)


# ── Roll / array chip ────────────────────────────────────────────────────────

class Chip(QPushButton):
    def __init__(self, value: int, parent=None):
        super().__init__(str(value), parent)
        self.value = value
        self.setFixedSize(56, 50)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._selected = False
        self._refresh()

    def set_selected(self, v: bool):
        self._selected = v
        self._refresh()

    def set_used(self, v: bool):
        self._selected = False
        self.setEnabled(not v)
        self._refresh()

    def _refresh(self):
        if not self.isEnabled():
            s = (f"QPushButton{{background:#B8A888;color:{COLOR_TEXT_SUBTEXT};"
                 f"border:2px solid #A09070;border-radius:6px;"
                 f"font-family:{FONT_HEADER};font-size:14pt;font-weight:bold;}}")
        elif self._selected:
            s = (f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
                 f"border:3px solid {COLOR_GOLD_RULE};border-radius:6px;"
                 f"font-family:{FONT_HEADER};font-size:14pt;font-weight:bold;}}")
        else:
            s = (f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_PRIMARY};"
                 f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
                 f"font-family:{FONT_HEADER};font-size:14pt;font-weight:bold;}}"
                 f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};"
                 f"border-color:{COLOR_SECTION_BORDER_HOVER};}}")
        self.setStyleSheet(s)


# ── Editor dialog ─────────────────────────────────────────────────────────────

class AbilityScoreEditor(QDialog):
    scores_saved = pyqtSignal(dict)   # {"STR": 15, "DEX": 14, ...}

    def __init__(self, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ②  —  Ability Scores")
        self.setMinimumSize(780, 560)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        # state
        self._mode = "roll"
        self._cards: dict[str, AbilityCard] = {}
        self._roll_chips: list[Chip] = []
        self._arr_chips:  list[Chip] = []     # built once, never deleted
        self._sel_chip: Chip | None = None
        self._sel_card: str | None = None
        self._assignments: dict[str, Chip | None] = {ab: None for ab in ABILITIES}

        self._build_ui()
        self._switch_mode("roll")
        if existing:
            self._load(existing)

    # ── UI construction ──────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(26, 20, 26, 20)
        root.setSpacing(12)

        # Title
        root.addWidget(_lbl("⚂  ABILITY  SCORES", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        # Method selector
        root.addWidget(self._build_method_row())
        root.addWidget(_rule())

        # Cards
        root.addWidget(self._build_cards_row())

        # Mode-specific panels
        self._roll_panel  = self._build_roll_panel()
        self._arr_panel   = self._build_array_panel()
        self._pb_panel    = self._build_pb_panel()
        for w in (self._roll_panel, self._arr_panel, self._pb_panel):
            root.addWidget(w)

        # Hint
        self._hint = _lbl("", COLOR_TEXT_SUBTEXT, FONT_BODY, 9,
                           italic=True, align=Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._hint)

        root.addStretch()
        root.addWidget(_rule())

        # Buttons
        row = QHBoxLayout()
        self._clear_btn = self._mk_btn("Clear All", secondary=True)
        self._clear_btn.clicked.connect(self._on_clear)
        row.addWidget(self._clear_btn)
        row.addStretch()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        row.addWidget(cancel)
        save = self._mk_btn("Save & Close", secondary=False)
        save.clicked.connect(self._on_save)
        row.addWidget(save)
        root.addLayout(row)

    def _build_method_row(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        row = QHBoxLayout(w)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(0)

        self._method_grp = QButtonGroup(self)
        specs = [
            ("roll",     "🎲  Roll 4d6 (drop lowest)"),
            ("array",    "📋  Standard Array"),
            ("pointbuy", "🧮  Point Buy  (27 pts)"),
        ]
        for i, (mode, label) in enumerate(specs):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedHeight(36)
            btn.setProperty("mode_id", mode)
            r = ("border-radius:5px 0 0 5px;" if i == 0
                 else "border-radius:0 5px 5px 0;" if i == len(specs)-1
                 else "border-radius:0;")
            btn.setStyleSheet(
                f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
                f"border:2px solid {COLOR_SECTION_BORDER};border-right:1px solid {COLOR_SECTION_BORDER};"
                f"font-family:{FONT_BODY};font-size:10pt;{r}padding:0 14px;}}"
                f"QPushButton:checked{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
                f"border:2px solid {COLOR_SECTION_BORDER};}}"
                f"QPushButton:hover:!checked{{background:{COLOR_PARCHMENT_HOVER};}}"
            )
            self._method_grp.addButton(btn, i)
            row.addWidget(btn)

        row.addStretch()
        self._method_grp.idClicked.connect(lambda i: self._switch_mode(
            self._method_grp.button(i).property("mode_id")))
        self._method_grp.button(0).setChecked(True)
        return w

    def _build_cards_row(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        row = QHBoxLayout(w)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)
        row.addStretch()
        for ab in ABILITIES:
            card = AbilityCard(ab)
            card.card_clicked.connect(self._on_card_clicked)
            card.minus_clicked.connect(lambda a: self._pb_adjust(a, -1))
            card.plus_clicked.connect(lambda a: self._pb_adjust(a, +1))
            self._cards[ab] = card
            row.addWidget(card)
        row.addStretch()
        return w

    def _build_roll_panel(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(8)

        top = QHBoxLayout()
        self._roll_btn = self._mk_btn("🎲  Roll Dice", secondary=False)
        self._roll_btn.clicked.connect(self._on_roll)
        self._reroll_btn = self._mk_btn("↺  Reroll All", secondary=True)
        self._reroll_btn.clicked.connect(self._on_roll)
        self._reroll_btn.hide()
        top.addWidget(self._roll_btn)
        top.addWidget(self._reroll_btn)
        top.addStretch()
        lo.addLayout(top)

        self._chips_container = QWidget()
        self._chips_container.setStyleSheet("background:transparent;")
        self._chips_row = QHBoxLayout(self._chips_container)
        self._chips_row.setContentsMargins(0, 0, 0, 0)
        self._chips_row.setSpacing(8)
        self._chips_row.addStretch()
        lo.addWidget(self._chips_container)
        return w

    def _build_array_panel(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        row = QHBoxLayout(w)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(8)
        row.addWidget(_lbl("Values:", COLOR_TEXT_HEADER, FONT_BODY, 10, bold=True))
        for val in STANDARD_ARRAY:
            chip = Chip(val)
            chip.clicked.connect(lambda _checked, c=chip: self._on_chip_clicked(c))
            self._arr_chips.append(chip)
            row.addWidget(chip)
        row.addStretch()
        return w

    def _build_pb_panel(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        row = QHBoxLayout(w)
        row.setContentsMargins(0, 0, 0, 0)
        self._pb_lbl = QLabel()
        self._pb_lbl.setTextFormat(Qt.TextFormat.RichText)
        self._pb_lbl.setStyleSheet(
            f"color:{COLOR_TEXT_HEADER};font-family:{FONT_HEADER};"
            "font-size:13pt;font-weight:bold;background:transparent;border:none;"
        )
        row.addWidget(self._pb_lbl)
        row.addStretch()
        return w

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

    # ── Mode switching ───────────────────────────────────────────────────────

    def _switch_mode(self, mode: str):
        self._mode = mode
        self._clear_selection()

        self._roll_panel.setVisible(mode == "roll")
        self._arr_panel.setVisible(mode == "array")
        self._pb_panel.setVisible(mode == "pointbuy")

        for card in self._cards.values():
            card.set_mode(mode)

        if mode == "roll":
            self._reset_roll_chips()
            self._assignments = {ab: None for ab in ABILITIES}
            self._hint.setText(
                "Click  Roll Dice  →  select a value  →  click an ability score to assign it."
            )
        elif mode == "array":
            self._assignments = {ab: None for ab in ABILITIES}
            for chip in self._arr_chips:
                chip.set_used(False)
                chip.set_selected(False)
            self._hint.setText(
                "Click a value below  →  click an ability score to assign it."
            )
        elif mode == "pointbuy":
            self._assignments = {ab: None for ab in ABILITIES}
            self._pb_refresh_label()
            self._pb_refresh_buttons()
            self._hint.setText(
                "Use − and + to set each score (8–15).  Budget: 27 points."
            )

    # ── Rolling ──────────────────────────────────────────────────────────────

    def _on_roll(self):
        self._clear_selection()
        for ab in ABILITIES:
            self._cards[ab].set_score(None)
        self._assignments = {ab: None for ab in ABILITIES}
        self._reset_roll_chips()

        rolled = sorted([_roll() for _ in range(6)], reverse=True)
        for val in rolled:
            chip = Chip(val)
            chip.clicked.connect(lambda _checked, c=chip: self._on_chip_clicked(c))
            self._roll_chips.append(chip)
            self._chips_row.insertWidget(self._chips_row.count() - 1, chip)

        self._roll_btn.hide()
        self._reroll_btn.show()
        self._hint.setText("Select a value below  →  click an ability score to assign it.")

    def _reset_roll_chips(self):
        for chip in self._roll_chips:
            self._chips_row.removeWidget(chip)
            chip.deleteLater()
        self._roll_chips.clear()
        self._roll_btn.show()
        self._reroll_btn.hide()

    # ── Assignment ───────────────────────────────────────────────────────────

    def _on_chip_clicked(self, chip: Chip):
        if not chip.isEnabled():
            return
        if self._sel_chip is chip:
            chip.set_selected(False)
            self._sel_chip = None
            return
        if self._sel_chip:
            self._sel_chip.set_selected(False)
        self._sel_chip = chip
        chip.set_selected(True)
        # auto-assign if a card is waiting
        if self._sel_card:
            self._do_assign(self._sel_card, chip)

    def _on_card_clicked(self, ability: str):
        existing = self._assignments.get(ability)
        if existing is not None:
            # unassign — return chip to pool
            existing.set_used(False)
            self._assignments[ability] = None
            self._cards[ability].set_score(None)
            self._cards[ability].set_selected(False)
            if self._sel_card == ability:
                self._sel_card = None
            return

        if self._sel_chip:
            self._do_assign(ability, self._sel_chip)
        else:
            # select card, waiting for a chip
            if self._sel_card:
                self._cards[self._sel_card].set_selected(False)
            self._sel_card = ability
            self._cards[ability].set_selected(True)

    def _do_assign(self, ability: str, chip: Chip):
        self._assignments[ability] = chip
        self._cards[ability].set_score(chip.value)
        self._cards[ability].set_selected(False)
        chip.set_used(True)
        self._sel_chip = None
        self._sel_card = None

    def _clear_selection(self):
        if self._sel_chip:
            self._sel_chip.set_selected(False)
            self._sel_chip = None
        if self._sel_card:
            self._cards[self._sel_card].set_selected(False)
            self._sel_card = None

    # ── Point buy ────────────────────────────────────────────────────────────

    def _pb_adjust(self, ability: str, delta: int):
        if self._mode != "pointbuy":
            return
        card = self._cards[ability]
        cur = card.score() or PB_MIN
        new = cur + delta
        if not (PB_MIN <= new <= PB_MAX):
            return
        trial = {ab: (self._cards[ab].score() or PB_MIN) for ab in ABILITIES}
        trial[ability] = new
        if sum(PB_COSTS.get(v, 0) for v in trial.values()) > PB_BUDGET:
            return
        card.set_score(new)
        self._pb_refresh_label()
        self._pb_refresh_buttons()

    def _pb_refresh_label(self):
        spent = sum(PB_COSTS.get(self._cards[ab].score() or PB_MIN, 0) for ab in ABILITIES)
        rem = PB_BUDGET - spent
        color = COLOR_BADGE_BG if rem == 0 else COLOR_TEXT_HEADER
        self._pb_lbl.setText(
            f"Points remaining: "
            f"<span style='color:{color};'>{rem}</span> / {PB_BUDGET}"
        )

    def _pb_refresh_buttons(self):
        scores = {ab: (self._cards[ab].score() or PB_MIN) for ab in ABILITIES}
        spent = sum(PB_COSTS.get(v, 0) for v in scores.values())
        remaining = PB_BUDGET - spent
        for ab in ABILITIES:
            s = scores[ab]
            card = self._cards[ab]
            card.minus_btn.setEnabled(s > PB_MIN)
            next_cost = PB_COSTS.get(s + 1, 999)
            card.plus_btn.setEnabled(s < PB_MAX and next_cost <= remaining)

    # ── Clear / save ─────────────────────────────────────────────────────────

    def _on_clear(self):
        self._clear_selection()
        if self._mode == "pointbuy":
            for card in self._cards.values():
                card.set_score(PB_MIN)
            self._pb_refresh_label()
            self._pb_refresh_buttons()
        else:
            for ab in ABILITIES:
                self._cards[ab].set_score(None)
            self._assignments = {ab: None for ab in ABILITIES}
            if self._mode == "roll":
                for chip in self._roll_chips:
                    chip.set_used(False)
            elif self._mode == "array":
                for chip in self._arr_chips:
                    chip.set_used(False)

    def _on_save(self):
        out = {}
        for ab in ABILITIES:
            s = self._cards[ab].score()
            if s is not None:
                out[ab] = s
        self.scores_saved.emit(out)
        self.accept()

    def _load(self, existing: dict):
        for ab, val in existing.items():
            if ab in self._cards:
                self._cards[ab].set_score(val)
