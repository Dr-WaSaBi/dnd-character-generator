from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QListWidget, QListWidgetItem, QLineEdit,
    QTabWidget, QSpinBox,
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

# ── Item catalog ──────────────────────────────────────────────────────────────
# Each entry: (name, weight_lb, notes)

ARMOR: list[tuple[str, float, str]] = [
    # Light
    ("Padded Armor",        8.0,  "AC 11 + DEX mod · Disadvantage on Stealth · 5 gp"),
    ("Leather Armor",      10.0,  "AC 11 + DEX mod · 10 gp"),
    ("Studded Leather",    13.0,  "AC 12 + DEX mod · 45 gp"),
    # Medium
    ("Hide Armor",         12.0,  "AC 12 + DEX mod (max +2) · 10 gp"),
    ("Chain Shirt",        20.0,  "AC 13 + DEX mod (max +2) · 50 gp"),
    ("Scale Mail",         45.0,  "AC 14 + DEX mod (max +2) · Disadvantage on Stealth · 50 gp"),
    ("Breastplate",        20.0,  "AC 14 + DEX mod (max +2) · 400 gp"),
    ("Half Plate",         40.0,  "AC 15 + DEX mod (max +2) · Disadvantage on Stealth · 750 gp"),
    # Heavy
    ("Ring Mail",          40.0,  "AC 14 · Disadvantage on Stealth · 30 gp"),
    ("Chain Mail",         55.0,  "AC 16 · STR 13 required · Disadvantage on Stealth · 75 gp"),
    ("Splint Armor",       60.0,  "AC 17 · STR 15 required · Disadvantage on Stealth · 200 gp"),
    ("Plate Armor",        65.0,  "AC 18 · STR 15 required · Disadvantage on Stealth · 1500 gp"),
    # Shield
    ("Shield",              6.0,  "+2 AC · 10 gp"),
]

WEAPONS_SIMPLE: list[tuple[str, float, str]] = [
    ("Club",                2.0,  "1d4 bludgeoning · Light · 1 sp"),
    ("Dagger",              1.0,  "1d4 piercing · Finesse, Light, Thrown 20/60 · 2 gp"),
    ("Greatclub",          10.0,  "1d8 bludgeoning · Two-handed · 2 sp"),
    ("Handaxe",             2.0,  "1d6 slashing · Light, Thrown 20/60 · 5 gp"),
    ("Javelin",             2.0,  "1d6 piercing · Thrown 30/120 · 5 sp"),
    ("Light Hammer",        2.0,  "1d4 bludgeoning · Light, Thrown 20/60 · 2 gp"),
    ("Mace",                4.0,  "1d6 bludgeoning · 5 gp"),
    ("Quarterstaff",        4.0,  "1d6 bludgeoning · Versatile (1d8) · 2 sp"),
    ("Sickle",              2.0,  "1d4 slashing · Light · 1 gp"),
    ("Spear",               3.0,  "1d6 piercing · Thrown 20/60, Versatile (1d8) · 1 gp"),
    ("Light Crossbow",      5.0,  "1d8 piercing · Loading, Range 80/320, Two-handed · 25 gp"),
    ("Dart",                0.25, "1d4 piercing · Finesse, Thrown 20/60 · 5 cp"),
    ("Shortbow",            2.0,  "1d6 piercing · Range 80/320, Two-handed · 25 gp"),
    ("Sling",               0.0,  "1d4 bludgeoning · Range 30/120 · 1 sp"),
]

