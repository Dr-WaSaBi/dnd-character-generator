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
        super().__init__(parent)
        self.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:5px;"
        )
        self._build(data or {})

    def _build(self, d: dict):
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
        return {
            "name":        self._name.text().strip(),
            "description": self._desc.toPlainText().strip(),
        }


class FeaturesEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ⑨  —  Features & Traits")
        self.setMinimumSize(560, 580)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._cards: list[FeatureCard] = []
        self._build_ui(existing or {})

    def _build_ui(self, data: dict):
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
        root.addWidget(add_btn)

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
        card = FeatureCard(data)
        card.remove_requested.connect(self._remove_card)
        self._cards.append(card)
        self._inner_lo.insertWidget(self._inner_lo.count() - 1, card)

    def _remove_card(self, card: FeatureCard):
        self._inner_lo.removeWidget(card)
        card.deleteLater()
        self._cards.remove(card)

    def _on_save(self):
        features = [c.to_dict() for c in self._cards if c.to_dict()["name"]]
        self.data_saved.emit({"features": features})
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
