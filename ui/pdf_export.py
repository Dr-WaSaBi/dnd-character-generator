"""
PDF export — two-page D&D 5e character sheet via reportlab.
"""

import os
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas as rl_canvas

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
C_PARCHMENT = colors.HexColor("#F5E6C8")
C_DARK      = colors.HexColor("#EAD8A8")
C_BORDER    = colors.HexColor("#8B4513")
C_HEADER    = colors.HexColor("#2C1810")
C_TEXT      = colors.HexColor("#1A0A00")
C_SUBTEXT   = colors.HexColor("#6B4226")
C_GOLD      = colors.HexColor("#C8A84B")
C_RED       = colors.HexColor("#8B0000")
C_GREEN     = colors.HexColor("#1a6b1a")
C_WHITE     = colors.white

PW, PH = LETTER   # 612 × 792 pts

# Margins & column layout (pts)
M     = 0.30 * inch   # 21.6
TOP_Y = PH - M - 98   # top of main content (below header)  ≈ 672

C1_X = M               # ability scores
C1_W = 72.0            # 1.0 inch

C2_X = C1_X + C1_W + 4
C2_W = 108.0           # 1.5 inch   (saves + skills)

C3_X = C2_X + C2_W + 4
C4_W = 126.0           # 1.75 inch  personality (right side)
C4_X = PW - M - C4_W
C3_W = C4_X - C3_X - 4


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _mod(score: int) -> int:
    return (score - 10) // 2


def _fmt(val: int) -> str:
    return f"+{val}" if val >= 0 else str(val)


def _prof(level: int) -> int:
    return (max(1, level) - 1) // 4 + 2


def _wrap(text: str, max_chars: int) -> list[str]:
    words = (text or "").split()
    lines, cur = [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > max_chars:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------
class Sheet:
    def __init__(self, c: rl_canvas.Canvas):
        self.c = c

    def bg(self):
        self.c.setFillColor(C_PARCHMENT)
        self.c.rect(0, 0, PW, PH, fill=1, stroke=0)

    def rbox(self, x, y, w, h, r=4, fill=C_DARK, stroke=C_BORDER, lw=0.7):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill)
        self.c.roundRect(x, y, w, h, r, fill=1, stroke=1)

    def box(self, x, y, w, h, fill=C_WHITE, stroke=C_BORDER, lw=0.7):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill)
        self.c.rect(x, y, w, h, fill=1, stroke=1)

    def circle(self, cx, cy, r, fill=C_WHITE, stroke=C_BORDER, lw=0.7):
        self.c.setStrokeColor(stroke)
        self.c.setLineWidth(lw)
        self.c.setFillColor(fill)
        self.c.circle(cx, cy, r, fill=1, stroke=1)

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

    def rule(self, x, y, w, color=C_GOLD, lw=0.8):
        self.c.setStrokeColor(color)
        self.c.setLineWidth(lw)
        self.c.line(x, y, x + w, y)

    def txt(self, x, y, s, size=8, color=C_TEXT, bold=False, align="left"):
        self.c.setFillColor(color)
        self.c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        s = str(s)
        if align == "center":
            self.c.drawCentredString(x, y, s)
        elif align == "right":
            self.c.drawRightString(x, y, s)
        else:
            self.c.drawString(x, y, s)


def _sec_hdr(s: Sheet, x, y, w, title: str, h=12):
    s.c.setFillColor(C_RED)
    s.c.setStrokeColor(C_RED)
    s.c.roundRect(x, y, w, h, 3, fill=1, stroke=0)
    s.txt(x + w / 2, y + 3, title.upper(), size=6.5,
          color=C_WHITE, bold=True, align="center")
    return y - 2   # return y just below the header


# ---------------------------------------------------------------------------
# ABILITY SCORES  (column 1)
# ---------------------------------------------------------------------------
ABILITY_ABBRS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
ABILITY_KEYS  = ["strength", "dexterity", "constitution",
                 "intelligence", "wisdom", "charisma"]
ABBR_TO_KEY   = dict(zip(ABILITY_ABBRS, ABILITY_KEYS))

SAVE_ABBRS = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]


