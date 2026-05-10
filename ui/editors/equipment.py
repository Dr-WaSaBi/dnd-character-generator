from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QLineEdit, QSpinBox, QDoubleSpinBox, QScrollArea, QCheckBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

# imported lazily to avoid circular import
def _open_starting_dialog(char_data: dict, parent) -> "StartingEquipmentDialog":
    from ui.editors.starting_equipment import StartingEquipmentDialog
    return StartingEquipmentDialog(char_data=char_data, parent=parent)

def _open_item_picker(parent) -> "ItemPickerDialog":
    from ui.editors.item_picker import ItemPickerDialog
    return ItemPickerDialog(parent=parent)

from ui.styles import (
    COLOR_PARCHMENT, COLOR_PARCHMENT_DARK, COLOR_PARCHMENT_HOVER,
    COLOR_SECTION_BORDER, COLOR_SECTION_BORDER_HOVER,
    COLOR_BADGE_BG, COLOR_BADGE_TEXT,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_HEADER, COLOR_TEXT_SUBTEXT,
    COLOR_GOLD_RULE,
    FONT_HEADER, FONT_BODY,
)

# GP conversion rates
COIN_TO_GP = {"CP": 0.01, "SP": 0.1, "EP": 0.5, "GP": 1.0, "PP": 10.0}
COIN_LABELS = {
    "CP": ("Copper",   "#B87333"),
    "SP": ("Silver",   "#C0C0C0"),
    "EP": ("Electrum", "#7EB6B6"),
    "GP": ("Gold",     "#D4AF37"),
    "PP": ("Platinum", "#9DA5A5"),
}


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


_FIELD_CSS = (
    f"QLineEdit{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"font-family:{FONT_BODY};font-size:9pt;padding:2px 4px;}}"
    f"QLineEdit:focus{{border:1px solid {COLOR_SECTION_BORDER_HOVER};}}"
)

_SPIN_CSS = (
    f"QSpinBox,QDoubleSpinBox{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"font-family:{FONT_BODY};font-size:9pt;padding:1px 2px;}}"
    f"QSpinBox:focus,QDoubleSpinBox:focus{{"
    f"border:1px solid {COLOR_SECTION_BORDER_HOVER};}}"
    f"QSpinBox::up-button,QSpinBox::down-button,"
    f"QDoubleSpinBox::up-button,QDoubleSpinBox::down-button{{width:14px;}}"
)


class ItemRow(QWidget):
    remove_requested = pyqtSignal(object)
    changed = pyqtSignal()

    def __init__(self, data: dict | None = None, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        self._build(data or {})

    def _build(self, d: dict):
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 2, 0, 2)
        row.setSpacing(6)

        self._name = QLineEdit(d.get("name", ""))
        self._name.setPlaceholderText("Item name")
        self._name.setFixedHeight(26)
        self._name.setStyleSheet(_FIELD_CSS)
        self._name.textChanged.connect(self.changed)

        self._qty = QSpinBox()
        self._qty.setRange(1, 9999)
        self._qty.setValue(d.get("qty", 1))
        self._qty.setFixedSize(60, 26)
        self._qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qty.setStyleSheet(_SPIN_CSS)
        self._qty.valueChanged.connect(self.changed)

        self._weight = QDoubleSpinBox()
        self._weight.setRange(0, 9999)
        self._weight.setDecimals(1)
        self._weight.setSingleStep(0.5)
        self._weight.setValue(d.get("weight", 0.0))
        self._weight.setFixedSize(70, 26)
        self._weight.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._weight.setStyleSheet(_SPIN_CSS)
        self._weight.valueChanged.connect(self.changed)

        self._notes = QLineEdit(d.get("notes", ""))
        self._notes.setPlaceholderText("Notes")
        self._notes.setFixedHeight(26)
        self._notes.setStyleSheet(_FIELD_CSS)

        self._equipped = QCheckBox("Worn / Wielded")
        self._equipped.setChecked(d.get("equipped", False))
        self._equipped.setToolTip(
            "Check if wearing this armor or wielding this weapon.\n"
            "Saving equipment will auto-update your AC and weapon attacks."
        )
        self._equipped.setFixedWidth(100)
        self._equipped.setStyleSheet(
            f"QCheckBox{{color:{COLOR_TEXT_SUBTEXT};"
            f"font-family:{FONT_BODY};font-size:8pt;background:transparent;}}"
            f"QCheckBox::indicator{{width:14px;height:14px;"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:2px;"
            f"background:{COLOR_PARCHMENT_DARK};}}"
            f"QCheckBox::indicator:checked{{background:{COLOR_BADGE_BG};"
            f"border-color:{COLOR_GOLD_RULE};}}"
            f"QCheckBox::indicator:hover{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
        )
        self._equipped.stateChanged.connect(self.changed)

        rm = QPushButton("✕")
        rm.setFixedSize(24, 24)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;font-size:9pt;}}"
            f"QPushButton:hover{{color:{COLOR_BADGE_BG};border-color:{COLOR_BADGE_BG};}}"
        )
        rm.clicked.connect(lambda: self.remove_requested.emit(self))

        row.addWidget(self._name, 3)
        row.addWidget(self._qty)
        row.addWidget(self._weight)
        row.addWidget(self._notes, 2)
        row.addWidget(self._equipped)
        row.addWidget(rm)

    def to_dict(self) -> dict:
        return {
            "name":     self._name.text().strip(),
            "qty":      self._qty.value(),
            "weight":   self._weight.value(),
            "notes":    self._notes.text().strip(),
            "equipped": self._equipped.isChecked(),
        }

    def total_weight(self) -> float:
        return self._qty.value() * self._weight.value()


