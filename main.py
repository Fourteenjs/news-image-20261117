# main.py — news-image-20261117 entry (make.fun).
# A program that DRAWS one front-page image summing up Tuesday 17 Nov 2026.
# Pure Python 3 stdlib only (no PIL, no network). Deterministic: two runs
# write byte-identical PNGs. Output: $MAKEFUN_OUTPUT_DIR/entry.png (or /output).
# Usage (dev): python3 main.py [1|2|3] [out.png]  — variant 1 is the default.
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import (Canvas, draw_text, draw_block, wrap_text, text_w,
                    save_png, draw_map)

INK = bytes((26, 26, 26))
PAPER = bytes((247, 243, 232))
PAPER2 = bytes((255, 252, 244))
RED = bytes((185, 28, 28))
BLUE = bytes((38, 84, 124))
LAND = bytes((232, 214, 165))
GREY = bytes((90, 84, 72))
LGREY = bytes((200, 192, 172))
DARK = bytes((30, 41, 59))

W = H = 1024
MARGIN = 28

# ---------------------------------------------------------------- stories
# Every headline was checked against reporting of 17 Nov 2026 (or, where
# marked 16 Nov, was the news carried on 17 Nov front pages). No invented
# numbers or dates. (headline, sub-line or '', map marker number or 0)
EUROPE = [
    ("Russia hits Kyiv bridges", "Reply strikes target Dnipro crossings", 0),
    ("UK sanctions 8 settlement builders", "Asset freezes over West Bank building", 7),
    ("Depardieu drops appeal", "Sex-assault conviction now final in Paris", 0),
    ("Geneva opens robot-weapons talks", "128 states debate binding rules", 0),
    ("EU plans Rwanda return hub", "5 states to send rejected asylum seekers", 0),
]
MIDDLE_EAST = [
    ("Iran drones target US base", "Bahrain: all intercepted, no injuries", 2),
    ("Tanker hit off Oman", "Crew safe; 3rd US carrier in region", 3),
    ("Houthis advance on Aden", "Govt forces pull back from Red Sea coast", 8),
    ("West presses Israel on Gaza aid", "Call to open crossings for tents, food", 0),
]
ASIA_PACIFIC = [
    ("Trump lands in Manila", "First Quad summit in two years", 4),
    ("Xi, Carney cut tariffs", "Relief for C$400m of Canadian goods", 6),
    ("Japan scrambles jets", "Suspected Russian planes enter airspace", 5),
    ("Xi-Trump-Putin talks set", "First trilateral meet on Thursday", 0),
]
AMERICAS = [
    ("Pentagon fails audit again", "9th year; $4.8T cannot be verified", 0),
    ("13 babies born with measles", "US cases highest since 1991", 0),
    ("White House curbs testimony", "Agencies need approval to appear", 0),
]
TECH = [
    ("US closes AI-chip loophole", "New rule on remote access to chips", 0),
    ("Anthropic IPO to price Wed.", "Raise of up to $64B on Nasdaq", 0),
    ("GTA VI out on Thursday", "Midnight launch on PS5 and Xbox", 0),
    ("Malware hits 178 big sites", "Via Optimizely; BBC, CNN, Zoom hit", 0),
]
COMING_UP = [
    ("THU — Xi, Trump, Putin meet", "First trilateral, in Shenzhen", 0),
    ("THU — GTA VI launches", "At midnight, local time", 0),
    ("WED — Anthropic prices IPO", "Trading starts Thursday", 0),
    ("FRI — COP31 deal sought", "Final week in Antalya", 0),
]
REGIONS = [
    ("EUROPE", EUROPE),
    ("MIDDLE EAST", MIDDLE_EAST),
    ("ASIA-PACIFIC", ASIA_PACIFIC),
    ("AMERICAS", AMERICAS),
    ("TECH & BUSINESS", TECH),
    ("COMING UP", COMING_UP),
]
MARKERS = [
    (33, 45, 1, RED), (47, 29, 2, RED), (60, 22, 3, RED),
    (125, 11, 4, RED), (141, 38, 5, RED), (110, 26, 6, RED),
    (-0.1, 51.5, 7, RED), (45, 12.5, 8, RED),
]
NUMBERS = ["2nd day, Kerch", "8 firms sanctioned", "3 US carriers",
           "$4.8T unaudited", "13 babies", "128 states", "$64B IPO",
           "178 sites hit"]