def _ability_col(s: Sheet, scores: dict, y_top: float) -> float:
    """Draw ability score boxes. Returns y of bottom."""
    _sec_hdr(s, C1_X, y_top, C1_W, "Ability Scores")
    y = y_top - 2

    BH = 42.0   # box height
    GAP = 3.0

    for i, (abbr, key) in enumerate(zip(ABILITY_ABBRS, ABILITY_KEYS)):
        by = y - BH - GAP
        score = scores.get(key, 10)
        mod   = _mod(score)

        s.box(C1_X, by, C1_W, BH, fill=C_WHITE)
        # ability label at top
        s.txt(C1_X + C1_W / 2, by + BH - 11, abbr,
              size=7, bold=True, color=C_SUBTEXT, align="center")
        # score (large)
        s.txt(C1_X + C1_W / 2, by + BH - 24, str(score),
              size=14, bold=True, color=C_HEADER, align="center")
        # modifier circle at bottom
        s.circle(C1_X + C1_W / 2, by + 9, 8, fill=C_PARCHMENT)
        s.txt(C1_X + C1_W / 2, by + 6, _fmt(mod),
              size=8, bold=True, color=C_HEADER, align="center")

        y = by

    return y   # bottom of last box


# ---------------------------------------------------------------------------
# SAVES + INSPIRATION + PROF BONUS  (column 2 top)
# ---------------------------------------------------------------------------
def _saves_col(s: Sheet, throws: dict, scores: dict,
               prof_bonus: int, y_top: float) -> float:
    """Draw inspiration, prof bonus, saving throws. Returns y of bottom."""

    # Inspiration
    s.circle(C2_X + 8, y_top - 8, 5, fill=C_WHITE)
    s.txt(C2_X + 16, y_top - 11, "Inspiration", size=7, color=C_TEXT)

    # Proficiency Bonus
    pb_y = y_top - 28
    s.box(C2_X, pb_y, C2_W, 14, fill=C_WHITE)
    s.txt(C2_X + C2_W / 2, pb_y + 4, _fmt(prof_bonus),
          size=9, bold=True, color=C_HEADER, align="center")
    s.txt(C2_X + C2_W / 2, pb_y - 8, "Proficiency Bonus",
          size=6, color=C_SUBTEXT, align="center")

    # Saving Throws
    sv_top = pb_y - 20
    _sec_hdr(s, C2_X, sv_top, C2_W, "Saving Throws")
    y = sv_top - 2

    for abbr, key in zip(SAVE_ABBRS, ABILITY_KEYS):
        prof   = throws.get(abbr, False)
        base   = _mod(scores.get(key, 10))
        val    = base + (prof_bonus if prof else 0)
        ry     = y - 10
        s.circle(C2_X + 6, ry + 4, 3,
                 fill=C_RED if prof else C_WHITE,
                 stroke=C_RED if prof else C_BORDER)
        s.txt(C2_X + 13, ry + 1, _fmt(val), size=7, color=C_TEXT)
        s.txt(C2_X + 28, ry + 1, abbr, size=7, color=C_TEXT)
        y = ry

    # Passive Perception
    wis_mod = _mod(scores.get("wisdom", 10))
    pp      = 10 + wis_mod
    pp_y    = y - 8
    s.rbox(C2_X, pp_y, C2_W, 12, fill=C_DARK)
    s.txt(C2_X + C2_W / 2, pp_y + 3, f"Passive Perception  {pp}",
          size=6.5, bold=True, color=C_HEADER, align="center")

    return pp_y


# ---------------------------------------------------------------------------
# SKILLS  (column 2 bottom half)
# ---------------------------------------------------------------------------
SKILLS = [
    ("Acrobatics",      "DEX"),
    ("Animal Handling", "WIS"),
    ("Arcana",          "INT"),
    ("Athletics",       "STR"),
    ("Deception",       "CHA"),
    ("History",         "INT"),
    ("Insight",         "WIS"),
    ("Intimidation",    "CHA"),
    ("Investigation",   "INT"),
    ("Medicine",        "WIS"),
    ("Nature",          "INT"),
    ("Perception",      "WIS"),
    ("Performance",     "CHA"),
    ("Persuasion",      "CHA"),
    ("Religion",        "INT"),
    ("Sleight of Hand", "DEX"),
    ("Stealth",         "DEX"),
    ("Survival",        "WIS"),
]


