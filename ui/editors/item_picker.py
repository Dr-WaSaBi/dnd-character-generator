from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QListWidget, QListWidgetItem, QLineEdit,
    QTabWidget, QSpinBox, QScrollArea,
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

# ── Stat lookup tables (used by character_sheet to auto-sync AC & attacks) ────

# name → (ac_base, armor_type)
# armor_type: "light" = base+DEX, "medium" = base+DEX(max+2), "heavy" = base, "shield" = +2
ARMOR_DATA: dict[str, tuple[int, str]] = {
    "Padded Armor":    (11, "light"),
    "Leather Armor":   (11, "light"),
    "Studded Leather": (12, "light"),
    "Hide Armor":      (12, "medium"),
    "Chain Shirt":     (13, "medium"),
    "Scale Mail":      (14, "medium"),
    "Breastplate":     (14, "medium"),
    "Half Plate":      (15, "medium"),
    "Ring Mail":       (14, "heavy"),
    "Chain Mail":      (16, "heavy"),
    "Splint Armor":    (17, "heavy"),
    "Plate Armor":     (18, "heavy"),
    "Shield":          (2,  "shield"),
}

# name → {damage, dmg_type, finesse, ranged}
WEAPON_DATA: dict[str, dict] = {
    # Simple Melee
    "Club":           {"damage": "1d4",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Dagger":         {"damage": "1d4",  "dmg_type": "piercing",    "finesse": True,  "ranged": False},
    "Greatclub":      {"damage": "1d8",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Handaxe":        {"damage": "1d6",  "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Javelin":        {"damage": "1d6",  "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "Light Hammer":   {"damage": "1d4",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Mace":           {"damage": "1d6",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Quarterstaff":   {"damage": "1d6",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Sickle":         {"damage": "1d4",  "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Spear":          {"damage": "1d6",  "dmg_type": "piercing",    "finesse": False, "ranged": False},
    # Simple Ranged
    "Light Crossbow": {"damage": "1d8",  "dmg_type": "piercing",    "finesse": False, "ranged": True},
    "Dart":           {"damage": "1d4",  "dmg_type": "piercing",    "finesse": True,  "ranged": True},
    "Shortbow":       {"damage": "1d6",  "dmg_type": "piercing",    "finesse": False, "ranged": True},
    "Sling":          {"damage": "1d4",  "dmg_type": "bludgeoning", "finesse": False, "ranged": True},
    # Martial Melee
    "Battleaxe":      {"damage": "1d8",  "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Flail":          {"damage": "1d8",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Glaive":         {"damage": "1d10", "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Greataxe":       {"damage": "1d12", "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Greatsword":     {"damage": "2d6",  "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Halberd":        {"damage": "1d10", "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Lance":          {"damage": "1d12", "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "Longsword":      {"damage": "1d8",  "dmg_type": "slashing",    "finesse": False, "ranged": False},
    "Maul":           {"damage": "2d6",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Morningstar":    {"damage": "1d8",  "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "Pike":           {"damage": "1d10", "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "Rapier":         {"damage": "1d8",  "dmg_type": "piercing",    "finesse": True,  "ranged": False},
    "Scimitar":       {"damage": "1d6",  "dmg_type": "slashing",    "finesse": True,  "ranged": False},
    "Shortsword":     {"damage": "1d6",  "dmg_type": "piercing",    "finesse": True,  "ranged": False},
    "Trident":        {"damage": "1d6",  "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "War Pick":       {"damage": "1d8",  "dmg_type": "piercing",    "finesse": False, "ranged": False},
    "Warhammer":      {"damage": "1d8",  "dmg_type": "bludgeoning", "finesse": False, "ranged": False},
    "Whip":           {"damage": "1d4",  "dmg_type": "slashing",    "finesse": True,  "ranged": False},
    # Martial Ranged
    "Hand Crossbow":  {"damage": "1d6",  "dmg_type": "piercing",    "finesse": False, "ranged": True},
    "Heavy Crossbow": {"damage": "1d10", "dmg_type": "piercing",    "finesse": False, "ranged": True},
    "Longbow":        {"damage": "1d8",  "dmg_type": "piercing",    "finesse": False, "ranged": True},
    "Net":            {"damage": "—",    "dmg_type": "special",     "finesse": False, "ranged": True},
}

# ── Shared styles ─────────────────────────────────────────────────────────────

_SEARCH_CSS = (
    f"QLineEdit{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_PRIMARY};"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
    f"font-family:{FONT_BODY};font-size:10pt;padding:2px 6px;}}"
    f"QLineEdit:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
)

_TAB_CSS = (
    f"QTabWidget::pane{{background:{COLOR_PARCHMENT};"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;}}"
    f"QTabBar::tab{{background:{COLOR_PARCHMENT_DARK};"
    f"color:{COLOR_TEXT_HEADER};"
    f"font-family:{FONT_BODY};font-size:9pt;"
    f"padding:5px 10px;border:1px solid {COLOR_SECTION_BORDER};"
    f"border-bottom:none;border-radius:4px 4px 0 0;margin-right:2px;}}"
    f"QTabBar::tab:selected{{background:{COLOR_PARCHMENT};font-weight:bold;}}"
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

_QTY_CSS = (
    f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_PRIMARY};"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:4px;"
    f"font-family:{FONT_BODY};font-size:10pt;padding:1px 4px;}}"
    f"QSpinBox:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
    f"QSpinBox::up-button,QSpinBox::down-button{{width:16px;}}"
)

_CART_QTY_CSS = (
    f"QSpinBox{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_PRIMARY};"
    f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"font-family:{FONT_BODY};font-size:9pt;padding:1px 2px;}}"
    f"QSpinBox:focus{{border-color:{COLOR_SECTION_BORDER_HOVER};}}"
    f"QSpinBox::up-button,QSpinBox::down-button{{width:14px;}}"
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


# ── Cart row widget ───────────────────────────────────────────────────────────

class CartRow(QWidget):
    remove_requested = pyqtSignal(object)

    def __init__(self, name: str, weight: float, notes: str, qty: int = 1, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background:transparent;")
        self._name = name
        self._weight = weight
        self._notes = notes
        self._build(qty)

    def _build(self, qty: int):
        row = QHBoxLayout(self)
        row.setContentsMargins(2, 2, 2, 2)
        row.setSpacing(6)

        name_lbl = _lbl(self._name, COLOR_TEXT_PRIMARY, FONT_BODY, 9)

        self._qty_spin = QSpinBox()
        self._qty_spin.setRange(1, 9999)
        self._qty_spin.setValue(qty)
        self._qty_spin.setFixedSize(58, 24)
        self._qty_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qty_spin.setStyleSheet(_CART_QTY_CSS)

        wt_lbl = _lbl(f"{self._weight:.1f} lb", COLOR_TEXT_SUBTEXT, FONT_BODY, 8,
                       align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        wt_lbl.setFixedWidth(52)

        rm = QPushButton("✕")
        rm.setFixedSize(22, 22)
        rm.setCursor(Qt.CursorShape.PointingHandCursor)
        rm.setStyleSheet(
            f"QPushButton{{background:transparent;color:{COLOR_TEXT_SUBTEXT};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:3px;font-size:9pt;}}"
            f"QPushButton:hover{{color:{COLOR_BADGE_BG};border-color:{COLOR_BADGE_BG};}}"
        )
        rm.clicked.connect(lambda: self.remove_requested.emit(self))

        row.addWidget(name_lbl, 1)
        row.addWidget(_lbl("×", COLOR_TEXT_SUBTEXT, FONT_BODY, 9))
        row.addWidget(self._qty_spin)
        row.addWidget(wt_lbl)
        row.addWidget(rm)

    def to_dict(self) -> dict:
        return {
            "name":   self._name,
            "qty":    self._qty_spin.value(),
            "weight": self._weight,
            "notes":  self._notes,
        }


# ── Main dialog ───────────────────────────────────────────────────────────────

class ItemPickerDialog(QDialog):
    """Browse the item catalog across tabs, build a cart, then save all at once."""
    items_chosen = pyqtSignal(list)   # list of {name, qty, weight, notes}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Browse & Add Items")
        self.setMinimumSize(660, 680)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")
        self._cart_rows: list[CartRow] = []
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(8)

        root.addWidget(_lbl("BROWSE  ITEMS", COLOR_TEXT_HEADER, FONT_HEADER, 15,
                             bold=True, align=Qt.AlignmentFlag.AlignCenter))

        # Search
        search_row = QHBoxLayout()
        search_row.addWidget(_lbl("Search:", COLOR_TEXT_HEADER, FONT_BODY, 10))
        self._search = QLineEdit()
        self._search.setPlaceholderText("Type to filter items…")
        self._search.setFixedHeight(28)
        self._search.setStyleSheet(_SEARCH_CSS)
        self._search.textChanged.connect(self._on_search)
        search_row.addWidget(self._search, 1)
        root.addLayout(search_row)

        root.addWidget(_rule())

        # Item tabs
        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(_TAB_CSS)
        self._lists: dict[str, QListWidget] = {}

        for cat_name, items in CATEGORIES:
            lst = QListWidget()
            lst.setStyleSheet(_LIST_CSS)
            lst.itemDoubleClicked.connect(self._on_double_click)
            for name, weight, notes in items:
                li = QListWidgetItem(f"{name}  —  {notes}")
                li.setData(Qt.ItemDataRole.UserRole, (name, weight, notes))
                lst.addItem(li)
            self._lists[cat_name] = lst
            tab = QWidget()
            tab.setStyleSheet(f"background:{COLOR_PARCHMENT};")
            tlo = QVBoxLayout(tab)
            tlo.setContentsMargins(4, 4, 4, 4)
            tlo.addWidget(lst)
            self._tabs.addTab(tab, cat_name)

        root.addWidget(self._tabs, 3)

        # Qty row + "Add to Cart" button
        pick_row = QHBoxLayout()
        pick_row.addWidget(_lbl("Qty:", COLOR_TEXT_HEADER, FONT_BODY, 10))
        self._qty = QSpinBox()
        self._qty.setRange(1, 9999)
        self._qty.setValue(1)
        self._qty.setFixedSize(62, 30)
        self._qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._qty.setStyleSheet(_QTY_CSS)
        pick_row.addWidget(self._qty)
        pick_row.addWidget(
            _lbl("Select an item above, set qty, then click Add to Cart  (or double-click to add qty 1)",
                 COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True), 1
        )

        add_btn = QPushButton("＋  Add to Cart")
        add_btn.setFixedHeight(30)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:5px;"
            f"font-family:{FONT_HEADER};font-size:10pt;font-weight:bold;padding:0 14px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
        )
        add_btn.clicked.connect(self._on_add_to_cart)
        pick_row.addWidget(add_btn)
        root.addLayout(pick_row)

        root.addWidget(_rule())

        # Cart header
        cart_hdr = QHBoxLayout()
        cart_hdr.addWidget(_lbl("SELECTED ITEMS", COLOR_TEXT_HEADER, FONT_BODY, 9, bold=True))
        cart_hdr.addStretch()
        self._count_lbl = _lbl("Nothing selected yet", COLOR_TEXT_SUBTEXT, FONT_BODY, 8,
                                italic=True, align=Qt.AlignmentFlag.AlignRight)
        cart_hdr.addWidget(self._count_lbl)
        root.addLayout(cart_hdr)

        # Cart scroll area
        cart_scroll = QScrollArea()
        cart_scroll.setWidgetResizable(True)
        cart_scroll.setFixedHeight(150)
        cart_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        cart_scroll.setStyleSheet(
            f"QScrollArea{{border:1px solid {COLOR_SECTION_BORDER};"
            f"border-radius:4px;background:{COLOR_PARCHMENT_DARK};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT_DARK};}}"
        )

        self._cart_inner = QWidget()
        self._cart_inner.setStyleSheet(f"background:{COLOR_PARCHMENT_DARK};")
        self._cart_layout = QVBoxLayout(self._cart_inner)
        self._cart_layout.setContentsMargins(6, 4, 6, 4)
        self._cart_layout.setSpacing(2)

        self._empty_lbl = _lbl(
            "Your cart is empty — select items above and click  ＋ Add to Cart",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 8, italic=True,
            align=Qt.AlignmentFlag.AlignCenter,
        )
        self._cart_layout.addWidget(self._empty_lbl)
        self._cart_layout.addStretch()

        cart_scroll.setWidget(self._cart_inner)
        root.addWidget(cart_scroll)

        root.addWidget(_rule())

        # Bottom buttons
        btn_row = QHBoxLayout()
        cancel = QPushButton("Cancel")
        cancel.setFixedHeight(34)
        cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 16px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        btn_row.addStretch()

        self._save_btn = QPushButton("✔  Add to Equipment")
        self._save_btn.setFixedHeight(34)
        self._save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_btn.setEnabled(False)
        self._save_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:6px;"
            f"font-family:{FONT_HEADER};font-size:11pt;font-weight:bold;padding:0 20px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
            f"QPushButton:disabled{{background:#5A3030;color:#A08080;"
            f"border-color:#8B6060;}}"
        )
        self._save_btn.clicked.connect(self._on_save)
        btn_row.addWidget(self._save_btn)
        root.addLayout(btn_row)

    # ── Search ────────────────────────────────────────────────────────────────

    def _on_search(self, text: str):
        text = text.strip().lower()
        for lst in self._lists.values():
            for i in range(lst.count()):
                item = lst.item(i)
                name, _, _ = item.data(Qt.ItemDataRole.UserRole)
                item.setHidden(bool(text) and text not in name.lower())

    # ── Cart management ───────────────────────────────────────────────────────

    def _current_item_data(self) -> tuple | None:
        lst = self._tabs.currentWidget().layout().itemAt(0).widget()
        selected = lst.selectedItems()
        if not selected:
            return None
        return selected[0].data(Qt.ItemDataRole.UserRole)

    def _on_double_click(self, list_item: QListWidgetItem):
        data = list_item.data(Qt.ItemDataRole.UserRole)
        if data:
            name, weight, notes = data
            self._add_to_cart(name, weight, notes, qty=1)

    def _on_add_to_cart(self):
        data = self._current_item_data()
        if not data:
            return
        name, weight, notes = data
        self._add_to_cart(name, weight, notes, qty=self._qty.value())
        self._qty.setValue(1)

    def _add_to_cart(self, name: str, weight: float, notes: str, qty: int):
        # If the item is already in the cart, just bump its qty
        for row in self._cart_rows:
            if row._name == name:
                row._qty_spin.setValue(row._qty_spin.value() + qty)
                self._refresh_cart_state()
                return

        row = CartRow(name, weight, notes, qty)
        row.remove_requested.connect(self._remove_cart_row)
        self._cart_rows.append(row)
        # Insert before the trailing stretch
        self._cart_layout.insertWidget(self._cart_layout.count() - 1, row)
        self._refresh_cart_state()

    def _remove_cart_row(self, row: CartRow):
        self._cart_layout.removeWidget(row)
        row.deleteLater()
        self._cart_rows.remove(row)
        self._refresh_cart_state()

    def _refresh_cart_state(self):
        n = len(self._cart_rows)
        self._empty_lbl.setVisible(n == 0)
        self._save_btn.setEnabled(n > 0)
        if n == 0:
            self._count_lbl.setText("Nothing selected yet")
        else:
            total = sum(r.to_dict()["qty"] * r._weight for r in self._cart_rows)
            self._count_lbl.setText(
                f"{n} item type{'s' if n != 1 else ''}  ·  {total:.1f} lb total"
            )

    # ── Save ──────────────────────────────────────────────────────────────────

    def _on_save(self):
        if not self._cart_rows:
            return
        self.items_chosen.emit([r.to_dict() for r in self._cart_rows])
        self.accept()
