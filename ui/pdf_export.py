"""
PDF export — generates a two-page D&D 5e character sheet.
Page 1: core stats, combat, skills, attacks, equipment, personality
Page 2: features & traits, proficiencies & languages
"""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Palette — matches the parchment theme
# ---------------------------------------------------------------------------
C_PARCHMENT  = colors.HexColor("#F5E6C8")
C_DARK       = colors.HexColor("#E8D5A0")
C_BORDER     = colors.HexColor("#8B4513")
C_HEADER     = colors.HexColor("#2C1810")
C_TEXT       = colors.HexColor("#1A0A00")
C_SUBTEXT    = colors.HexColor("#6B4226")
C_GOLD       = colors.HexColor("#C8A84B")
C_RED        = colors.HexColor("#8B0000")
C_WHITE      = colors.white

PW, PH = LETTER   # 612 × 792 pts
MARGIN = 0.35 * inch


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _mod(score: int) -> int:
    return (score - 10) // 2


def _fmt_mod(val: int) -> str:
    return f"+{val}" if val >= 0 else str(val)


def _wrap_text(text: str, max_chars: int) -> list[str]:
    """Naive word-wrap to a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip() if cur else w
    if cur:
        lines.append(cur)
    return lines or [""]


# ---------------------------------------------------------------------------
# Low-level drawing primitives
# ---------------------------------------------------------------------------
class Sheet:
    def __init__(self, c: rl_canvas.Canvas):
        self.c = c

    # ── background
    def fill_bg(self):
        self.c.setFillColor(C_PARCHMENT)
        self.c.rect(0, 0, PW, PH, fill=1, stroke=0)

    # ── ruled box
    def box(self, x, y, w, h, fill=None, stroke=C_BORDER, lw=0.8):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill or C_PARCHMENT)
        self.c.rect(x, y, w, h, fill=1 if fill else 0, stroke=1)

    # ── rounded box
    def rbox(self, x, y, w, h, r=4, fill=C_DARK, stroke=C_BORDER, lw=0.8):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill)
        self.c.roundRect(x, y, w, h, r, fill=1, stroke=1)

    # ── circle
    def circle(self, cx, cy, r, fill=C_WHITE, stroke=C_BORDER, lw=0.8):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill)
        self.c.circle(cx, cy, r, fill=1, stroke=1)

    # ── diamond (for AC)
    def diamond(self, cx, cy, hw, hh, fill=C_WHITE, stroke=C_BORDER, lw=1.0):
        p = self.c.beginPath()
        p.moveTo(cx, cy + hh)
        p.lineTo(cx + hw, cy)
        p.lineTo(cx, cy - hh)
        p.lineTo(cx - hw, cy)
        p.close()
        self.c.setFillColor(fill)
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.drawPath(p, fill=1, stroke=1)

    # ── horizontal rule
    def hrule(self, x, y, w, color=C_GOLD, lw=1.0):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(lw)
        self.c.line(x, y, x + w, y)

    # ── text helpers
    def text(self, x, y, s, size=8, color=C_TEXT, bold=False, align="left"):
        self.c.setFillColor(color)
        fn = "Helvetica-Bold" if bold else "Helvetica"
        self.c.setFont(fn, size)
        if align == "center":
            self.c.drawCentredString(x, y, str(s))
        elif align == "right":
            self.c.drawRightString(x, y, str(s))
        else:
            self.c.drawString(x, y, str(s))

    def label_above(self, cx, y_bottom, lbl, size=6, color=C_SUBTEXT):
        """Small label drawn above a field."""
        self.text(cx, y_bottom, lbl, size=size, color=color, align="center")

    def label_below(self, cx, y_top, lbl, size=6, color=C_SUBTEXT):
        """Small label drawn below a field."""
        self.text(cx, y_top - 7, lbl, size=size, color=color, align="center")


# ---------------------------------------------------------------------------
# Section header banner
# ---------------------------------------------------------------------------
def _section_header(s: Sheet, x, y, w, title: str, h=13):
    s.c.setFillColor(C_RED)
    s.c.setStrokeColor(C_RED)
    s.c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    s.text(x + w / 2, y + 3, title.upper(), size=7, color=C_WHITE,
           bold=True, align="center")


# ---------------------------------------------------------------------------
# Page 1
# ---------------------------------------------------------------------------
def _draw_page1(s: Sheet, d: dict):
    s.fill_bg()

    info    = d.get("character_info", {})
    scores  = d.get("ability_scores", {})
    throws  = d.get("saving_throws", {})
    skills  = d.get("skills", {})
    combat  = d.get("combat_stats", {})
    attacks = d.get("attacks_spells", {})
    equip   = d.get("equipment", {})
    pers    = d.get("personality", {})

    _header_block(s, info)
    _ability_block(s, scores, throws)
    _skills_block(s, skills, scores)
    _combat_block(s, combat, info)
    _attacks_block(s, attacks)
    _equipment_block(s, equip)
    _personality_block(s, pers, info)

    # page footer
    s.hrule(MARGIN, 0.22 * inch, PW - 2 * MARGIN, lw=0.5)
    s.text(PW / 2, 0.10 * inch, "D&D 5e Character Sheet — Page 1",
           size=6, color=C_SUBTEXT, align="center")


# ---------------------------------------------------------------------------
# Header block  (top of page 1)
# ---------------------------------------------------------------------------
def _header_block(s: Sheet, info: dict):
    TOP = PH - MARGIN
    W   = PW - 2 * MARGIN
    X   = MARGIN

    # character name — big
    name = info.get("name", "Unnamed Hero") or "Unnamed Hero"
    s.c.setFillColor(C_HEADER)
    s.c.setFont("Helvetica-Bold", 20)
    s.c.drawString(X, TOP - 18, name)

    # decorative gold rule under name
    s.hrule(X, TOP - 22, W, lw=1.5)

    # Info row 1
    y1 = TOP - 36
    fields1 = [
        ("Class & Level", f"{info.get('class', '')} {info.get('level', '')}".strip()),
        ("Background",    info.get("background", "")),
        ("Player Name",   info.get("player_name", "")),
    ]
    seg = W / 3
    for i, (lbl, val) in enumerate(fields1):
        fx = X + i * seg
        s.rbox(fx, y1 - 14, seg - 4, 14, fill=C_DARK)
        s.text(fx + (seg - 4) / 2, y1 - 10, val or "—", size=8,
               color=C_TEXT, align="center")
        s.text(fx + (seg - 4) / 2, y1 - 22, lbl, size=6,
               color=C_SUBTEXT, align="center")

    # Info row 2
    y2 = y1 - 28
    fields2 = [
        ("Race",        info.get("race", "")),
        ("Alignment",   info.get("alignment", "")),
        ("Experience",  str(info.get("experience_points", 0)) + " XP"),
    ]
    for i, (lbl, val) in enumerate(fields2):
        fx = X + i * seg
        s.rbox(fx, y2 - 14, seg - 4, 14, fill=C_DARK)
        s.text(fx + (seg - 4) / 2, y2 - 10, val or "—", size=8,
               color=C_TEXT, align="center")
        s.text(fx + (seg - 4) / 2, y2 - 22, lbl, size=6,
               color=C_SUBTEXT, align="center")

    s.hrule(X, y2 - 28, W, lw=0.5)


# ---------------------------------------------------------------------------
# Ability Scores + Saving Throws  (left column)
# ---------------------------------------------------------------------------
ABILITY_NAMES = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_KEYS  = ["strength", "dexterity", "constitution",
                 "intelligence", "wisdom", "charisma"]

SAVE_KEYS = ["strength_save", "dexterity_save", "constitution_save",
             "intelligence_save", "wisdom_save", "charisma_save"]


def _ability_block(s: Sheet, scores: dict, throws: dict):
    X   = MARGIN
    TOP = PH - MARGIN - 110     # below header block

    COL_W = 0.70 * inch
    BOX_H = 0.62 * inch

    _section_header(s, X, TOP, COL_W * 2 + 4, "Ability Scores")

    for i, (abbr, key) in enumerate(zip(ABILITY_NAMES, ABILITY_KEYS)):
        row = i // 2
        col = i % 2
        bx = X + col * (COL_W + 4)
        by = TOP - (row + 1) * (BOX_H + 4)

        score = scores.get(key, 10)
        mod   = _mod(score)

        # outer box
        s.rbox(bx, by, COL_W, BOX_H, fill=C_WHITE)
        # big modifier circle
        s.circle(bx + COL_W / 2, by + 14, 12, fill=C_PARCHMENT)
        s.text(bx + COL_W / 2, by + 10, _fmt_mod(mod),
               size=10, bold=True, color=C_HEADER, align="center")
        # score number
        s.text(bx + COL_W / 2, by + BOX_H - 14, str(score),
               size=16, bold=True, color=C_TEXT, align="center")
        # ability label
        s.text(bx + COL_W / 2, by + BOX_H - 25, abbr,
               size=7, bold=True, color=C_SUBTEXT, align="center")

    # ── Saving Throws
    sy_start = TOP - 3 * (BOX_H + 4) - 6
    sav_w    = COL_W * 2 + 4

    _section_header(s, X, sy_start, sav_w, "Saving Throws")

    prof_bonus = _prof_bonus_from_throws(throws)

    for i, (abbr, key) in enumerate(zip(ABILITY_NAMES, SAVE_KEYS)):
        ry = sy_start - 11 - i * 10
        td = throws.get(key, {})
        prof = td.get("proficient", False)
        val  = td.get("value", 0)

        # dot
        s.circle(X + 6, ry + 3, 3, fill=C_RED if prof else C_WHITE)
        s.text(X + 13, ry, _fmt_mod(val), size=7, color=C_TEXT)
        s.text(X + 30, ry, abbr, size=7, color=C_TEXT)

    # Passive Perception
    pp_y = sy_start - 11 - 6 * 10 - 4
    wis_score = 0
    for key, abbr in zip(ABILITY_KEYS, ABILITY_NAMES):
        if abbr == "WIS":
            wis_score = throws.get("wisdom_save", {}).get("value", _mod(scores.get("wisdom", 10)))
            break
    wis_mod = _mod(scores.get("wisdom", 10))
    # try to get perception skill
    pp = 10 + wis_mod
    s.rbox(X, pp_y - 12, sav_w, 12, fill=C_DARK)
    s.text(X + sav_w / 2, pp_y - 9, f"Passive Perception  {pp}",
           size=7, color=C_TEXT, bold=True, align="center")

    # Prof bonus
    pb_y = pp_y - 22
    s.rbox(X, pb_y - 14, sav_w, 14, fill=C_WHITE)
    s.text(X + sav_w / 2, pb_y - 10, _fmt_mod(prof_bonus),
           size=11, bold=True, color=C_HEADER, align="center")
    s.text(X + sav_w / 2, pb_y - 20, "Proficiency Bonus",
           size=6, color=C_SUBTEXT, align="center")

    # Inspiration
    insp_y = pb_y - 34
    s.circle(X + 10, insp_y + 4, 5, fill=C_WHITE)
    s.text(X + 20, insp_y, "Inspiration", size=7, color=C_TEXT)


def _prof_bonus_from_throws(throws: dict) -> int:
    for k, v in throws.items():
        if isinstance(v, dict) and v.get("proficient"):
            val   = v.get("value", 0)
            base  = v.get("base_mod", 0)
            bonus = val - base
            if 2 <= bonus <= 6:
                return bonus
    return 2


# ---------------------------------------------------------------------------
# Skills  (middle-left column)
# ---------------------------------------------------------------------------
SKILLS = [
    ("Acrobatics",       "dexterity",     "acrobatics"),
    ("Animal Handling",  "wisdom",        "animal_handling"),
    ("Arcana",           "intelligence",  "arcana"),
    ("Athletics",        "strength",      "athletics"),
    ("Deception",        "charisma",      "deception"),
    ("History",          "intelligence",  "history"),
    ("Insight",          "wisdom",        "insight"),
    ("Intimidation",     "charisma",      "intimidation"),
    ("Investigation",    "intelligence",  "investigation"),
    ("Medicine",         "wisdom",        "medicine"),
    ("Nature",           "intelligence",  "nature"),
    ("Perception",       "wisdom",        "perception"),
    ("Performance",      "charisma",      "performance"),
    ("Persuasion",       "charisma",      "persuasion"),
    ("Religion",         "intelligence",  "religion"),
    ("Sleight of Hand",  "dexterity",     "sleight_of_hand"),
    ("Stealth",          "dexterity",     "stealth"),
    ("Survival",         "wisdom",        "survival"),
]

STAT_ABBR = {
    "strength": "STR", "dexterity": "DEX", "constitution": "CON",
    "intelligence": "INT", "wisdom": "WIS", "charisma": "CHA",
}


def _skills_block(s: Sheet, skills: dict, scores: dict):
    # Position: right of ability block
    X   = MARGIN + 1.50 * inch
    TOP = PH - MARGIN - 110

    W = 1.65 * inch
    _section_header(s, X, TOP, W, "Skills")

    for i, (name, stat, key) in enumerate(SKILLS):
        ry   = TOP - 11 - i * 10.2
        sk   = skills.get(key, {})
        prof = sk.get("proficient", False)
        exp  = sk.get("expertise", False)
        val  = sk.get("value", _mod(scores.get(stat, 10)))
        abbr = STAT_ABBR.get(stat, "")

        fill = C_RED if prof else C_WHITE
        if exp:
            s.circle(X + 6, ry + 3, 3, fill=fill)
            s.circle(X + 12, ry + 3, 3, fill=fill)
        else:
            s.circle(X + 6, ry + 3, 3, fill=fill)

        s.text(X + 16, ry, _fmt_mod(val), size=6.5, color=C_TEXT)
        s.text(X + 30, ry, name, size=6.5, color=C_TEXT)
        s.text(X + W - 2, ry, abbr, size=5.5, color=C_SUBTEXT, align="right")


# ---------------------------------------------------------------------------
# Combat Stats  (right area, top)
# ---------------------------------------------------------------------------
def _combat_block(s: Sheet, combat: dict, info: dict):
    X   = MARGIN + 3.30 * inch
    TOP = PH - MARGIN - 110
    W   = PW - X - MARGIN

    ac      = combat.get("ac",           10)
    ini     = combat.get("initiative",    0)
    speed   = combat.get("speed",        30)
    max_hp  = combat.get("max_hp",        0)
    cur_hp  = combat.get("current_hp",   max_hp)
    tmp_hp  = combat.get("temp_hp",       0)
    hd_used = combat.get("hit_dice_used", 0)
    ds_s    = combat.get("death_successes", 0)
    ds_f    = combat.get("death_failures",  0)

    level   = info.get("level", 1) or 1
    cls     = info.get("class", "")

    from ui.editors.combat_stats import HIT_DICE
    die = HIT_DICE.get(cls, 8)

    _section_header(s, X, TOP, W, "Combat")

    cell_h = 0.50 * inch
    cell_y = TOP - cell_h - 4

    # AC diamond
    cell_w = W / 3 - 4
    acx = X + cell_w / 2 + 2
    s.diamond(acx, cell_y + cell_h / 2, cell_w / 2 - 2, cell_h / 2 - 2,
              fill=C_WHITE)
    s.text(acx, cell_y + cell_h / 2 - 5, str(ac),
           size=16, bold=True, color=C_HEADER, align="center")
    s.text(acx, cell_y - 6, "Armor Class",
           size=6, color=C_SUBTEXT, align="center")

    # Initiative circle
    inix = X + W / 2
    s.circle(inix, cell_y + cell_h / 2, cell_h / 2 - 2, fill=C_WHITE)
    s.text(inix, cell_y + cell_h / 2 - 5, _fmt_mod(ini),
           size=14, bold=True, color=C_HEADER, align="center")
    s.text(inix, cell_y - 6, "Initiative",
           size=6, color=C_SUBTEXT, align="center")

    # Speed box
    spdx = X + W - cell_w / 2 - 2
    s.rbox(X + 2 * (cell_w + 4), cell_y, cell_w, cell_h, fill=C_WHITE)
    s.text(spdx, cell_y + cell_h / 2 - 5, f"{speed} ft",
           size=11, bold=True, color=C_HEADER, align="center")
    s.text(spdx, cell_y - 6, "Speed",
           size=6, color=C_SUBTEXT, align="center")

    # HP row
    hp_y = cell_y - 0.55 * inch

    # Max HP
    s.rbox(X, hp_y, W, 0.45 * inch, fill=C_WHITE)
    s.text(X + W / 2, hp_y + 0.28 * inch, str(max_hp),
           size=14, bold=True, color=C_HEADER, align="center")
    s.text(X + W / 2, hp_y + 0.45 * inch + 2, "Hit Point Maximum",
           size=6, color=C_SUBTEXT, align="center")

    cur_y = hp_y - 0.52 * inch
    s.rbox(X, cur_y, W * 0.55 - 2, 0.45 * inch, fill=C_WHITE)
    s.text(X + (W * 0.55 - 2) / 2, cur_y + 0.28 * inch, str(cur_hp),
           size=14, bold=True, color=C_HEADER, align="center")
    s.text(X + (W * 0.55 - 2) / 2, cur_y + 0.45 * inch + 2,
           "Current HP", size=6, color=C_SUBTEXT, align="center")

    tmp_x = X + W * 0.55 + 2
    s.rbox(tmp_x, cur_y, W * 0.45 - 2, 0.45 * inch, fill=C_WHITE)
    s.text(tmp_x + (W * 0.45 - 2) / 2, cur_y + 0.28 * inch, str(tmp_hp),
           size=14, bold=True, color=C_SUBTEXT, align="center")
    s.text(tmp_x + (W * 0.45 - 2) / 2, cur_y + 0.45 * inch + 2,
           "Temp HP", size=6, color=C_SUBTEXT, align="center")

    # Hit Dice + Death Saves row
    hd_y = cur_y - 0.50 * inch
    hd_total = level
    hd_left  = hd_total - hd_used

    s.rbox(X, hd_y, W * 0.45 - 2, 0.40 * inch, fill=C_WHITE)
    s.text(X + (W * 0.45 - 2) / 2, hd_y + 0.22 * inch,
           f"{hd_left}/{hd_total} d{die}",
           size=10, bold=True, color=C_TEXT, align="center")
    s.text(X + (W * 0.45 - 2) / 2, hd_y + 0.40 * inch + 2,
           "Hit Dice", size=6, color=C_SUBTEXT, align="center")

    # Death saves
    ds_x = X + W * 0.45 + 2
    ds_w = W * 0.55 - 2
    s.rbox(ds_x, hd_y, ds_w, 0.40 * inch, fill=C_WHITE)
    s.text(ds_x + ds_w / 2, hd_y + 0.40 * inch + 2,
           "Death Saves", size=6, color=C_SUBTEXT, align="center")

    def _ds_row(label, count, filled, row_y):
        s.text(ds_x + 4, row_y, label, size=6, color=C_TEXT)
        for j in range(3):
            fill = C_RED if j < filled else C_WHITE
            stroke = C_RED if label == "Failures" else colors.HexColor("#1a6b1a")
            s.circle(ds_x + ds_w - 12 - j * 11, row_y + 3, 4,
                     fill=fill, stroke=stroke)

    _ds_row("Successes", 3, ds_s, hd_y + 0.22 * inch)
    _ds_row("Failures",  3, ds_f, hd_y + 0.06 * inch)


# ---------------------------------------------------------------------------
# Attacks & Spellcasting
# ---------------------------------------------------------------------------
def _attacks_block(s: Sheet, attacks: dict):
    X   = MARGIN + 3.30 * inch
    W   = PW - X - MARGIN
    # positioned below combat block
    Y   = PH - MARGIN - 110 - 2.60 * inch

    atk_list = attacks.get("attacks", [])
    spell_ab  = attacks.get("spell_attack_bonus", "")
    spell_dc  = attacks.get("spell_save_dc", "")

    _section_header(s, X, Y, W, "Attacks & Spellcasting")

    # column headers
    col_n = X + 4
    col_b = X + W * 0.45
    col_d = X + W * 0.60
    hy    = Y - 10
    for cx, lbl in [(col_n, "Name"), (col_b, "Atk Bonus"), (col_d, "Damage / Type")]:
        s.text(cx, hy, lbl, size=6, color=C_SUBTEXT, bold=True)

    s.hrule(X, hy - 2, W, lw=0.5)

    row_h = 10
    max_rows = 7
    for i, atk in enumerate(atk_list[:max_rows]):
        ry = hy - row_h * (i + 1) - 2
        fill = C_DARK if i % 2 == 0 else C_WHITE
        s.c.setFillColor(fill)
        s.c.rect(X, ry - 1, W, row_h, fill=1, stroke=0)
        s.text(col_n, ry + 1, str(atk.get("name", ""))[:22], size=6.5, color=C_TEXT)
        s.text(col_b, ry + 1, str(atk.get("attack_bonus", "")), size=6.5, color=C_TEXT)
        dmg = f"{atk.get('damage_dice', '')} {atk.get('damage_type', '')}".strip()
        s.text(col_d, ry + 1, dmg[:22], size=6.5, color=C_TEXT)

    # spell stats
    if spell_ab or spell_dc:
        sy = hy - row_h * (max_rows + 1) - 6
        s.text(X + 4, sy, f"Spell Attack Bonus: {spell_ab}   Spell Save DC: {spell_dc}",
               size=7, color=C_TEXT)


# ---------------------------------------------------------------------------
# Equipment
# ---------------------------------------------------------------------------
def _equipment_block(s: Sheet, equip: dict):
    X   = MARGIN + 1.50 * inch
    W   = 1.75 * inch
    # position below skills block (~18 skill rows × 10.2 pt)
    Y   = PH - MARGIN - 110 - 18 * 10.2 - 20

    items    = equip.get("items", [])
    currency = equip.get("currency", {})

    _section_header(s, X, Y, W, "Equipment")

    # currency row
    coins = [("CP", "cp"), ("SP", "sp"), ("EP", "ep"), ("GP", "gp"), ("PP", "pp")]
    cw    = W / len(coins)
    cy    = Y - 16
    for i, (lbl, key) in enumerate(coins):
        cx = X + i * cw + cw / 2
        val = currency.get(key, 0)
        s.rbox(X + i * cw, cy - 12, cw - 2, 12, fill=C_WHITE)
        s.text(cx, cy - 9, str(val), size=6.5, color=C_TEXT, align="center")
        s.text(cx, cy - 20, lbl, size=6, color=C_SUBTEXT, align="center")

    # item list
    iy = cy - 26
    row_h = 9
    max_items = 14
    for i, item in enumerate(items[:max_items]):
        ry   = iy - i * row_h
        fill = C_DARK if i % 2 == 0 else C_WHITE
        s.c.setFillColor(fill)
        s.c.rect(X, ry - 1, W, row_h, fill=1, stroke=0)
        name = item.get("name", "")[:26]
        qty  = item.get("quantity", 1)
        eqp  = " ✦" if item.get("equipped") else ""
        s.text(X + 3, ry + 1, f"{qty}× {name}{eqp}", size=6.5, color=C_TEXT)


# ---------------------------------------------------------------------------
# Personality  (far-right column)
# ---------------------------------------------------------------------------
def _personality_block(s: Sheet, pers: dict, info: dict):
    X = PW - MARGIN - 1.65 * inch
    W = 1.65 * inch
    Y = PH - MARGIN - 110

    _section_header(s, X, Y, W, "Personality")

    sections = [
        ("Traits",  "traits"),
        ("Ideals",  "ideals"),
        ("Bonds",   "bonds"),
        ("Flaws",   "flaws"),
    ]
    py = Y - 4
    box_h = 0.52 * inch
    for label, key in sections:
        py -= box_h + 4
        s.rbox(X, py, W, box_h, fill=C_WHITE)
        s.text(X + W / 2, py + box_h - 6, label,
               size=6, bold=True, color=C_SUBTEXT, align="center")
        text = pers.get(key, "") or ""
        lines = _wrap_text(text, 28)[:4]
        for j, line in enumerate(lines):
            s.text(X + 3, py + box_h - 14 - j * 8, line,
                   size=6.5, color=C_TEXT)


# ---------------------------------------------------------------------------
# Page 2  — Features, Proficiencies
# ---------------------------------------------------------------------------
def _draw_page2(s: Sheet, d: dict):
    s.fill_bg()

    features = d.get("features", {})
    profs    = d.get("proficiencies", {})
    info     = d.get("character_info", {})

    # page title
    name = info.get("name", "Unnamed Hero") or "Unnamed Hero"
    s.c.setFont("Helvetica-Bold", 14)
    s.c.setFillColor(C_HEADER)
    s.c.drawString(MARGIN, PH - MARGIN - 14, f"{name}  —  Page 2")
    s.hrule(MARGIN, PH - MARGIN - 18, PW - 2 * MARGIN, lw=1.2)

    _features_block(s, features)
    _proficiencies_block(s, profs)

    s.hrule(MARGIN, 0.22 * inch, PW - 2 * MARGIN, lw=0.5)
    s.text(PW / 2, 0.10 * inch, "D&D 5e Character Sheet — Page 2",
           size=6, color=C_SUBTEXT, align="center")


def _features_block(s: Sheet, features: dict):
    feat_list = features.get("features", [])
    X = MARGIN
    W = (PW - 2 * MARGIN) * 0.60
    Y = PH - MARGIN - 30

    _section_header(s, X, Y, W, "Features & Traits")

    py = Y - 6
    max_feats = 18
    for feat in feat_list[:max_feats]:
        name = feat.get("name", "")
        desc = feat.get("description", "")

        entry_lines = _wrap_text(desc, 68)[:3]
        h = 10 + len(entry_lines) * 8 + 4

        if py - h < 0.30 * inch:
            break

        py -= h
        s.rbox(X, py, W, h, fill=C_WHITE)
        s.text(X + 4, py + h - 9, name, size=7.5, bold=True, color=C_HEADER)
        for j, line in enumerate(entry_lines):
            s.text(X + 4, py + h - 18 - j * 8, line, size=6.5, color=C_TEXT)
        py -= 3


def _proficiencies_block(s: Sheet, profs: dict):
    X = MARGIN + (PW - 2 * MARGIN) * 0.62
    W = (PW - 2 * MARGIN) * 0.38
    Y = PH - MARGIN - 30

    _section_header(s, X, Y, W, "Proficiencies & Languages")

    categories = [
        ("Armor",    profs.get("armor", [])),
        ("Weapons",  profs.get("weapons", [])),
        ("Tools",    profs.get("tools", [])),
        ("Languages", profs.get("languages", [])),
    ]

    py = Y - 6
    for cat, items in categories:
        if not items:
            continue
        py -= 14
        s.text(X + 3, py, cat, size=7, bold=True, color=C_HEADER)
        py -= 2
        s.hrule(X + 3, py, W - 6, lw=0.4)
        text = ", ".join(items) if isinstance(items, list) else str(items)
        lines = _wrap_text(text, 36)[:6]
        for line in lines:
            py -= 9
            s.text(X + 3, py, line, size=6.5, color=C_TEXT)
        py -= 4


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
def export_pdf(char_data: dict, path: str):
    c = rl_canvas.Canvas(path, pagesize=LETTER)
    sh = Sheet(c)

    _draw_page1(sh, char_data)
    c.showPage()
    _draw_page2(sh, char_data)
    c.showPage()

    c.save()