def _skills_col(s: Sheet, skills: dict, scores: dict,
                prof_bonus: int, y_top: float) -> float:
    sk_top = y_top - 12
    _sec_hdr(s, C2_X, sk_top, C2_W, "Skills")
    y = sk_top - 2

    for name, abbr in SKILLS:
        key  = ABBR_TO_KEY[abbr]
        prof = skills.get(name, False)
        base = _mod(scores.get(key, 10))
        val  = base + (prof_bonus if prof else 0)
        ry   = y - 9.8
        s.circle(C2_X + 6, ry + 3.5, 3,
                 fill=C_RED if prof else C_WHITE,
                 stroke=C_RED if prof else C_BORDER)
        s.txt(C2_X + 13, ry + 0.5, _fmt(val), size=6.5, color=C_TEXT)
        s.txt(C2_X + 27, ry + 0.5, name, size=6.5, color=C_TEXT)
        s.txt(C2_X + C2_W - 2, ry + 0.5, abbr, size=5.5,
              color=C_SUBTEXT, align="right")
        y = ry

    return y


# ---------------------------------------------------------------------------
# COMBAT STATS  (column 3 top)
# ---------------------------------------------------------------------------
def _combat_col(s: Sheet, combat: dict, info: dict, y_top: float) -> float:
    level  = info.get("level", 1) or 1
    cls    = info.get("class", "")

    try:
        from ui.editors.combat_stats import HIT_DICE
        die = HIT_DICE.get(cls, 8)
    except Exception:
        die = 8

    ac      = combat.get("ac", 10)
    ini     = combat.get("initiative", 0)
    speed   = combat.get("speed", 30)
    max_hp  = combat.get("max_hp", 0)
    cur_hp  = combat.get("current_hp", max_hp)
    tmp_hp  = combat.get("temp_hp", 0)
    hd_used = combat.get("hit_dice_used", 0)
    ds_s    = combat.get("death_successes", 0)
    ds_f    = combat.get("death_failures", 0)
    hd_left = level - hd_used

    y = _sec_hdr(s, C3_X, y_top, C3_W, "Combat Stats")

    # ── Row 1: AC  Initiative  Speed
    R1H = 46.0
    y -= R1H + 4
    cw  = C3_W / 3 - 3

    # AC diamond
    acx = C3_X + cw / 2
    s.diamond(acx, y + R1H / 2, cw / 2 - 3, R1H / 2 - 3, fill=C_WHITE)
    s.txt(acx, y + R1H / 2 - 6, str(ac),
          size=16, bold=True, color=C_HEADER, align="center")
    s.txt(acx, y - 8, "Armor Class", size=6, color=C_SUBTEXT, align="center")

    # Initiative circle
    inx = C3_X + C3_W / 2
    s.circle(inx, y + R1H / 2, R1H / 2 - 3, fill=C_WHITE)
    s.txt(inx, y + R1H / 2 - 6, _fmt(ini),
          size=14, bold=True, color=C_HEADER, align="center")
    s.txt(inx, y - 8, "Initiative", size=6, color=C_SUBTEXT, align="center")

    # Speed box
    spx = C3_X + 2 * (cw + 3) + cw / 2
    s.box(C3_X + 2 * (cw + 3), y, cw, R1H, fill=C_WHITE)
    s.txt(spx, y + R1H / 2 - 6, f"{speed} ft",
          size=12, bold=True, color=C_HEADER, align="center")
    s.txt(spx, y - 8, "Speed", size=6, color=C_SUBTEXT, align="center")

    # ── Row 2: Max HP
    y -= 22
    s.box(C3_X, y, C3_W, 32, fill=C_WHITE)
    s.txt(C3_X + C3_W / 2, y + 10,
          str(max_hp) if max_hp else "—",
          size=16, bold=True, color=C_HEADER, align="center")
    s.txt(C3_X + C3_W / 2, y + 34, "Hit Point Maximum",
          size=6, color=C_SUBTEXT, align="center")

    # ── Row 3: Current HP  |  Temp HP
    y -= 46
    lw = C3_W * 0.57 - 2
    rw = C3_W - lw - 4
    s.box(C3_X, y, lw, 32, fill=C_WHITE)
    s.txt(C3_X + lw / 2, y + 10,
          str(cur_hp) if max_hp else "—",
          size=16, bold=True, color=C_HEADER, align="center")
    s.txt(C3_X + lw / 2, y + 34, "Current Hit Points",
          size=6, color=C_SUBTEXT, align="center")

    tx = C3_X + lw + 4
    s.box(tx, y, rw, 32, fill=C_WHITE)
    s.txt(tx + rw / 2, y + 10, str(tmp_hp) or "—",
          size=14, bold=True, color=C_SUBTEXT, align="center")
    s.txt(tx + rw / 2, y + 34, "Temporary HP",
          size=6, color=C_SUBTEXT, align="center")

    # ── Row 4: Hit Dice  |  Death Saves
    y -= 46
    dw = C3_W * 0.42 - 2
    sw = C3_W - dw - 4

    s.box(C3_X, y, dw, 36, fill=C_WHITE)
    s.txt(C3_X + dw / 2, y + 12, f"{hd_left}/{level}",
          size=11, bold=True, color=C_TEXT, align="center")
    s.txt(C3_X + dw / 2, y + 4, f"d{die}", size=8, color=C_SUBTEXT, align="center")
    s.txt(C3_X + dw / 2, y + 38, "Hit Dice", size=6, color=C_SUBTEXT, align="center")

    dsx = C3_X + dw + 4
    s.box(dsx, y, sw, 36, fill=C_WHITE)
    s.txt(dsx + sw / 2, y + 38, "Death Saves",
          size=6, color=C_SUBTEXT, align="center")

    def _ds_row(label, count, filled, ry, dot_color):
        s.txt(dsx + 4, ry, label, size=6, color=C_TEXT)
        for j in range(3):
            fill = dot_color if j < filled else C_WHITE
            s.circle(dsx + sw - 10 - j * 11, ry + 4, 4,
                     fill=fill, stroke=dot_color)

    _ds_row("Successes", 3, ds_s, y + 20, C_GREEN)
    _ds_row("Failures",  3, ds_f, y + 6,  C_RED)

    return y - 14


