import random

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QPushButton, QWidget,
    QScrollArea, QCheckBox, QButtonGroup,
    QRadioButton, QTabWidget,
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

# ── Starting gold: (num_dice, die_sides, multiplier) ─────────────────────────
STARTING_GOLD: dict[str, tuple[int, int, int]] = {
    "Barbarian": (2, 4, 10),
    "Bard":      (5, 4, 10),
    "Cleric":    (5, 4, 10),
    "Druid":     (2, 4, 10),
    "Fighter":   (5, 4, 10),
    "Monk":      (5, 4,  1),
    "Paladin":   (5, 4, 10),
    "Ranger":    (5, 4, 10),
    "Rogue":     (4, 4, 10),
    "Sorcerer":  (3, 4, 10),
    "Warlock":   (4, 4, 10),
    "Wizard":    (4, 4, 10),
    "Artificer": (5, 4, 10),
}

# ── Standard class equipment (typical first choice) ──────────────────────────
# Each item: {name, qty, weight, notes}
CLASS_EQUIPMENT: dict[str, list[dict]] = {
    "Barbarian": [
        {"name": "Greataxe",        "qty": 1, "weight": 7.0,  "notes": "1d12 slashing, heavy, two-handed"},
        {"name": "Handaxe",         "qty": 2, "weight": 2.0,  "notes": "1d6 slashing, light, thrown 20/60"},
        {"name": "Explorer's Pack", "qty": 1, "weight": 59.0, "notes": "Bedroll, mess kit, tinderbox, 10 torches, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Javelin",         "qty": 4, "weight": 2.0,  "notes": "1d6 piercing, thrown 30/120"},
    ],
    "Bard": [
        {"name": "Rapier",              "qty": 1, "weight": 2.0,  "notes": "1d8 piercing, finesse"},
        {"name": "Diplomat's Pack",     "qty": 1, "weight": 36.0, "notes": "Chest, 2 cases for maps, fine clothes, bottle of ink, quill, small knife, perfume, wax, 5 sheets parchment"},
        {"name": "Lute",                "qty": 1, "weight": 2.0,  "notes": "Musical instrument"},
        {"name": "Leather Armor",       "qty": 1, "weight": 10.0, "notes": "AC 11 + DEX mod"},
        {"name": "Dagger",              "qty": 1, "weight": 1.0,  "notes": "1d4 piercing, finesse, light, thrown 20/60"},
    ],
    "Cleric": [
        {"name": "Mace",            "qty": 1, "weight": 4.0,  "notes": "1d6 bludgeoning"},
        {"name": "Scale Mail",      "qty": 1, "weight": 45.0, "notes": "AC 14 + DEX mod (max 2), disadvantage on Stealth"},
        {"name": "Light Crossbow",  "qty": 1, "weight": 5.0,  "notes": "1d8 piercing, loading, range 80/320, two-handed"},
        {"name": "Crossbow Bolt",   "qty": 20,"weight": 1.5,  "notes": "Ammunition for light crossbow"},
        {"name": "Priest's Pack",   "qty": 1, "weight": 24.0, "notes": "Backpack, blanket, 10 candles, tinderbox, alms box, 2 blocks incense, censer, vestments, 2 days rations, waterskin"},
        {"name": "Shield",          "qty": 1, "weight": 6.0,  "notes": "+2 AC"},
        {"name": "Holy Symbol",     "qty": 1, "weight": 1.0,  "notes": "Spellcasting focus"},
    ],
    "Druid": [
        {"name": "Wooden Shield",   "qty": 1, "weight": 6.0,  "notes": "+2 AC"},
        {"name": "Scimitar",        "qty": 1, "weight": 3.0,  "notes": "1d6 slashing, finesse, light"},
        {"name": "Leather Armor",   "qty": 1, "weight": 10.0, "notes": "AC 11 + DEX mod"},
        {"name": "Explorer's Pack", "qty": 1, "weight": 59.0, "notes": "Bedroll, mess kit, tinderbox, 10 torches, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Druidic Focus",   "qty": 1, "weight": 1.0,  "notes": "Sprig of mistletoe / wooden staff / yew wand"},
    ],
    "Fighter": [
        {"name": "Chain Mail",      "qty": 1, "weight": 55.0, "notes": "AC 16, disadvantage on Stealth, STR 13 required"},
        {"name": "Longsword",       "qty": 1, "weight": 3.0,  "notes": "1d8 slashing (1d10 two-handed), versatile"},
        {"name": "Shield",          "qty": 1, "weight": 6.0,  "notes": "+2 AC"},
        {"name": "Light Crossbow",  "qty": 1, "weight": 5.0,  "notes": "1d8 piercing, loading, range 80/320, two-handed"},
        {"name": "Crossbow Bolt",   "qty": 20,"weight": 1.5,  "notes": "Ammunition for light crossbow"},
        {"name": "Dungeoneer's Pack","qty": 1, "weight": 61.5,"notes": "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft rope"},
    ],
    "Monk": [
        {"name": "Shortsword",      "qty": 1, "weight": 2.0,  "notes": "1d6 piercing, finesse, light"},
        {"name": "Dungeoneer's Pack","qty": 1, "weight": 61.5,"notes": "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Dart",            "qty": 10,"weight": 0.25, "notes": "1d4 piercing, finesse, thrown 20/60"},
    ],
    "Paladin": [
        {"name": "Longsword",       "qty": 1, "weight": 3.0,  "notes": "1d8 slashing (1d10 two-handed), versatile"},
        {"name": "Shield",          "qty": 1, "weight": 6.0,  "notes": "+2 AC"},
        {"name": "Javelin",         "qty": 5, "weight": 2.0,  "notes": "1d6 piercing, thrown 30/120"},
        {"name": "Priest's Pack",   "qty": 1, "weight": 24.0, "notes": "Backpack, blanket, 10 candles, tinderbox, alms box, incense, censer, vestments, 2 days rations, waterskin"},
        {"name": "Chain Mail",      "qty": 1, "weight": 55.0, "notes": "AC 16, disadvantage on Stealth, STR 13 required"},
        {"name": "Holy Symbol",     "qty": 1, "weight": 1.0,  "notes": "Spellcasting focus"},
    ],
    "Ranger": [
        {"name": "Scale Mail",      "qty": 1, "weight": 45.0, "notes": "AC 14 + DEX mod (max 2), disadvantage on Stealth"},
        {"name": "Shortsword",      "qty": 2, "weight": 2.0,  "notes": "1d6 piercing, finesse, light"},
        {"name": "Dungeoneer's Pack","qty": 1, "weight": 61.5,"notes": "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Longbow",         "qty": 1, "weight": 2.0,  "notes": "1d8 piercing, heavy, range 150/600, two-handed"},
        {"name": "Arrow",           "qty": 20,"weight": 1.0,  "notes": "Ammunition for longbow"},
    ],
    "Rogue": [
        {"name": "Rapier",          "qty": 1, "weight": 2.0,  "notes": "1d8 piercing, finesse"},
        {"name": "Shortbow",        "qty": 1, "weight": 2.0,  "notes": "1d6 piercing, range 80/320, two-handed"},
        {"name": "Arrow",           "qty": 20,"weight": 1.0,  "notes": "Ammunition for shortbow"},
        {"name": "Burglar's Pack",  "qty": 1, "weight": 47.5, "notes": "Backpack, 1000 ball bearings, 10 ft string, bell, 5 candles, crowbar, hammer, 10 pitons, hooded lantern, 2 flasks oil, 5 days rations, tinderbox, waterskin"},
        {"name": "Leather Armor",   "qty": 1, "weight": 10.0, "notes": "AC 11 + DEX mod"},
        {"name": "Dagger",          "qty": 2, "weight": 1.0,  "notes": "1d4 piercing, finesse, light, thrown 20/60"},
        {"name": "Thieves' Tools",  "qty": 1, "weight": 1.0,  "notes": "Pick locks, disarm traps"},
    ],
    "Sorcerer": [
        {"name": "Light Crossbow",  "qty": 1, "weight": 5.0,  "notes": "1d8 piercing, loading, range 80/320, two-handed"},
        {"name": "Crossbow Bolt",   "qty": 20,"weight": 1.5,  "notes": "Ammunition for light crossbow"},
        {"name": "Arcane Focus",    "qty": 1, "weight": 1.0,  "notes": "Crystal / orb / rod / staff / wand"},
        {"name": "Dungeoneer's Pack","qty": 1, "weight": 61.5,"notes": "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Dagger",          "qty": 2, "weight": 1.0,  "notes": "1d4 piercing, finesse, light, thrown 20/60"},
    ],
    "Warlock": [
        {"name": "Light Crossbow",  "qty": 1, "weight": 5.0,  "notes": "1d8 piercing, loading, range 80/320, two-handed"},
        {"name": "Crossbow Bolt",   "qty": 20,"weight": 1.5,  "notes": "Ammunition for light crossbow"},
        {"name": "Arcane Focus",    "qty": 1, "weight": 1.0,  "notes": "Crystal / orb / rod / staff / wand"},
        {"name": "Scholar's Pack",  "qty": 1, "weight": 10.0, "notes": "Backpack, book of lore, bottle of ink, ink pen, 10 sheets parchment, little bag of sand, small knife"},
        {"name": "Leather Armor",   "qty": 1, "weight": 10.0, "notes": "AC 11 + DEX mod"},
        {"name": "Dagger",          "qty": 2, "weight": 1.0,  "notes": "1d4 piercing, finesse, light, thrown 20/60"},
    ],
    "Wizard": [
        {"name": "Quarterstaff",    "qty": 1, "weight": 4.0,  "notes": "1d6 bludgeoning (1d8 two-handed), versatile"},
        {"name": "Arcane Focus",    "qty": 1, "weight": 1.0,  "notes": "Crystal / orb / rod / staff / wand"},
        {"name": "Scholar's Pack",  "qty": 1, "weight": 10.0, "notes": "Backpack, book of lore, bottle of ink, ink pen, 10 sheets parchment, little bag of sand, small knife"},
        {"name": "Spellbook",       "qty": 1, "weight": 3.0,  "notes": "Contains 6 1st-level spells"},
    ],
    "Artificer": [
        {"name": "Any Simple Weapon","qty": 2, "weight": 2.0, "notes": "Two simple weapons of your choice"},
        {"name": "Light Crossbow",  "qty": 1, "weight": 5.0,  "notes": "1d8 piercing, loading, range 80/320, two-handed"},
        {"name": "Crossbow Bolt",   "qty": 20,"weight": 1.5,  "notes": "Ammunition for light crossbow"},
        {"name": "Dungeoneer's Pack","qty": 1, "weight": 61.5,"notes": "Backpack, crowbar, hammer, 10 pitons, 10 torches, tinderbox, 10 days rations, waterskin, 50 ft rope"},
        {"name": "Leather Armor",   "qty": 1, "weight": 10.0, "notes": "AC 11 + DEX mod"},
        {"name": "Thieves' Tools",  "qty": 1, "weight": 1.0,  "notes": "Required for infusions"},
        {"name": "Tinker's Tools",  "qty": 1, "weight": 10.0, "notes": "Required for infusions"},
    ],
}