# ---------------------------------------------------------------- shared pieces
def draw_masthead(cv, name_scale=6):
    x0, x1 = MARGIN, W - MARGIN
    draw_text(cv, (x0 + x1) // 2, 30, "THE WORLD IN ONE PAGE", name_scale, INK, 'c')
    y = 30 + 8 * name_scale + 10
    cv.hline(x0, y, x1 - x0, INK, 3)
    y += 12
    draw_text(cv, (x0 + x1) // 2, y, "TUESDAY, 17 NOVEMBER 2026", 3, INK, 'c')
    y += 8 * 3 + 10
    draw_text(cv, (x0 + x1) // 2, y,
              "25 STORIES FROM AROUND THE WORLD - TUESDAY'S NEWS IN ONE PAGE",
              2, GREY, 'c')
    y += 8 * 2 + 12
    cv.hline(x0, y, x1 - x0, RED, 3)
    return y + 14

def draw_bridge(cv, x, y, w, h):
    """Stylised Kerch bridge with a broken span. Geometry is relative to
    the panel height so nothing pokes out of the frame: deck sits above
    a water band, towers rise from the deck, smoke stays inside."""
    cv.fill_rect(x, y, w, h, DARK)
    # water band at the bottom
    wy = y + h - 20
    cv.fill_rect(x, wy, w, 20, bytes((56, 96, 130)))
    for i in range(3):
        cv.hline(x + 16 + i * 9, wy + 5 + i * 5, w - 32 - i * 18,
                 bytes((180, 210, 230)), 2)
    deck_y = wy - 14
    mid = x + w // 2
    gap = 26
    # deck: two halves with a gap in the middle
    cv.fill_rect(x + 8, deck_y, mid - gap - (x + 8), 6, PAPER2)
    cv.fill_rect(mid + gap, deck_y, x + w - 8 - (mid + gap), 6, PAPER2)
    # broken span tilting down from the left deck end into the water
    cv.line(mid - gap, deck_y + 3, mid - 2, wy - 2, PAPER2, 4)
    # towers (stay inside the panel)
    top = deck_y - 34
    for tx in (x + w // 4, x + 3 * w // 4):
        cv.fill_rect(tx - 3, top, 6, deck_y - top, PAPER2)
        # cables fan from the tower top down to the deck on its own side
        for dx in (-34, -17, 17, 34):
            ex = tx + dx
            if x + 8 <= ex <= x + w - 8 and abs(ex - mid) > gap + 4:
                cv.line(tx, top, ex, deck_y, PAPER2, 1)
    # smoke over the gap, inside the panel
    for (sx, sy, r) in ((mid - 10, top + 16, 9), (mid + 8, top + 8, 11),
                        (mid, top + 26, 7)):
        cv.circle(sx, sy, r, bytes((120, 116, 108)), fill=True)
        cv.circle(sx, sy, r, bytes((90, 86, 80)))
    # red burst at the break
    cv.circle(mid - 4, deck_y - 4, 6, RED, fill=True)
    cv.circle(mid - 4, deck_y - 4, 6, bytes((255, 220, 120)))

def draw_lead_panel(cv, x, y, w, h, img_h=92, head_scale=4):
    cv.fill_rect(x, y, w, h, PAPER2)
    cv.rect(x, y, w, h, INK, 2)
    ix, iy, iw = x + 12, y + 12, w - 24
    draw_bridge(cv, ix, iy, iw, img_h)
    ty = iy + img_h + 8
    draw_text(cv, x + 16, ty, "LEAD STORY", 2, RED)
    ty += 8 * 2 + 6
    lines = wrap_text("KERCH BRIDGE HIT AGAIN", w - 32, head_scale)
    ty = draw_block(cv, x + 16, ty, lines, head_scale, INK,
                    leading=10 * head_scale)
    ty += 4
    sub = wrap_text("Ukraine strikes a 2nd day; the road arch falls.",
                    w - 32, 2)
    draw_block(cv, x + 16, ty, sub, 2, GREY, leading=20)

def draw_map_panel(cv, x, y, w, h):
    cv.rect(x, y, w, h, INK, 2)
    if w < 480:
        draw_text(cv, x + 12, y + 10, "WHERE IT HAPPENED", 2, INK)
        draw_text(cv, x + w - 12, y + 10, "1-8", 2, RED, 'r')
        draw_map(cv, x + 2, y + 34, w - 4, h - 36, BLUE, LAND, MARKERS,
                 marker_r=7)
    else:
        draw_text(cv, x + 12, y + 10, "WHERE THE DAY HAPPENED", 2, INK)
        draw_text(cv, x + w - 12, y + 10, "1-8 ON THE MAP", 2, RED, 'r')
        draw_map(cv, x + 2, y + 34, w - 4, h - 36, BLUE, LAND, MARKERS)

def draw_region_block(cv, x, y, w, h, title, stories):
    """Region block: title + red rule, then stories laid out in flow order
    (headline lines are measured, gaps justified to fill the block)."""
    draw_text(cv, x, y, title, 3, INK)
    cv.hline(x, y + 8 * 3 + 6, w, RED, 3)
    top = y + 8 * 3 + 16
    avail = h - (8 * 3 + 16)
    n = len(stories)
    # measure each story's height (headline lines only, first story + sub)
    heights = []
    for i, (head, sub, mark) in enumerate(stories):
        txw = w - (22 if mark else 0)
        lines = wrap_text(head, txw, 2)[:2]
        hh = len(lines) * 20
        heights.append(hh)
    min_gap = 4
    total = sum(heights) + (n - 1) * min_gap
    # sub-line for the first story, if it fits
    show_sub = False
    if stories[0][1] and total + 12 <= avail:
        show_sub = True
        total += 12
    gap = min_gap
    if n > 1 and total < avail:
        gap = min_gap + (avail - total) / (n - 1)
    sy = top
    for i, (head, sub, mark) in enumerate(stories):
        syi = int(sy)
        tx = x
        if mark:
            cv.circle(x + 9, syi + 8, 9, RED, fill=True)
            cv.circle(x + 9, syi + 8, 9, INK)
            draw_text(cv, x + 9, syi + 3, str(mark), 1,
                      bytes((255, 255, 255)), 'c')
            tx = x + 22
        lines = wrap_text(head, w - (tx - x), 2)[:2]
        draw_block(cv, tx, syi, lines, 2, INK, leading=20)
        sy += heights[i]
        if i == 0 and show_sub:
            draw_text(cv, tx, int(sy) + 2, sub, 1, GREY)
            sy += 12
        sy += gap

def draw_footer(cv, y):
    draw_text(cv, W // 2, y,
              "THE WORLD IN ONE PAGE  -  Covering Tuesday 17 November 2026"
              "  -  Sources: wire reports",
              1, GREY, 'c')

# ---------------------------------------------------------------- layouts
def draw_numbers_strip(cv, y):
    s = "THE DAY IN NUMBERS:  " + "  \u2022  ".join(NUMBERS)
    lines = wrap_text(s, W - 2 * MARGIN, 2)
    return draw_block(cv, W // 2, y, lines, 2, INK, leading=20, align='c')

def draw_grid(cv, y, block_h, cols=3):
    col_w = (W - 2 * MARGIN - (cols - 1) * 16) // cols
    for i, (title, stories) in enumerate(REGIONS):
        r, c = divmod(i, cols)
        bx = MARGIN + c * (col_w + 16)
        by = y + r * (block_h + 16)
        draw_region_block(cv, bx, by, col_w, block_h, title, stories)
    return y + ((len(REGIONS) + cols - 1) // cols) * (block_h + 16) - 16

def variant_1(cv):
    """Broadsheet: masthead, map + lead hero, numbers strip, 3x2 grid."""
    cv.fill_rect(0, 0, W, H, PAPER)
    cv.rect(20, 20, W - 40, H - 40, INK, 2)
    y = draw_masthead(cv)
    draw_map_panel(cv, MARGIN, y, 540, 280)
    draw_lead_panel(cv, MARGIN + 540 + 16, y, W - MARGIN - (MARGIN + 540 + 16),
                    280)
    y += 280 + 12
    y = draw_numbers_strip(cv, y)
    y += 12
    draw_grid(cv, y, 222)
    draw_footer(cv, 984)

def variant_2(cv):
    """Map first: compact masthead, full-width map, lead strip, 3x2 grid."""
    cv.fill_rect(0, 0, W, H, PAPER)
    cv.rect(20, 20, W - 40, H - 40, INK, 2)
    y = draw_masthead(cv, name_scale=5)
    draw_map_panel(cv, MARGIN, y, W - 2 * MARGIN, 260)
    y += 260 + 12
    draw_text(cv, MARGIN, y, "LEAD STORY", 2, RED)
    draw_text(cv, MARGIN, y + 22,
              "KERCH BRIDGE HIT AGAIN", 4, INK)
    draw_text(cv, MARGIN, y + 22 + 40,
              "Ukraine strikes a 2nd day; the road arch falls into the strait.",
              2, GREY)
    y += 22 + 40 + 20 + 12
    cv.hline(MARGIN, y, W - 2 * MARGIN, RED, 3)
    y += 14
    draw_grid(cv, y, 200)
    draw_footer(cv, 976)

def variant_3(cv):
    """Lead dominant: big bridge illustration + headline, small map, grid."""
    cv.fill_rect(0, 0, W, H, PAPER)
    cv.rect(20, 20, W - 40, H - 40, INK, 2)
    y = draw_masthead(cv)
    draw_lead_panel(cv, MARGIN, y, 612, 280, img_h=140, head_scale=4)
    mx = MARGIN + 612 + 16
    draw_map_panel(cv, mx, y, W - MARGIN - mx, 280)
    y += 280 + 12
    y = draw_numbers_strip(cv, y)
    y += 12
    draw_grid(cv, y, 222)
    draw_footer(cv, 984)

VARIANTS = {1: variant_1, 2: variant_2, 3: variant_3}

def main():
    variant = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    out_arg = sys.argv[2] if len(sys.argv) > 2 else None
    out_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    out_path = out_arg or os.path.join(out_dir, 'entry.png')
    cv = Canvas(W, H, PAPER)
    VARIANTS[variant](cv)
    os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
    n = save_png(cv, out_path)
    sys.stderr.write("wrote %s (%d bytes, variant %d)\n"
                     % (out_path, n, variant))
    return 0

if __name__ == '__main__':
    sys.exit(main())