# ---------------------------------------------------------------------------
# ATTACKS & SPELLCASTING  (column 3 middle)
# ---------------------------------------------------------------------------
def _attacks_col(s: Sheet, attacks: dict, y_top: float) -> float:
    y = _sec_hdr(s, C3_X, y_top, C3_W, "Attacks & Spellcasting")

    atk_list = attacks.get("attacks", [])
    spell_ab = attacks.get("spell_atk_bonus")
    spell_dc = attacks.get("spell_save_dc")

    # Column headers
    cn = C3_X + 3
    cb = C3_X + C3_W * 0.46
    cd = C3_X + C3_W * 0.60
    y -= 10
    s.txt(cn, y, "Name",         size=6, color=C_SUBTEXT, bold=True)
    s.txt(cb, y, "Atk Bonus",    size=6, color=C_SUBTEXT, bold=True)
    s.txt(cd, y, "Damage / Type",size=6, color=C_SUBTEXT, bold=True)
    y -= 2
    s.rule(C3_X, y, C3_W, lw=0.5)

    RH = 9.5
    for i, atk in enumerate(atk_list[:8]):
        ry = y - RH * (i + 1)
        fill = C_DARK if i % 2 == 0 else C_WHITE
        s.c.setFillColor(fill)
        s.c.rect(C3_X, ry - 1, C3_W, RH, fill=1, stroke=0)
        s.txt(cn, ry + 1.5, str(atk.get("name", ""))[:22], size=7, color=C_TEXT)
        s.txt(cb, ry + 1.5, str(atk.get("attack_bonus", "")),size=7, color=C_TEXT)
        dmg = f"{atk.get('damage', '')} {atk.get('damage_type', '')}".strip()
        s.txt(cd, ry + 1.5, dmg[:22], size=7, color=C_TEXT)

    y -= RH * (min(len(atk_list), 8) + 1) + 4

    if spell_ab or spell_dc:
        y -= 10
        parts = []
        if spell_ab:
            parts.append(f"Spell Attack Bonus: {spell_ab}")
        if spell_dc:
            parts.append(f"Spell Save DC: {spell_dc}")
        s.txt(C3_X + 3, y, "   ".join(parts), size=6.5, color=C_TEXT)

    return y - 4


# ---------------------------------------------------------------------------
# EQUIPMENT  (column 3 bottom)
# ---------------------------------------------------------------------------
COIN_KEYS = [("CP", "CP"), ("SP", "SP"), ("EP", "EP"),
             ("GP", "GP"), ("PP", "PP")]