WEAPONS_MARTIAL: list[tuple[str, float, str]] = [
    ("Battleaxe",           4.0,  "1d8 slashing · Versatile (1d10) · 10 gp"),
    ("Flail",               2.0,  "1d8 bludgeoning · 10 gp"),
    ("Glaive",              6.0,  "1d10 slashing · Heavy, Reach, Two-handed · 20 gp"),
    ("Greataxe",            7.0,  "1d12 slashing · Heavy, Two-handed · 30 gp"),
    ("Greatsword",          6.0,  "2d6 slashing · Heavy, Two-handed · 50 gp"),
    ("Halberd",             6.0,  "1d10 slashing · Heavy, Reach, Two-handed · 20 gp"),
    ("Lance",               6.0,  "1d12 piercing · Reach, Special · 10 gp"),
    ("Longsword",           3.0,  "1d8 slashing · Versatile (1d10) · 15 gp"),
    ("Maul",               10.0,  "2d6 bludgeoning · Heavy, Two-handed · 10 gp"),
    ("Morningstar",         4.0,  "1d8 piercing · 15 gp"),
    ("Pike",               18.0,  "1d10 piercing · Heavy, Reach, Two-handed · 5 gp"),
    ("Rapier",              2.0,  "1d8 piercing · Finesse · 25 gp"),
    ("Scimitar",            3.0,  "1d6 slashing · Finesse, Light · 25 gp"),
    ("Shortsword",          2.0,  "1d6 piercing · Finesse, Light · 10 gp"),
    ("Trident",             4.0,  "1d6 piercing · Thrown 20/60, Versatile (1d8) · 5 gp"),
    ("War Pick",            2.0,  "1d8 piercing · 5 gp"),
    ("Warhammer",           2.0,  "1d8 bludgeoning · Versatile (1d10) · 15 gp"),
    ("Whip",                3.0,  "1d4 slashing · Finesse, Reach · 2 gp"),
    ("Hand Crossbow",       3.0,  "1d6 piercing · Light, Loading, Range 30/120 · 75 gp"),
    ("Heavy Crossbow",     18.0,  "1d10 piercing · Heavy, Loading, Range 100/400, Two-handed · 50 gp"),
    ("Longbow",             2.0,  "1d8 piercing · Heavy, Range 150/600, Two-handed · 50 gp"),
    ("Net",                 3.0,  "Thrown 5/15, Special · 1 gp"),
]

GEAR: list[tuple[str, float, str]] = [
    ("Arrows (20)",         1.0,  "Ammunition for bows · 1 gp"),
    ("Blowgun Needles (50)",1.0,  "Ammunition for blowgun · 1 gp"),
    ("Crossbow Bolts (20)", 1.5,  "Ammunition for crossbows · 1 gp"),
    ("Sling Bullets (20)",  1.5,  "Ammunition for slings · 4 cp"),
    ("Arcane Focus",        1.0,  "Crystal / orb / rod / staff / wand · 10–20 gp"),
    ("Backpack",            5.0,  "Holds 30 lb / 1 cu. ft. · 2 gp"),
    ("Bedroll",             7.0,  "1 gp"),
    ("Blanket",             3.0,  "5 sp"),
    ("Candles (10)",        0.0,  "1 hour light, 5 ft radius · 1 cp each"),
    ("Climber's Kit",      12.0,  "Pitons, boot tips, gloves, harness · 25 gp"),
    ("Component Pouch",     2.0,  "Holds spell components · 25 gp"),
    ("Crowbar",             5.0,  "Advantage on STR checks where applicable · 2 gp"),
    ("Disguise Kit",        3.0,  "Proficiency required for best results · 25 gp"),
    ("Druidic Focus",       1.0,  "Sprig of mistletoe / wooden staff / yew wand · varies"),
    ("Flask",               1.0,  "2 cp"),
    ("Grappling Hook",      4.0,  "2 gp"),
    ("Hammer",              3.0,  "1 gp"),
    ("Healer's Kit",        3.0,  "10 uses, stabilise dying creature · 5 gp"),
    ("Herbalism Kit",       3.0,  "Identify and apply herbs · 5 gp"),
    ("Holy Symbol",         1.0,  "Spellcasting focus for Clerics and Paladins · 5 gp"),
    ("Holy Water (flask)",  1.0,  "2d6 radiant vs undead/fiends · 25 gp"),
    ("Hunting Trap",       25.0,  "DC 13 STR to escape, 1d4 piercing · 5 gp"),
    ("Lantern (bullseye)",  2.0,  "60 ft cone, 6 hrs/flask oil · 10 gp"),
    ("Lantern (hooded)",    2.0,  "30 ft radius, 6 hrs/flask oil · 5 gp"),
    ("Lock",                1.0,  "DC 15 Thieves' Tools to pick · 10 gp"),
    ("Manacles",            6.0,  "DC 20 STR or Escape Artist to break · 2 gp"),
    ("Mess Kit",            1.0,  "Tin box with cup, plate, fork, knife · 2 sp"),
    ("Mirror (steel)",      0.5,  "5 gp"),
    ("Oil (flask)",         1.0,  "Burns 6 hrs, sets fire · 1 sp"),
    ("Pitons (10)",         2.5,  "5 cp each"),
    ("Pole (10 ft)",        7.0,  "5 cp"),
    ("Pot (iron)",         10.0,  "2 sp"),
    ("Potion of Healing",   0.5,  "Restores 2d4+2 HP · 50 gp"),
    ("Pouch",               1.0,  "Holds 6 lb / 1/5 cu. ft. · 5 sp"),
    ("Rations (1 day)",     2.0,  "Dry food for one day · 5 sp"),
    ("Rope, Hempen (50 ft)",10.0, "2 HP, AC 11 · 1 gp"),
    ("Rope, Silk (50 ft)",  5.0,  "10 gp"),
    ("Shovel",              5.0,  "2 gp"),
    ("Spellbook",           3.0,  "Contains your prepared wizard spells · 50 gp"),
    ("Thieves' Tools",      1.0,  "Pick locks and disarm traps · 25 gp"),
    ("Tinderbox",           1.0,  "Light fires · 5 sp"),
    ("Tinker's Tools",     10.0,  "Construct/repair small objects · 50 gp"),
    ("Torch",               1.0,  "20 ft light, 1 hr · 1 cp"),
    ("Torch (10)",         10.0,  "20 ft light, 1 hr each · 1 cp each"),
    ("Waterskin",           5.0,  "Holds 4 pints · 2 sp"),
    ("Whetstone",           1.0,  "1 cp"),
]