class EquipmentEditor(QDialog):
    data_saved = pyqtSignal(dict)

    def __init__(self, char_data: dict | None = None,
                 existing: dict | None = None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Section ⑦  —  Equipment & Currency")
        self.setMinimumSize(600, 580)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        self._char_data  = char_data or {}
        self._item_rows: list[ItemRow] = []
        self._coin_spins: dict[str, QSpinBox] = {}
        self._existing = existing or {}
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 18)
        root.setSpacing(10)

        root.addWidget(_lbl("🎒  EQUIPMENT  &  CURRENCY", COLOR_TEXT_HEADER,
                             FONT_HEADER, 15, bold=True,
                             align=Qt.AlignmentFlag.AlignCenter))
        root.addWidget(_rule())

        # ── Equipment list ────────────────────────────────────────────────────
        root.addWidget(_lbl("CARRIED GEAR", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))

        # Column headers
        hdr = QHBoxLayout()
        hdr.setSpacing(6)
        for text, stretch, fixed in [
            ("Item Name",  3, None),
            ("Qty",   None, 60),
            ("Wt (lb)", None, 70),
            ("Notes",   2, None),
            ("Worn/Wield", None, 72),
            ("",       None, 24),
        ]:
            lbl = _lbl(text, COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True)
            if fixed:
                lbl.setFixedWidth(fixed)
            hdr.addWidget(lbl, stretch or 0)
        root.addLayout(hdr)

        # Scrollable item rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:1px solid {COLOR_SECTION_BORDER};"
            f"border-radius:4px;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        self._items_inner = QWidget()
        self._items_inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        self._items_layout = QVBoxLayout(self._items_inner)
        self._items_layout.setContentsMargins(6, 4, 6, 4)
        self._items_layout.setSpacing(2)
        self._items_layout.addStretch()
        scroll.setWidget(self._items_inner)
        root.addWidget(scroll, 1)

        for item in self._existing.get("items", []):
            self._add_item_row(item)

        # Add button + starting equipment button + weight total
        bottom_row = QHBoxLayout()
        add_btn = QPushButton("＋  Add Item")
        add_btn.setFixedHeight(30)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:5px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 14px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        add_btn.clicked.connect(self._on_pick_item)
        bottom_row.addWidget(add_btn)

        start_btn = QPushButton("⚔  Starting Equipment…")
        start_btn.setFixedHeight(30)
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        start_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:5px;"
            f"font-family:{FONT_BODY};font-size:10pt;font-weight:bold;padding:0 14px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
        )
        start_btn.clicked.connect(self._on_starting_equipment)
        bottom_row.addWidget(start_btn)
        bottom_row.addStretch()
        self._weight_lbl = _lbl("Total weight: 0.0 lb", COLOR_TEXT_SUBTEXT,
                                  FONT_BODY, 9, italic=True,
                                  align=Qt.AlignmentFlag.AlignRight)
        bottom_row.addWidget(self._weight_lbl)
        root.addLayout(bottom_row)

        root.addWidget(_rule())

        # ── Currency ──────────────────────────────────────────────────────────
        root.addWidget(_lbl("CURRENCY", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))

        coin_row = QHBoxLayout()
        coin_row.setSpacing(10)

        _COIN_SPIN_CSS = (
            f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};"
            f"color:{COLOR_TEXT_PRIMARY};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
            f"font-family:{FONT_HEADER};font-size:13pt;font-weight:bold;"
            f"padding:2px 4px;}}"
            f"QSpinBox:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
            f"QSpinBox::up-button,QSpinBox::down-button{{width:18px;}}"
        )

        for coin, (label, color) in COIN_LABELS.items():
            card = QWidget()
            card.setStyleSheet(
                f"background:{COLOR_PARCHMENT_DARK};"
                f"border:2px solid {color};border-radius:6px;"
            )
            cl = QVBoxLayout(card)
            cl.setContentsMargins(8, 6, 8, 6)
            cl.setSpacing(3)

            cl.addWidget(_lbl(label.upper(), color, FONT_BODY, 8, bold=True,
                               align=Qt.AlignmentFlag.AlignCenter))

            spin = QSpinBox()
            spin.setRange(0, 999999)
            spin.setValue(self._existing.get("currency", {}).get(coin, 0))
            spin.setFixedHeight(36)
            spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spin.setStyleSheet(_COIN_SPIN_CSS.replace(
                COLOR_SECTION_BORDER, color).replace(
                COLOR_SECTION_BORDER_HOVER, color))
            spin.valueChanged.connect(self._update_gp_total)
            self._coin_spins[coin] = spin
            cl.addWidget(spin)

            cl.addWidget(_lbl(coin, COLOR_TEXT_SUBTEXT, FONT_BODY, 7, italic=True,
                               align=Qt.AlignmentFlag.AlignCenter))
            coin_row.addWidget(card)

        root.addLayout(coin_row)

        self._gp_lbl = _lbl("", COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
                              align=Qt.AlignmentFlag.AlignRight)
        root.addWidget(self._gp_lbl)
        self._update_gp_total()

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

    # ── Item rows ─────────────────────────────────────────────────────────────

    def _add_item_row(self, data: dict | None = None):
        row = ItemRow(data)
        row.remove_requested.connect(self._remove_item_row)
        row.changed.connect(self._update_weight)
        self._item_rows.append(row)
        self._items_layout.insertWidget(self._items_layout.count() - 1, row)
        self._update_weight()

    def _remove_item_row(self, row: ItemRow):
        self._items_layout.removeWidget(row)
        row.deleteLater()
        self._item_rows.remove(row)
        self._update_weight()

    def _on_pick_item(self):
        dlg = _open_item_picker(self)
        dlg.items_chosen.connect(self._apply_picked_items)
        dlg.exec()

    def _apply_picked_items(self, items: list):
        for item in items:
            self._add_item_row(item)

    def _on_starting_equipment(self):
        dlg = _open_starting_dialog(self._char_data, self)
        dlg.equipment_chosen.connect(self._apply_starting_equipment)
        dlg.exec()

    def _apply_starting_equipment(self, items: list, gold_gp: int):
        for item in items:
            self._add_item_row(item)
        if gold_gp:
            current = self._coin_spins["GP"].value()
            self._coin_spins["GP"].setValue(current + gold_gp)

    def _update_weight(self):
        total = sum(r.total_weight() for r in self._item_rows)
        self._weight_lbl.setText(f"Total weight: {total:.1f} lb")

    # ── Currency ──────────────────────────────────────────────────────────────

    def _update_gp_total(self):
        total = sum(
            self._coin_spins[c].value() * COIN_TO_GP[c]
            for c in COIN_LABELS
        )
        self._gp_lbl.setText(f"Total value: {total:,.2f} gp")

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        items = [r.to_dict() for r in self._item_rows if r.to_dict()["name"]]
        currency = {c: self._coin_spins[c].value() for c in COIN_LABELS}
        self.data_saved.emit({"items": items, "currency": currency})
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