def _equipment_col(s: Sheet, equip: dict, y_top: float) -> float:
    y = _sec_hdr(s, C3_X, y_top, C3_W, "Equipment & Currency")

    currency = equip.get("currency", {})
    items    = equip.get("items", [])

    # Currency row
    y -= 2
    cw = C3_W / 5
    for i, (label, key) in enumerate(COIN_KEYS):
        cx  = C3_X + i * cw + cw / 2
        val = currency.get(key, 0)
        s.box(C3_X + i * cw, y - 12, cw - 2, 12, fill=C_WHITE)
        s.txt(cx, y - 9, str(val), size=7, color=C_TEXT, align="center")
        s.txt(cx, y - 22, label, size=6, color=C_SUBTEXT, align="center")

    # Item list
    y -= 28
    RH = 9.0
    for i, item in enumerate(items[:14]):
        if y - RH < M + 14:
            break
        ry   = y - RH
        fill = C_DARK if i % 2 == 0 else C_WHITE
        s.c.setFillColor(fill)
        s.c.rect(C3_X, ry, C3_W, RH, fill=1, stroke=0)
        qty  = item.get("qty", item.get("quantity", 1))
        name = str(item.get("name", ""))[:28]
        eqp  = " ✦" if item.get("equipped") else ""
        s.txt(C3_X + 3, ry + 1.5, f"{qty}× {name}{eqp}", size=7, color=C_TEXT)
        y = ry

    # Border around whole equipment section
    total_h = y_top - y + 2
    s.c.setStrokeColor(C_BORDER)
    s.c.setLineWidth(0.5)
    s.c.rect(C3_X, y - 2, C3_W, total_h, fill=0, stroke=1)

    return y - 4


# ---------------------------------------------------------------------------
# PERSONALITY  (column 4)
# ---------------------------------------------------------------------------
PERS_FIELDS = [
    ("Personality Traits", "traits"),
    ("Ideals",             "ideals"),
    ("Bonds",              "bonds"),
    ("Flaws",              "flaws"),
]


def _personality_col(s: Sheet, pers: dict, y_top: float) -> float:
    y = y_top
    BOX_H = (y_top - M - 14) / 4 - 4   # divide available height into 4

    for label, key in PERS_FIELDS:
        bh = BOX_H
        s.box(C4_X, y - bh, C4_W, bh, fill=C_WHITE)
        # red label banner inside top of box
        s.c.setFillColor(C_RED)
        s.c.roundRect(C4_X, y - 12, C4_W, 12, 3, fill=1, stroke=0)
        s.txt(C4_X + C4_W / 2, y - 9, label.upper(),
              size=6, bold=True, color=C_WHITE, align="center")

        text  = pers.get(key, "") or ""
        lines = _wrap(text, 26)
        for j, line in enumerate(lines[:5]):
            s.txt(C4_X + 4, y - 16 - j * 9, line, size=7, color=C_TEXT)

        y -= bh + 4

    return y


# ---------------------------------------------------------------------------
# HEADER  (top of page)
# ---------------------------------------------------------------------------
def _header(s: Sheet, info: dict):
    x   = M
    w   = PW - 2 * M
    top = PH - M

    # Character name
    name = info.get("character_name", "") or info.get("name", "") or "Unnamed Hero"
    s.c.setFillColor(C_HEADER)
    s.c.setFont("Helvetica-Bold", 20)
    s.c.drawString(x, top - 18, name)
    s.rule(x, top - 22, w, lw=1.5)

    # Row 1: Class+Level, Background, Player Name
    fields1 = [
        ("Class & Level", f"{info.get('class', '')} {info.get('level', '')}".strip()),
        ("Background",    info.get("background", "")),
        ("Player Name",   info.get("player_name", "")),
    ]
    seg = w / 3
    y1  = top - 37
    for i, (lbl, val) in enumerate(fields1):
        fx = x + i * seg
        s.rbox(fx + 1, y1 - 13, seg - 4, 13, fill=C_DARK)
        s.txt(fx + seg / 2, y1 - 10, str(val) or "—",
              size=8, color=C_TEXT, align="center")
        s.txt(fx + seg / 2, y1 - 22, lbl,
              size=6, color=C_SUBTEXT, align="center")

    # Row 2: Race, Alignment, XP
    fields2 = [
        ("Race",       info.get("race", "")),
        ("Alignment",  info.get("alignment", "")),
        ("Experience", f"{info.get('xp', 0) or 0} XP"),
    ]
    y2 = y1 - 28
    for i, (lbl, val) in enumerate(fields2):
        fx = x + i * seg
        s.rbox(fx + 1, y2 - 13, seg - 4, 13, fill=C_DARK)
        s.txt(fx + seg / 2, y2 - 10, str(val) or "—",
              size=8, color=C_TEXT, align="center")
        s.txt(fx + seg / 2, y2 - 22, lbl,
              size=6, color=C_SUBTEXT, align="center")

    s.rule(x, y2 - 28, w, lw=0.5)