PACKS: list[tuple[str, float, str]] = [
    ("Burglar's Pack",     47.5,  "Backpack, 1000 ball bearings, 10 ft string, bell, 5 candles, crowbar, hammer, 10 pitons, hooded lantern, 2 flasks oil, 5 days rations, tinderbox, waterskin · 16 gp"),
    ("Diplomat's Pack",    36.0,  "Chest, 2 map/scroll cases, fine clothes, ink bottle, ink pen, lamp, 2 flasks oil, 5 sheets paper, perfume, sealing wax, soap · 39 gp"),
    ("Dungeoneer's Pack",  61.5,  "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft hempen rope · 12 gp"),
    ("Entertainer's Pack", 38.0,  "Backpack, bedroll, 2 costumes, 5 candles, 5 days rations, waterskin, disguise kit · 40 gp"),
    ("Explorer's Pack",    59.0,  "Backpack, bedroll, mess kit, tinderbox, 10 torches, 10 days rations, waterskin, 50 ft hempen rope · 10 gp"),
    ("Priest's Pack",      24.0,  "Backpack, blanket, 10 candles, tinderbox, alms box, 2 blocks incense, censer, vestments, 2 days rations, waterskin · 19 gp"),
    ("Scholar's Pack",     10.0,  "Backpack, book of lore, ink bottle, ink pen, 10 sheets parchment, bag of sand, small knife · 40 gp"),
]

CATEGORIES: list[tuple[str, list]] = [
    ("Armor & Shields",   ARMOR),
    ("Simple Weapons",    WEAPONS_SIMPLE),
    ("Martial Weapons",   WEAPONS_MARTIAL),
    ("Adventuring Gear",  GEAR),
    ("Packs & Bags",      PACKS),
]


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


