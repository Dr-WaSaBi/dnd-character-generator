import json
import os

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QSizePolicy,
    QMenuBar, QMenu, QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QAction, QKeySequence

from ui.editors import AbilityScoreEditor, CharacterInfoEditor
from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_SECTION_BORDER_HOVER,
    COLOR_BADGE_BG, COLOR_BADGE_RING, COLOR_BADGE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER, COLOR_TEXT_SUBTEXT,
    COLOR_WINDOW_BG, COLOR_GOLD_RULE,
    FONT_HEADER, FONT_BODY,
)

# Section definitions: (number, title, description, hint)
SECTIONS = [
    (1,  "Character Info",
     "Character Name  ·  Class & Level  ·  Race  ·  Background\nAlignment  ·  Experience Points  ·  Player Name",
     "Identity & origin"),

    (2,  "Ability Scores",
     "STR  ·  DEX  ·  CON  ·  INT  ·  WIS  ·  CHA\nRoll 4d6-drop-lowest, Standard Array, or Point Buy",
     "Roll or assign your 6 core stats"),

    (3,  "Saving Throws",
     "Proficiency-based saving throws\nfor each of the six ability scores.\nDetermined automatically by your class.",
     "Class-granted proficiencies"),

    (4,  "Skills",
     "Acrobatics · Animal Handling · Arcana\nAthletics · Deception · History · Insight\nIntimidation · Investigation · Medicine\nNature · Perception · Performance\nPersuasion · Religion · Sleight of Hand\nStealth · Survival",
     "Choose your trained skills"),

    (5,  "Combat Stats",
     "Armor Class  ·  Initiative  ·  Speed\nMax HP  ·  Current HP  ·  Temporary HP\nHit Dice  ·  Death Saving Throws",
     "Defense & hit points"),

    (6,  "Attacks & Spellcasting",
     "Weapon attacks with name, bonus & damage\nSpell attack bonus  ·  Spell save DC\nSpell slots by level  ·  Known spells",
     "Weapons, spells & cantrips"),

    (7,  "Equipment & Currency",
     "Carried gear, armor, and tools\n\nCopper  ·  Silver  ·  Electrum  ·  Gold  ·  Platinum",
     "Inventory & coin purse"),

    (8,  "Personality",
     "Personality Traits — what defines your character day-to-day\nIdeals — the principles you live by\nBonds — ties to the world\nFlaws — your greatest weaknesses",
     "Traits, ideals, bonds & flaws"),

    (9,  "Features & Traits",
     "Class features unlocked at each level\nRacial traits from your ancestry\nBackground feature & proficiencies",
     "Abilities granted by class & race"),

    (10, "Proficiencies & Languages",
     "Armor  ·  Weapons  ·  Tools\n\nLanguages spoken and understood\nby your character",
     "Training & communication"),
]


def _label(text, color, font_family, font_size_pt, bold=False, italic=False,
           align=Qt.AlignmentFlag.AlignLeft, word_wrap=False):
    """Build a styled QLabel with transparent background."""
    lbl = QLabel(text)
    lbl.setAlignment(align)
    lbl.setWordWrap(word_wrap)
    style = (
        f"color: {color};"
        f"font-family: {font_family};"
        f"font-size: {font_size_pt}pt;"
        f"background: transparent;"
        f"border: none;"
    )
    if bold:
        style += "font-weight: bold;"
    if italic:
        style += "font-style: italic;"
    lbl.setStyleSheet(style)
    return lbl