# ── Background equipment + bonus gold ────────────────────────────────────────
BACKGROUND_EQUIPMENT: dict[str, tuple[list[dict], int]] = {
    # (items, bonus_gp)
    "Acolyte":       ([
        {"name": "Holy Symbol",     "qty": 1, "weight": 1.0, "notes": "A gift to you when you entered the priesthood"},
        {"name": "Prayer Book",     "qty": 1, "weight": 1.0, "notes": ""},
        {"name": "Incense",         "qty": 5, "weight": 0.0, "notes": "Sticks of incense"},
        {"name": "Vestments",       "qty": 1, "weight": 4.0, "notes": ""},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 15),
    "Charlatan":     ([
        {"name": "Fine Clothes",    "qty": 1, "weight": 6.0, "notes": ""},
        {"name": "Disguise Kit",    "qty": 1, "weight": 3.0, "notes": ""},
        {"name": "Con Tools",       "qty": 1, "weight": 0.5, "notes": "e.g. weighted dice, marked cards"},
    ], 15),
    "Criminal":      ([
        {"name": "Crowbar",         "qty": 1, "weight": 5.0, "notes": ""},
        {"name": "Dark Common Clothes","qty":1,"weight": 3.0,"notes": "Includes a hood"},
    ], 15),
    "Entertainer":   ([
        {"name": "Musical Instrument","qty":1,"weight": 2.0, "notes": "One of your choice"},
        {"name": "Costume",         "qty": 1, "weight": 4.0, "notes": ""},
    ], 15),
    "Folk Hero":     ([
        {"name": "Artisan's Tools", "qty": 1, "weight": 5.0, "notes": "One type of your choice"},
        {"name": "Shovel",          "qty": 1, "weight": 5.0, "notes": ""},
        {"name": "Iron Pot",        "qty": 1, "weight": 10.0,"notes": ""},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 10),
    "Guild Artisan": ([
        {"name": "Artisan's Tools", "qty": 1, "weight": 5.0, "notes": "One type related to your guild"},
        {"name": "Letter of Introduction","qty":1,"weight":0.0,"notes": "From your guild"},
        {"name": "Traveler's Clothes","qty":1,"weight": 4.0, "notes": ""},
    ], 15),
    "Hermit":        ([
        {"name": "Scroll Case",     "qty": 1, "weight": 1.0, "notes": "Stuffed full of notes from your studies"},
        {"name": "Winter Blanket",  "qty": 1, "weight": 3.0, "notes": ""},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
        {"name": "Herbalism Kit",   "qty": 1, "weight": 3.0, "notes": ""},
    ], 5),
    "Noble":         ([
        {"name": "Fine Clothes",    "qty": 1, "weight": 6.0, "notes": ""},
        {"name": "Signet Ring",     "qty": 1, "weight": 0.0, "notes": ""},
        {"name": "Scroll of Pedigree","qty":1,"weight": 0.0, "notes": ""},
    ], 25),
    "Outlander":     ([
        {"name": "Staff",           "qty": 1, "weight": 4.0, "notes": ""},
        {"name": "Hunting Trap",    "qty": 1, "weight": 25.0,"notes": ""},
        {"name": "Traveler's Clothes","qty":1,"weight": 4.0, "notes": ""},
    ], 10),
    "Sage":          ([
        {"name": "Bottle of Black Ink","qty":1,"weight":0.0, "notes": ""},
        {"name": "Quill",           "qty": 1, "weight": 0.0, "notes": ""},
        {"name": "Small Knife",     "qty": 1, "weight": 0.5, "notes": ""},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 10),
    "Sailor":        ([
        {"name": "Belaying Pin",    "qty": 1, "weight": 2.0, "notes": "Club, 1d4 bludgeoning"},
        {"name": "Silk Rope",       "qty": 1, "weight": 5.0, "notes": "50 ft"},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 10),
    "Soldier":       ([
        {"name": "Rank Insignia",   "qty": 1, "weight": 0.0, "notes": ""},
        {"name": "Trophy",          "qty": 1, "weight": 0.0, "notes": "From a fallen enemy"},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 10),
    "Urchin":        ([
        {"name": "Small Knife",     "qty": 1, "weight": 0.5, "notes": ""},
        {"name": "City Map",        "qty": 1, "weight": 0.0, "notes": "Map of the city you grew up in"},
        {"name": "Common Clothes",  "qty": 1, "weight": 3.0, "notes": ""},
    ], 10),
}


def _roll_gold(cls: str) -> tuple[int, int]:
    """Returns (rolled_gp, average_gp)."""
    n, d, mult = STARTING_GOLD.get(cls, (5, 4, 10))
    rolled = sum(random.randint(1, d) for _ in range(n)) * mult
    avg    = round((n * (d + 1) / 2) * mult)
    return rolled, avg


# ── Helpers ───────────────────────────────────────────────────────────────────

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


_CHECK_CSS = (
    f"QCheckBox{{color:{COLOR_TEXT_PRIMARY};font-family:{FONT_BODY};"
    f"font-size:9pt;background:transparent;spacing:6px;}}"
    f"QCheckBox::indicator{{width:14px;height:14px;"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:3px;"
    f"background:{COLOR_PARCHMENT_DARK};}}"
    f"QCheckBox::indicator:checked{{background:{COLOR_BADGE_BG};"
    f"border-color:{COLOR_GOLD_RULE};}}"
)

_RADIO_CSS = (
    f"QRadioButton{{color:{COLOR_TEXT_PRIMARY};font-family:{FONT_BODY};"
    f"font-size:10pt;background:transparent;spacing:8px;}}"
    f"QRadioButton::indicator{{width:14px;height:14px;"
    f"border:2px solid {COLOR_SECTION_BORDER};border-radius:7px;"
    f"background:{COLOR_PARCHMENT_DARK};}}"
    f"QRadioButton::indicator:checked{{background:{COLOR_BADGE_BG};"
    f"border-color:{COLOR_GOLD_RULE};}}"
)


class StartingEquipmentDialog(QDialog):
    """
    Emits equipment_chosen(items: list[dict], gold_gp: int).
    The caller merges this into the existing equipment section.
    """
    equipment_chosen = pyqtSignal(list, int)   # items list, gold gp to add

    def __init__(self, char_data: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Apply Starting Equipment")
        self.setMinimumSize(560, 620)
        self.setModal(True)
        self.setStyleSheet(f"QDialog{{background:{COLOR_PARCHMENT};}}")

        info = char_data.get("character_info", {})
        self._cls  = info.get("class", "")
        self._bg   = info.get("background", "")
        self._item_checks: list[tuple[QCheckBox, dict]] = []
        self._gold_gp = 0

        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 18, 24, 16)
        root.setSpacing(10)

        root.addWidget(_lbl("⚔  STARTING  EQUIPMENT", COLOR_TEXT_HEADER,
                             FONT_HEADER, 15, bold=True,
                             align=Qt.AlignmentFlag.AlignCenter))

        if not self._cls:
            root.addWidget(_lbl(
                "Set your class in Section 1 first.",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 10, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))
            root.addStretch()
            close = self._mk_btn("Close", secondary=True)
            close.clicked.connect(self.reject)
            root.addWidget(close)
            return

        # Method selector
        method_card = QWidget()
        method_card.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
        )
        mc = QVBoxLayout(method_card)
        mc.setContentsMargins(14, 10, 14, 10)
        mc.setSpacing(8)
        mc.addWidget(_lbl("Choose a starting method:", COLOR_TEXT_HEADER,
                           FONT_BODY, 10, bold=True))

        self._radio_standard = QRadioButton("Standard equipment package  (pre-selected items below)")
        self._radio_gold     = QRadioButton(f"Roll for starting gold  (buy your own gear)")
        self._radio_standard.setChecked(True)
        self._radio_standard.setStyleSheet(_RADIO_CSS)
        self._radio_gold.setStyleSheet(_RADIO_CSS)
        self._radio_standard.toggled.connect(self._on_method_changed)
        mc.addWidget(self._radio_standard)
        mc.addWidget(self._radio_gold)
        root.addWidget(method_card)

        root.addWidget(_rule())

        # Stacked content — standard tab vs gold tab
        self._standard_widget = self._build_standard_panel()
        self._gold_widget      = self._build_gold_panel()
        root.addWidget(self._standard_widget, 1)
        root.addWidget(self._gold_widget, 1)
        self._gold_widget.hide()

        root.addWidget(_rule())

        btn_row = QHBoxLayout()
        cancel = self._mk_btn("Cancel", secondary=True)
        cancel.clicked.connect(self.reject)
        btn_row.addWidget(cancel)
        btn_row.addStretch()
        self._apply_btn = self._mk_btn("Apply to Character", secondary=False)
        self._apply_btn.clicked.connect(self._on_apply)
        btn_row.addWidget(self._apply_btn)
        root.addLayout(btn_row)

    # ── Standard panel ────────────────────────────────────────────────────────

    def _build_standard_panel(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(6)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea{{border:1px solid {COLOR_SECTION_BORDER};"
            f"border-radius:4px;background:{COLOR_PARCHMENT};}}"
            f"QScrollArea>QWidget>QWidget{{background:{COLOR_PARCHMENT};}}"
        )
        inner = QWidget()
        inner.setStyleSheet(f"background:{COLOR_PARCHMENT};")
        inner_lo = QVBoxLayout(inner)
        inner_lo.setContentsMargins(10, 8, 10, 8)
        inner_lo.setSpacing(4)

        cls_items = CLASS_EQUIPMENT.get(self._cls, [])
        bg_items, bg_gold = BACKGROUND_EQUIPMENT.get(self._bg, ([], 0))

        if cls_items:
            inner_lo.addWidget(_lbl(f"{self._cls} Equipment", COLOR_TEXT_HEADER,
                                     FONT_HEADER, 10, bold=True))
            for item in cls_items:
                self._add_check(inner_lo, item)
            inner_lo.addSpacing(6)

        if bg_items:
            inner_lo.addWidget(_rule())
            inner_lo.addSpacing(4)
            inner_lo.addWidget(_lbl(f"{self._bg} Background Equipment",
                                     COLOR_TEXT_HEADER, FONT_HEADER, 10, bold=True))
            for item in bg_items:
                self._add_check(inner_lo, item)
            if bg_gold:
                inner_lo.addWidget(_lbl(
                    f"+ {bg_gold} gp background money (added to your purse)",
                    COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
                ))
                self._bg_gold = bg_gold
            else:
                self._bg_gold = 0
        else:
            self._bg_gold = 0

        if not cls_items and not bg_items:
            inner_lo.addWidget(_lbl(
                "No standard equipment defined for this class/background combination.",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
            ))

        inner_lo.addStretch()
        scroll.setWidget(inner)
        lo.addWidget(scroll)

        sel_row = QHBoxLayout()
        sel_all = self._small_btn("Select All")
        sel_all.clicked.connect(lambda: [cb.setChecked(True) for cb, _ in self._item_checks])
        sel_none = self._small_btn("Select None")
        sel_none.clicked.connect(lambda: [cb.setChecked(False) for cb, _ in self._item_checks])
        sel_row.addWidget(sel_all)
        sel_row.addWidget(sel_none)
        sel_row.addStretch()
        lo.addLayout(sel_row)
        return w

    def _add_check(self, layout: QVBoxLayout, item: dict):
        weight_txt = f"{item['weight']} lb  " if item['weight'] else ""
        notes_txt  = f"— {item['notes']}" if item['notes'] else ""
        qty_txt    = f"×{item['qty']}  " if item['qty'] > 1 else ""
        label = f"{qty_txt}{item['name']}  {weight_txt}{notes_txt}"
        cb = QCheckBox(label)
        cb.setChecked(True)
        cb.setStyleSheet(_CHECK_CSS)
        self._item_checks.append((cb, item))
        layout.addWidget(cb)

    # ── Gold panel ────────────────────────────────────────────────────────────

    def _build_gold_panel(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lo = QVBoxLayout(w)
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(12)

        n, d, mult = STARTING_GOLD.get(self._cls, (5, 4, 10))
        avg = round((n * (d + 1) / 2) * mult)
        dice_txt = f"{n}d{d}" + (f" × {mult}" if mult > 1 else "")

        card = QWidget()
        card.setStyleSheet(
            f"background:{COLOR_PARCHMENT_DARK};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:8px;"
        )
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 16, 20, 16)
        cl.setSpacing(10)

        cl.addWidget(_lbl(f"{self._cls} Starting Gold: {dice_txt} gp",
                           COLOR_TEXT_HEADER, FONT_HEADER, 12, bold=True,
                           align=Qt.AlignmentFlag.AlignCenter))

        self._gold_result_lbl = _lbl(
            f"Average: {avg} gp",
            COLOR_TEXT_HEADER, FONT_HEADER, 22, bold=True,
            align=Qt.AlignmentFlag.AlignCenter,
        )
        self._gold_gp = avg
        cl.addWidget(self._gold_result_lbl)

        cl.addWidget(_lbl(
            f"Click Roll to randomise, or use the average ({avg} gp).",
            COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
            align=Qt.AlignmentFlag.AlignCenter,
        ))

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        roll_btn = QPushButton(f"🎲  Roll {dice_txt}")
        roll_btn.setFixedHeight(36)
        roll_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        roll_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_BADGE_BG};color:{COLOR_BADGE_TEXT};"
            f"border:2px solid {COLOR_GOLD_RULE};border-radius:6px;"
            f"font-family:{FONT_HEADER};font-size:11pt;font-weight:bold;padding:0 20px;}}"
            f"QPushButton:hover{{background:#A02020;}}"
        )
        roll_btn.clicked.connect(lambda: self._do_roll(n, d, mult))

        avg_btn = QPushButton(f"Take Average ({avg} gp)")
        avg_btn.setFixedHeight(36)
        avg_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        avg_btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT};color:{COLOR_TEXT_HEADER};"
            f"border:2px solid {COLOR_SECTION_BORDER};border-radius:6px;"
            f"font-family:{FONT_BODY};font-size:10pt;padding:0 16px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        avg_btn.clicked.connect(lambda: self._set_gold(avg))

        btn_row.addStretch()
        btn_row.addWidget(roll_btn)
        btn_row.addWidget(avg_btn)
        btn_row.addStretch()
        cl.addLayout(btn_row)

        # Background bonus gold
        _, bg_gold = BACKGROUND_EQUIPMENT.get(self._bg, ([], 0))
        self._bg_gold = bg_gold
        if bg_gold:
            cl.addWidget(_lbl(
                f"+ {bg_gold} gp from {self._bg} background  (added automatically)",
                COLOR_TEXT_SUBTEXT, FONT_BODY, 9, italic=True,
                align=Qt.AlignmentFlag.AlignCenter,
            ))

        lo.addWidget(card)
        lo.addStretch()
        return w

    def _do_roll(self, n: int, d: int, mult: int):
        result = sum(random.randint(1, d) for _ in range(n)) * mult
        self._set_gold(result)

    def _set_gold(self, gp: int):
        self._gold_gp = gp
        self._gold_result_lbl.setText(f"{gp} gp")

    # ── Method toggle ─────────────────────────────────────────────────────────

    def _on_method_changed(self, standard: bool):
        self._standard_widget.setVisible(standard)
        self._gold_widget.setVisible(not standard)

    # ── Apply ─────────────────────────────────────────────────────────────────

    def _on_apply(self):
        if self._radio_standard.isChecked():
            items = [item for cb, item in self._item_checks if cb.isChecked()]
            gold  = self._bg_gold
        else:
            items = []
            gold  = self._gold_gp + self._bg_gold
        self.equipment_chosen.emit(items, gold)
        self.accept()

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _small_btn(label: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setFixedHeight(26)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            f"QPushButton{{background:{COLOR_PARCHMENT_DARK};color:{COLOR_TEXT_HEADER};"
            f"border:1px solid {COLOR_SECTION_BORDER};border-radius:4px;"
            f"font-family:{FONT_BODY};font-size:9pt;padding:0 10px;}}"
            f"QPushButton:hover{{background:{COLOR_PARCHMENT_HOVER};}}"
        )
        return btn

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
