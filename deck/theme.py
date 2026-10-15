"""Design system for the deck.

Single source of truth for colour, type and geometry. Every value here is
taken straight from the brief so the deck stays on-spec.
"""

# --- Colour palette (strict) ------------------------------------------------
BG_LIGHT = "F8F9FA"   # primary background
BG_WHITE = "FFFFFF"
TEXT = "212529"       # body text
BLACK = "000000"
NAVY = "1A365D"       # accent 1 - headings
GREEN = "2F855A"      # accent 2 - positive
ORANGE = "DD6B20"     # accent 3 - risk / warning
RED = "C53030"        # accent 3 alt - risk
WHITE = "FFFFFF"
GREY = "6C757D"       # muted captions (derived, still neutral)
GREY_LIGHT = "E9ECEF" # hairline / table zebra
NAVY_TINT = "EDF2F7"  # very light navy wash for panels
GREEN_TINT = "E6F4EC"
ORANGE_TINT = "FBEEE2"

# --- Typography -------------------------------------------------------------
FONT = "Arial"        # single family across the whole deck

# Point sizes (brief ranges)
SZ_COVER_TITLE = 40
SZ_COVER_SUB = 24
SZ_TITLE = 34         # slide title (32-40)
SZ_SUBTITLE = 26      # sub-heading (24-28)
SZ_BODY = 22          # body (20-24)
SZ_SMALL = 18         # smallest allowed (captions)
SZ_BIG = 130          # hero statistic
SZ_KPI = 54           # large inline figure

# --- Geometry (inches) ------------------------------------------------------
SLIDE_W = 13.333
SLIDE_H = 7.5
MARGIN = 0.72         # ~1.8 cm - inside the 1-2 cm band
CONTENT_W = SLIDE_W - 2 * MARGIN
CONTENT_TOP = 1.62    # first content baseline under the title rule
FOOTER_Y = SLIDE_H - 0.5

COL = CONTENT_W / 3.0  # rule-of-thirds column width

EMU_PER_IN = 914400