class ClickableSection(QFrame):
    clicked = pyqtSignal(int, str)

    _STYLE_NORMAL = (
        f"QFrame {{ background-color: {COLOR_PARCHMENT_DARK};"
        f"border: 2px solid {COLOR_SECTION_BORDER}; border-radius: 6px; }}"
    )
    _STYLE_HOVER = (
        f"QFrame {{ background-color: {COLOR_PARCHMENT_HOVER};"
        f"border: 2px solid {COLOR_SECTION_BORDER_HOVER}; border-radius: 6px; }}"
    )

    def __init__(self, number: int, title: str, description: str,
                 hint: str = "", parent=None):
        super().__init__(parent)
        self._number = number
        self._title = title
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(self._STYLE_NORMAL)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._build(number, title, description, hint)

    def _build(self, number, title, description, hint):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(6)

        # Header row: badge + section title
        header = QHBoxLayout()
        header.setSpacing(8)
        header.setContentsMargins(0, 0, 0, 0)

        badge = QLabel(str(number))
        badge.setFixedSize(30, 30)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"QLabel {{ background-color: {COLOR_BADGE_BG};"
            f"color: {COLOR_BADGE_TEXT};"
            f"border: 2px solid {COLOR_BADGE_RING};"
            f"border-radius: 15px;"
            f"font-family: {FONT_HEADER};"
            f"font-size: 11pt; font-weight: bold; }}"
        )

        title_lbl = _label(
            title.upper(), COLOR_TEXT_HEADER, FONT_HEADER,
            font_size_pt=10, bold=True,
            align=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
        )

        header.addWidget(badge)
        header.addWidget(title_lbl, 1)
        layout.addLayout(header)

        # Thin gold divider under header
        rule = QFrame()
        rule.setFrameShape(QFrame.Shape.HLine)
        rule.setFixedHeight(1)
        rule.setStyleSheet(f"background: {COLOR_GOLD_RULE}; border: none;")
        layout.addWidget(rule)

        # Description
        self._desc_lbl = _label(
            description, COLOR_TEXT_PRIMARY, FONT_BODY,
            font_size_pt=9, word_wrap=True,
        )
        layout.addWidget(self._desc_lbl, 1)

        # Bottom hint (right-aligned, italic)
        if hint:
            hint_lbl = _label(
                hint, COLOR_TEXT_SUBTEXT, FONT_BODY,
                font_size_pt=8, italic=True,
                align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom,
            )
            layout.addWidget(hint_lbl)

    def set_preview(self, text: str):
        self._desc_lbl.setText(text)

    def enterEvent(self, event):
        self.setStyleSheet(self._STYLE_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self._STYLE_NORMAL)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self._number, self._title)
        super().mousePressEvent(event)


class CharacterSheetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D 5e Character Generator")
        self.setMinimumSize(1050, 720)
        self.resize(1200, 900)
        self._char_data: dict = {}
        self._sections: dict[int, ClickableSection] = {}
        self._current_file: str | None = None
        self._build_ui()
        self._build_menu()

    def _build_ui(self):
        # Outer dark border feel
        outer = QWidget()
        outer.setStyleSheet(f"background-color: {COLOR_WINDOW_BG};")
        self.setCentralWidget(outer)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(18, 18, 18, 18)

        # Scrollable parchment sheet
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.viewport().setStyleSheet(f"background-color: {COLOR_PARCHMENT};")
        outer_layout.addWidget(scroll)

        sheet = QWidget()
        sheet.setStyleSheet(f"background-color: {COLOR_PARCHMENT};")
        scroll.setWidget(sheet)

        layout = QVBoxLayout(sheet)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        # Sheet title
        layout.addWidget(self._make_sheet_title())

        # Section 1 — full width
        s1 = self._make_section(1)
        s1.setMinimumHeight(95)
        s1.setMaximumHeight(110)
        layout.addWidget(s1)

        # Thin gold rule
        rule = QFrame()
        rule.setFrameShape(QFrame.Shape.HLine)
        rule.setFixedHeight(1)
        rule.setStyleSheet(f"background: {COLOR_GOLD_RULE}; border: none;")
        layout.addWidget(rule)

        # Three-column body
        body = QHBoxLayout()
        body.setSpacing(10)
        layout.addLayout(body, 1)

        left = QVBoxLayout()
        left.setSpacing(8)
        for num in [2, 3, 4]:
            s = self._make_section(num)
            if num == 2:
                s.setMinimumHeight(160)
            elif num == 3:
                s.setMinimumHeight(120)
            elif num == 4:
                s.setMinimumHeight(260)
            left.addWidget(s)

        center = QVBoxLayout()
        center.setSpacing(8)
        for num in [5, 6, 7]:
            s = self._make_section(num)
            if num == 5:
                s.setMinimumHeight(115)
            elif num == 6:
                s.setMinimumHeight(185)
            elif num == 7:
                s.setMinimumHeight(150)
            center.addWidget(s)

        right = QVBoxLayout()
        right.setSpacing(8)
        for num in [8, 9, 10]:
            s = self._make_section(num)
            if num == 8:
                s.setMinimumHeight(165)
            elif num == 9:
                s.setMinimumHeight(185)
            elif num == 10:
                s.setMinimumHeight(100)
            right.addWidget(s)

        body.addLayout(left, 22)
        body.addLayout(center, 30)
        body.addLayout(right, 28)

        # Status bar
        self.statusBar().setFixedHeight(26)
        self.statusBar().showMessage(
            "  Select any numbered section above to begin building your character."
        )

    # ── Menu bar ─────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            f"QMenuBar{{background:{COLOR_WINDOW_BG};color:#D4AF37;"
            f"font-family:{FONT_BODY};font-size:9pt;padding:2px;}}"
            f"QMenuBar::item:selected{{background:#3A1A0A;}}"
            f"QMenu{{background:{COLOR_WINDOW_BG};color:#D4AF37;"
            f"font-family:{FONT_BODY};font-size:9pt;border:1px solid #D4AF37;}}"
            f"QMenu::item:selected{{background:#3A1A0A;}}"
        )
        file_menu = mb.addMenu("File")

        act_new = QAction("New Character", self)
        act_new.setShortcut(QKeySequence.StandardKey.New)
        act_new.triggered.connect(self._on_new)
        file_menu.addAction(act_new)

        file_menu.addSeparator()

        act_open = QAction("Open Character…", self)
        act_open.setShortcut(QKeySequence.StandardKey.Open)
        act_open.triggered.connect(self._on_open)
        file_menu.addAction(act_open)

        file_menu.addSeparator()

        act_save = QAction("Save", self)
        act_save.setShortcut(QKeySequence.StandardKey.Save)
        act_save.triggered.connect(self._on_save)
        file_menu.addAction(act_save)

        act_save_as = QAction("Save As…", self)
        act_save_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        act_save_as.triggered.connect(self._on_save_as)
        file_menu.addAction(act_save_as)

    # ── File I/O ──────────────────────────────────────────────────────────────

    def _on_new(self):
        if self._char_data and not self._confirm_discard():
            return
        self._char_data = {}
        self._current_file = None
        self._reset_sheet()
        self.setWindowTitle("D&D 5e Character Generator")
        self.statusBar().showMessage("  New character — select a section to begin.")

    def _on_open(self):
        if self._char_data and not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Character", "",
            "D&D Character (*.dnd5e);;JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._char_data = data
            self._current_file = path
            self._apply_loaded_data()
            self.setWindowTitle(f"D&D 5e — {os.path.basename(path)}")
            self.statusBar().showMessage(f"  Opened: {os.path.basename(path)}")
        except Exception as exc:
            QMessageBox.critical(self, "Open failed", str(exc))

    def _on_save(self):
        if self._current_file:
            self._write_file(self._current_file)
        else:
            self._on_save_as()

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character", "",
            "D&D Character (*.dnd5e);;JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        if not path.endswith((".dnd5e", ".json")):
            path += ".dnd5e"
        self._current_file = path
        self._write_file(path)
        self.setWindowTitle(f"D&D 5e — {os.path.basename(path)}")

    def _write_file(self, path: str):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._char_data, f, indent=2)
            self.statusBar().showMessage(f"  ✔  Saved: {os.path.basename(path)}")
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", str(exc))

    def _confirm_discard(self) -> bool:
        reply = QMessageBox.question(
            self, "Unsaved character",
            "You have unsaved data. Discard and continue?",
            QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
        )
        return reply == QMessageBox.StandardButton.Discard

    def _reset_sheet(self):
        for num, section in self._sections.items():
            _, title, description, hint = next(s for s in SECTIONS if s[0] == num)
            section.set_preview(description)

    def _apply_loaded_data(self):
        if info := self._char_data.get("character_info"):
            self._on_info_saved(info)
        if scores := self._char_data.get("ability_scores"):
            self._on_scores_saved(scores)

    def _make_sheet_title(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        h = QHBoxLayout(container)
        h.setContentsMargins(0, 0, 0, 4)

        left = _label("D&D 5e", COLOR_TEXT_SUBTEXT, FONT_HEADER, 11, italic=True)
        h.addWidget(left)

        title = _label(
            "CHARACTER  SHEET",
            COLOR_TEXT_HEADER, FONT_HEADER, 18, bold=True,
            align=Qt.AlignmentFlag.AlignCenter,
        )
        h.addWidget(title, 1)

        right = _label(
            "Click a section to edit →",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
            align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        )
        h.addWidget(right)

        return container

    def _make_section(self, number: int) -> ClickableSection:
        _, title, description, hint = next(s for s in SECTIONS if s[0] == number)
        section = ClickableSection(number, title, description, hint)
        section.clicked.connect(self._on_section_clicked)
        self._sections[number] = section
        return section

    def _on_section_clicked(self, number: int, title: str):
        if number == 1:
            self._open_info_editor()
            return
        if number == 2:
            self._open_ability_editor()
            return
        self.statusBar().showMessage(
            f"  ▶  Section {number}: {title}   —   editor coming soon"
        )

    def _open_info_editor(self):
        dlg = CharacterInfoEditor(
            existing=self._char_data.get("character_info"),
            parent=self,
        )
        dlg.info_saved.connect(self._on_info_saved)
        dlg.exec()

    def _on_info_saved(self, info: dict):
        self._char_data["character_info"] = info
        parts = []
        if info.get("character_name"):
            parts.append(info["character_name"])
        cls_level = " ".join(filter(None, [info.get("class"), str(info["level"]) if info.get("class") else ""]))
        if cls_level:
            parts.append(cls_level)
        if info.get("race"):
            parts.append(info["race"])
        if info.get("background"):
            parts.append(info["background"])
        line1 = "  ·  ".join(parts) if parts else ""

        parts2 = []
        if info.get("alignment"):
            parts2.append(info["alignment"])
        if info.get("xp") is not None:
            parts2.append(f"{info['xp']:,} XP")
        if info.get("player_name"):
            parts2.append(f"Player: {info['player_name']}")
        line2 = "  ·  ".join(parts2) if parts2 else ""

        preview = "\n".join(filter(None, [line1, line2]))
        if preview:
            self._sections[1].set_preview(preview)
        self.statusBar().showMessage("  ✔  Character info saved.")

    def _open_ability_editor(self):
        dlg = AbilityScoreEditor(
            existing=self._char_data.get("ability_scores"),
            parent=self,
        )
        dlg.scores_saved.connect(self._on_scores_saved)
        dlg.exec()

    def _on_scores_saved(self, scores: dict):
        self._char_data["ability_scores"] = scores
        if not scores:
            return
        # Build preview lines for the section 2 card
        ABILITIES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        def mod(s): m = (s - 10) // 2; return f"+{m}" if m >= 0 else str(m)
        top = "  ·  ".join(
            f"{ab} {scores[ab]} ({mod(scores[ab])})"
            for ab in ABILITIES[:3] if ab in scores
        )
        bot = "  ·  ".join(
            f"{ab} {scores[ab]} ({mod(scores[ab])})"
            for ab in ABILITIES[3:] if ab in scores
        )
        preview = "\n".join(filter(None, [top, bot]))
        self._sections[2].set_preview(preview)
        self.statusBar().showMessage(
            "  ✔  Ability scores saved."
        )
