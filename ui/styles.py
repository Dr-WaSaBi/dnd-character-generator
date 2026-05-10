# Parchment surface colors
COLOR_PARCHMENT        = "#F5E6C8"
COLOR_PARCHMENT_DARK   = "#EDD9A3"
COLOR_PARCHMENT_HOVER  = "#D9C48A"

# Section borders
COLOR_SECTION_BORDER       = "#5C3A1E"
COLOR_SECTION_BORDER_HOVER = "#8B1A1A"

# Badge (numbered circle)
COLOR_BADGE_BG   = "#8B1A1A"
COLOR_BADGE_RING = "#D4AF37"
COLOR_BADGE_TEXT = "#F5E6C8"

# Text
COLOR_TEXT_PRIMARY = "#2C1810"
COLOR_TEXT_HEADER  = "#5C3A1E"
COLOR_TEXT_SUBTEXT = "#7A5230"

# Window chrome
COLOR_WINDOW_BG       = "#2C1810"
COLOR_STATUSBAR_BG    = "#1A0A00"
COLOR_STATUSBAR_TEXT  = "#D4AF37"
COLOR_GOLD_RULE       = "#D4AF37"

FONT_HEADER = "Palatino Linotype"
FONT_BODY   = "Georgia"

SHEET_STYLE = f"""
    QMainWindow {{
        background-color: {COLOR_WINDOW_BG};
    }}

    QScrollArea {{
        background-color: {COLOR_PARCHMENT};
        border: none;
    }}

    QScrollArea > QWidget > QWidget {{
        background-color: {COLOR_PARCHMENT};
    }}

    QScrollBar:vertical {{
        background: {COLOR_PARCHMENT_DARK};
        width: 10px;
        border-radius: 5px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {COLOR_BADGE_BG};
        border-radius: 5px;
        min-height: 20px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QStatusBar {{
        background-color: {COLOR_STATUSBAR_BG};
        color: {COLOR_STATUSBAR_TEXT};
        font-family: {FONT_BODY};
        font-size: 9pt;
        padding: 2px 10px;
        border-top: 2px solid {COLOR_GOLD_RULE};
    }}
    QStatusBar QLabel {{
        color: {COLOR_STATUSBAR_TEXT};
        background: transparent;
    }}
"""