# ---------------------------------------------------------------------------
# PAGE 1
# ---------------------------------------------------------------------------
def _page1(s: Sheet, d: dict):
    s.bg()

    info    = d.get("character_info", {})
    scores  = d.get("ability_scores", {})
    throws  = d.get("saving_throws", {})
    skills  = d.get("skills", {})
    combat  = d.get("combat_stats", {})
    attacks = d.get("attacks_spells", {})
    equip   = d.get("equipment", {})
    pers    = d.get("personality", {})

    level      = info.get("level", 1) or 1
    prof_bonus = _prof(level)

    _header(s, info)

    # Column 1 — ability scores
    _ability_col(s, scores, TOP_Y)

    # Column 2 — saves, skills
    saves_bot = _saves_col(s, throws, scores, prof_bonus, TOP_Y)
    _skills_col(s, skills, scores, prof_bonus, saves_bot)

    # Column 3 — combat, attacks, equipment
    combat_bot  = _combat_col(s, combat, info, TOP_Y)
    attacks_bot = _attacks_col(s, attacks, combat_bot)
    _equipment_col(s, equip, attacks_bot)

    # Column 4 — personality
    _personality_col(s, pers, TOP_Y)

    # Footer
    s.rule(M, M + 10, PW - 2 * M, lw=0.4)
    s.txt(PW / 2, M + 3, "D&D 5e Character Sheet — Page 1",
          size=6, color=C_SUBTEXT, align="center")


# ---------------------------------------------------------------------------
# PAGE 2  — Features & Proficiencies
# ---------------------------------------------------------------------------
def _page2(s: Sheet, d: dict):
    s.bg()

    info     = d.get("character_info", {})
    features = d.get("features", {})
    profs    = d.get("proficiencies", {})

    name = info.get("character_name", "") or info.get("name", "") or "Unnamed Hero"
    s.c.setFont("Helvetica-Bold", 14)
    s.c.setFillColor(C_HEADER)
    s.c.drawString(M, PH - M - 14, f"{name}  —  Features, Traits & Proficiencies")
    s.rule(M, PH - M - 18, PW - 2 * M, lw=1.2)

    feat_list = features.get("features", [])
    y_top     = PH - M - 30

    # Left 60%: features
    FW = (PW - 2 * M) * 0.60
    FX = M
    y  = _sec_hdr(s, FX, y_top, FW, "Features & Traits")

    for feat in feat_list:
        name_  = feat.get("name", "")
        desc   = feat.get("description", "")
        lines  = _wrap(desc, 72)[:4]
        bh     = 11 + len(lines) * 8 + 3
        if y - bh < M + 14:
            break
        y -= bh
        s.rbox(FX, y, FW, bh, r=3, fill=C_WHITE)
        s.txt(FX + 4, y + bh - 9, name_, size=8, bold=True, color=C_HEADER)
        for j, ln in enumerate(lines):
            s.txt(FX + 4, y + bh - 18 - j * 8, ln, size=6.5, color=C_TEXT)
        y -= 3

    # Right 38%: proficiencies
    PX = M + (PW - 2 * M) * 0.62
    PW2 = PW - M - PX
    yp  = _sec_hdr(s, PX, y_top, PW2, "Proficiencies & Languages")

    cats = [
        ("Armor",     profs.get("armor", [])),
        ("Weapons",   profs.get("weapons", [])),
        ("Tools",     profs.get("tools", [])),
        ("Languages", profs.get("languages", [])),
    ]
    for cat, items in cats:
        if not items:
            continue
        yp -= 13
        s.txt(PX + 3, yp, cat, size=7.5, bold=True, color=C_HEADER)
        yp -= 2
        s.rule(PX + 3, yp, PW2 - 6, lw=0.4)
        text  = ", ".join(items) if isinstance(items, list) else str(items)
        lines = _wrap(text, 34)
        for ln in lines[:6]:
            yp -= 9
            s.txt(PX + 3, yp, ln, size=7, color=C_TEXT)
        yp -= 4

    s.rule(M, M + 10, PW - 2 * M, lw=0.4)
    s.txt(PW / 2, M + 3, "D&D 5e Character Sheet — Page 2",
          size=6, color=C_SUBTEXT, align="center")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def export_pdf(char_data: dict, path: str):
    c = rl_canvas.Canvas(path, pagesize=LETTER)
    sh = Sheet(c)
    _page1(sh, char_data)
    c.showPage()
    _page2(sh, char_data)
    c.showPage()
    c.save()
