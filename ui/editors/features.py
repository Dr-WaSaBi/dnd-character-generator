# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/editors/features.py                                    ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Editor dialog for features & traits. Shows scrollable FeatureCards ║
# ║  and can auto-populate from features_data based on class/race.      ║
# ╚══════════════════════════════════════════════════════════════════════╝

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QLineEdit, QTextEdit, QScrollArea,
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
from ui.editors.features_data import CLASS_FEATURES, RACE_TRAITS, BACKGROUND_FEATURES


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


class FeatureCard(QWidget):
    remove_requested = pyqtSignal(object)

    _NAME_CSS = (
        f"QLineEdit{{background:{COLOR_PARCHMENT};"
        f"color:{COLOR_TEXT_HEADER};"
        f"border:none;border-bottom:1px solid {COLOR_SECTION_BORDER};"
        f"font-family:{FONT_HEADER};font-size:10pt;font-weight:bold;"
        f"padding:2px 4px;}}"
        f"QLineEdit:focus{{border-bottom:2px solid {COLOR_SECTION_BORDER_HOVER};}}"
    )
    _DESC_CSS = (
        f"QTextEdit{{background:{COLOR_PARCHMENT};"
        f"color:{COLOR_TEXT_PRIMARY};"
        f"border:none;"
        f"font-family:{FONT_BODY};font-size:9pt;padding:2px 4px;}}"
    )

    def __init__(self, data: dict | None = None, parent=None):
        """Create a parchment-styled card widget, optionally pre-filled with name and description."""
        super().__init__(parent)
        self.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:5px;"
        )
        self._build(data or {})

    def _build(self, d: dict):
        """Lay out the feature-name field, remove button, and description text editor."""
        lo = QVBoxLayout(self)
        lo.setContentsMargins(8, 6, 8, 6)
        lo.setSpacing(4)

        # Header row: name + remove button
        hdr = QHBoxLayout()
        hdr.setContentsMargins(0, 0, 0, 0)
        hdr.setSpacing(6)

        self._name = QLineEdit(d.get("name", ""))
        self._name.setPlaceholderText("Feature / Trait name")
        self._name.setStyleSheet(self._NAME_CSS)
        self._name.setFixedHeight(26)
        hdr.addWidget(self._name, 1)

        rm = QPushButton("✕")
        rm.setFixedSize(22, 22)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;font-size:9pt;}}"
            f"QPushButton:hover{{color:{COLOR_BADGE_BG};border-color:{COLOR_BADGE_BG};}}"
        )
        rm.clicked.connect(lambda: self.remove_requested.emit(self))
        hdr.addWidget(rm)
        lo.addLayout(hdr)

        self._desc = QTextEdit()
        self._desc.setPlaceholderText("Description…")
        self._desc.setMinimumHeight(60)
        self._desc.setMaximumHeight(90)
        self._desc.setStyleSheet(self._DESC_CSS)
        if d.get("description"):
            self._desc.setPlainText(d["description"])
        lo.addWidget(self._desc)

    def to_dict(self) -> dict:
        """Return a dict with 'name' and 'description' extracted from the card's input widgets."""
        return {
            "name":        self._name.text().strip(),
            "description": self._desc.toPlainText().strip(),
        }


class FeaturesEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, char_data: dict | None = None, existing: dict | None = None, parent=None):
        """Initialize the dialog, load any existing feature cards, and build the scrollable UI."""
        super().__init__(parent)
        self._char_data = char_data or {}
        self.setWindowTitle("Section ⑨  —  Features & Traits")
        self.setMinimumSize(560, 580)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._cards: list[FeatureCard] = []
        self._build_ui(existing or {})

    def _build_ui(self, data: dict):
        """Build the scrollable card list, Add and Load buttons, status label, and Save/Cancel buttons."""
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(10)

        root.addWidget(_lbl("✨  FEATURES  &  TRAITS", COLOR_TEXT_HEADER, FONT_HEADER, 16,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))
        root.addWidget(_lbl(
            "Class features, racial traits, and background abilities",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
            align=Qt.AlignmentFlag.AlignCenter,
        ))
        root.addWidget(_rule())

        # Scrollable cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:none;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        self._inner = QWidget()
        self._inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        self._inner_lo = QVBoxLayout(self._inner)
        self._inner_lo.setContentsMargins(2, 2, 2, 2)
        self._inner_lo.setSpacing(8)
        self._inner_lo.addStretch()
        scroll.setWidget(self._inner)
        root.addWidget(scroll, 1)

        for feat in data.get("features", []):
            self._add_card(feat)

        # Button row: Add manually + Load from Class & Race
        btn_add_row = QHBoxLayout()
        btn_add_row.setSpacing(8)

        add_btn = QPushButton("＋  Add Feature / Trait")
        add_btn.setFixedHeight(32)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:5px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 14px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        add_btn.clicked.connect(lambda: self._add_card())
        btn_add_row.addWidget(add_btn, 1)

        load_btn = QPushButton("⚙  Load from Class & Race")
        load_btn.setFixedHeight(32)
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:5px;"
            f"font-family:{FONT_BODY};font-size:10pt;font-weight:bold;padding:0 14px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
        )
        load_btn.clicked.connect(self._load_from_class_race)
        btn_add_row.addWidget(load_btn)

        root.addLayout(btn_add_row)

        # Status label for feedback after auto-load
        self._status_lbl = _lbl("", COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
                                  align=Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self._status_lbl)

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

    def _add_card(self, data: dict | None = None):
        """Insert a new FeatureCard before the trailing stretch in the scrollable inner layout."""
        card = FeatureCard(data)
        card.remove_requested.connect(self._remove_card)
        self._cards.append(card)
        self._inner_lo.insertWidget(self._inner_lo.count() - 1, card)

    def _remove_card(self, card: FeatureCard):
        """Remove a FeatureCard from the layout and the internal list."""
        self._inner_lo.removeWidget(card)
        card.deleteLater()
        self._cards.remove(card)

    def _load_from_class_race(self):
        """Auto-populate cards from CLASS_FEATURES, RACE_TRAITS, and BACKGROUND_FEATURES, skipping duplicates."""
        info = self._char_data.get("character_info", {})
        cls        = info.get("class", "")
        race       = info.get("race", "")
        background = info.get("background", "")
        level      = info.get("level", 1) or 1

        existing_names = {c.to_dict()["name"] for c in self._cards}
        added = 0

        # Class features up to current level
        for feat_level, feat_name, feat_desc in CLASS_FEATURES.get(cls, []):
            if feat_level <= level and feat_name not in existing_names:
                self._add_card({"name": feat_name, "description": feat_desc})
                existing_names.add(feat_name)
                added += 1

        # Racial traits
        for trait_name, trait_desc in RACE_TRAITS.get(race, []):
            if trait_name not in existing_names:
                self._add_card({"name": trait_name, "description": trait_desc})
                existing_names.add(trait_name)
                added += 1

        # Background feature
        bg_entry = BACKGROUND_FEATURES.get(background)
        if bg_entry:
            feat_name, feat_desc = bg_entry
            if feat_name not in existing_names:
                self._add_card({"name": feat_name, "description": feat_desc})
                added += 1

        self._status_lbl.setText(f"Added {added} feature{'s' if added != 1 else ''}.")

    def _on_save(self):
        """Collect non-empty feature cards into a list, emit data_saved, and close the dialog."""
        features = [c.to_dict() for c in self._cards if c.to_dict()["name"]]
        self.data_saved.emit({"features": features})
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