class ItemPickerDialog(QDialog):
    """Select one or more items from the PHB catalog and return them."""
    items_chosen = pyqtSignal(list)   # list of {name, qty, weight, notes}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browse Items")
        self.setMinimumSize(620, 540)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(10)

        root.addWidget(_lbl("📦  BROWSE  ITEMS", COLOR_TEXT_HEADER, FONT_HEADER, 15,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        # Search
        search_row = QHBoxLayout()
        search_row.addWidget(_lbl("Search:", COLOR_TEXT_HEADER, FONT_BODY, 10))
        self._search = QLineEdit()
        self._search.setPlaceholderText("Type to filter…")
        self._search.setFixedHeight(28)
        self._search.setStyleSheet(
            f"QLineEdit{{background:{COLOR_PARCHMENT_DARK};"
            f"color:{COLOR_TEXT_PRIMARY};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:2px 6px;}}"
            f"QLineEdit:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
        )
        self._search.textChanged.connect(self._on_search)
        search_row.addWidget(self._search, 1)
        root.addLayout(search_row)

        root.addWidget(_rule())

        # Tabs
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(
            f"QTabWidget::pane{{background:{COLOR_PARCHMENT};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;}}"
            f"QTabBar::tab{{background:{COLOR_PARCHMENT_DARK};"
            f"color:{COLOR_TEXT_HEADER};"
            f"font-family:{FONT_BODY};font-size:9pt;"
            f"padding:5px 12px;border:1px solid {COLOR_SECTION_BORDER};"
            f"border-bottom:none;border-radius:4px 4px 0 0;margin-right:2px;}}"
            f"QTabBar::tab:selected{{background:{COLOR_PARCHMENT};"
            f"font-weight:bold;}}"
            f"QTabBar::tab:hover:!selected{{background:{COLOR_PARCHMENT_HOVER};}}"
        )

        _LIST_CSS = (
            f"QListWidget{{background:{COLOR_PARCHMENT};"
            f"border:none;"
            f"font-family:{FONT_BODY};font-size:9pt;"
            f"color:{COLOR_TEXT_PRIMARY};}}"
            f"QListWidget::item{{padding:4px 6px;"
            f"border-bottom:1px solid {COLOR_PARCHMENT_DARK};}}"
            f"QListWidget::item:selected{{background:{COLOR_BADGE_BG};"
            f"color:{COLOR_BADGE_TEXT};}}"
            f"QListWidget::item:hover:!selected{{background:{COLOR_PARCHMENT_DARK};}}"
        )

        self._lists: dict[str, QListWidget] = {}
        self._all_items: list[tuple[str, float, str]] = []

        for cat_name, items in CATEGORIES:
            lst = QListWidget()
            lst.setStyleSheet(_LIST_CSS)
            lst.setAlternatingRowColors(False)
            lst.itemDoubleClicked.connect(self._on_double_click)
            for name, weight, notes in items:
                item = QListWidgetItem(f"{name}  —  {notes}")
                item.setData(Qt.ItemDataRole.UserRole, (name, weight, notes))
                lst.addItem(item)
                self._all_items.append((name, weight, notes))
            self._lists[cat_name] = lst
            tab = QWidget()
            tab.setStyleSheet(f"background:{COLOR_PARCHMENT};")
            tlo = QVBoxLayout(tab)
            tlo.setContentsMargins(4, 4, 4, 4)
            tlo.addWidget(lst)
            self._tabs.addTab(tab, cat_name)

        root.addWidget(self._tabs, 1)

        root.addWidget(_rule())

        # Qty + buttons
        bottom = QHBoxLayout()
        bottom.addWidget(_lbl("Qty:", COLOR_TEXT_HEADER, FONT_BODY, 10))
        self._qty = QSpinBox()
        self._qty.setRange(1, 9999)
        self._qty.setValue(1)
        self._qty.setFixedSize(60, 32)
        self._qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qty.setStyleSheet(
            f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_PRIMARY};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:1px 4px;}}"
            f"QSpinBox:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
            f"QSpinBox::up-button,QSpinBox::down-button{{width:16px;}}"
        )
        bottom.addWidget(self._qty)
        bottom.addStretch()

        hint = _lbl("Double-click or select and click Add", COLOR_TEXT_SUBTEXT,
                     FONT_BODY, 8, italic=True)
        bottom.addWidget(hint)
        bottom.addSpacing(12)

        cancel = QPushButton("Cancel")
        cancel.setFixedHeight(34)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 14px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        cancel.clicked.connect(self.reject)
        bottom.addWidget(cancel)

        add_btn = QPushButton("＋  Add to Equipment")
        add_btn.setFixedHeight(34)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:6px;"
            f"font-family:{FONT_HEADER};font-size:10pt;font-weight:bold;padding:0 16px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
        )
        add_btn.clicked.connect(self._on_add)
        bottom.addWidget(add_btn)

        root.addLayout(bottom)

    # ── Search ────────────────────────────────────────────────────────────────

    def _on_search(self, text: str):
        text = text.strip().lower()
        for cat_name, lst in self._lists.items():
            for i in range(lst.count()):
                item = lst.item(i)
                name, _, _ = item.data(Qt.ItemDataRole.UserRole)
                item.setHidden(bool(text) and text not in name.lower())

    # ── Selection ─────────────────────────────────────────────────────────────

    def _current_item(self) -> tuple | None:
        lst = self._tabs.currentWidget().layout().itemAt(0).widget()
        selected = lst.selectedItems()
        if not selected:
            return None
        return selected[0].data(Qt.ItemDataRole.UserRole)

    def _on_double_click(self, list_item: QListWidgetItem):
        data = list_item.data(Qt.ItemDataRole.UserRole)
        if data:
            name, weight, notes = data
            qty = self._qty.value()
            self.items_chosen.emit([{"name": name, "qty": qty,
                                     "weight": weight, "notes": notes}])
            self.accept()

    def _on_add(self):
        data = self._current_item()
        if not data:
            return
        name, weight, notes = data
        qty = self._qty.value()
        self.items_chosen.emit([{"name": name, "qty": qty,
                                 "weight": weight, "notes": notes}])
        self.accept()
