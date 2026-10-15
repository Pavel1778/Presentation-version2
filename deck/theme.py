"""Design system for the deck.

Single source of truth for colour, type and geometry. Every value here is
taken straight from the brief so the deck stays on-spec.
"""

# --- Colour palette ---------------------------------------------------------
# Deliberately restrained: two chromatic colours (navy + orange) plus
# neutrals. Colour carries meaning - navy for structure/stable, orange for
# risk/attention - so the deck stays readable on a projector.
BG_LIGHT = "F8F9FA"    # slide background
BG_WHITE = "FFFFFF"    # cards
TEXT = "212529"        # body ink
NAVY = "1A365D"        # primary
NAVY_DEEP = "122A4A"   # darker field for cover/closing
ORANGE = "DD6B20"      # the single accent: risk / attention
WHITE = "FFFFFF"
GREY = "6C757D"        # muted captions
GREY_LIGHT = "E9ECEF"  # hairlines, zebra
NAVY_TINT = "EDF2F7"   # faint navy wash
ORANGE_TINT = "FBEEE2" # faint orange wash

# --- Typography -------------------------------------------------------------
FONT = "Arial"

# Point sizes (brief ranges)
SZ_COVER_TITLE = 40
SZ_COVER_SUB = 24
SZ_HOOK = 46          # hook question on the opening slide
SZ_TITLE = 34         # slide title (32-40)
SZ_SUBTITLE = 26      # sub-heading (24-28)
SZ_BODY = 22          # body (20-24)
SZ_SMALL = 18         # smallest allowed (captions)
SZ_BIG = 120          # hero statistic
SZ_KPI = 60           # large inline figure

# --- Geometry (inches) ------------------------------------------------------
SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN = 0.72         # ~1.8 cm - inside the 1-2 cm band
CONTENT_W = SLIDE_W - 2 * MARGIN
CONTENT_TOP = 1.62    # first content baseline under the title rule
FOOTER_Y = SLIDE_H - 0.5

COL = CONTENT_W / 3.0  # rule-of-thirds column width

EMU_PER_IN = 914400
