"""
visuals.py — Drawing helpers, fonts, karakter vector
REVISI v3: font lebih kecil + tidak bold untuk teks opsi, warna dari palet game
"""

import pygame
import math
import random
from constants import *

# ── FONT LOADER ─────────────────────────────────────────────────────────
def make_font(size, bold=True):
    CANDIDATES = ["Trebuchet MS", "Verdana", "Tahoma", "Segoe UI", "Arial"]
    for name in CANDIDATES:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except:
            pass
    return pygame.font.Font(None, size)

fXL = fL = fM = fS = fXS = fKEY = fOPT = None

def init_fonts():
    global fXL, fL, fM, fS, fXS, fKEY, fOPT
    fXL  = make_font(48, True)    # Victory/judul besar
    fL   = make_font(30, True)    # Sub-judul
    fM   = make_font(22, True)    # Teks soal (bold ok, background gelap)
    fS   = make_font(18, True)    # Label, score
    fXS  = make_font(14, False)   # Keterangan kecil
    fKEY = make_font(16, True)    # Key badge
    fOPT = make_font(18, False)   # Teks opsi jawaban — TIDAK BOLD, lebih kecil

# ── PALET WARNA GAME ─────────────────────────────────────────────────────
# Dari palet yang dikirim
PAL_ORANGE       = (210, 100, 45)
PAL_CREAM        = (245, 230, 200)
PAL_NAVY         = (55,  75, 110)
PAL_RED          = (180, 50,  55)
PAL_PURPLE_DARK  = (110, 60, 150)
PAL_PURPLE_LIGHT = (155, 100, 190)
PAL_OLIVE        = (100, 140, 70)
PAL_BEIGE        = (240, 225, 195)
PAL_GOLD         = (215, 175, 40)
PAL_BROWN        = (120, 75,  35)

# Warna teks opsi — gelap supaya kontras di background panel putih/terang
OPT_TEXT_DEFAULT = (45, 35, 20)       # coklat tua — sangat terbaca di background terang
OPT_TEXT_CORRECT = (30, 100, 40)      # hijau tua
OPT_TEXT_WRONG   = (140, 35, 35)      # merah tua
OPT_BG_DEFAULT   = (250, 245, 235)    # beige sangat terang
OPT_BG_CORRECT   = (210, 245, 215)    # hijau muda
OPT_BG_WRONG     = (250, 215, 215)    # merah muda
OPT_BORDER_DEFAULT = PAL_NAVY
OPT_BORDER_CORRECT = (60, 160, 70)
OPT_BORDER_WRONG   = (180, 60, 60)

# Panel soal
PANEL_BG         = (255, 250, 240)    # putih hangat/cream
PANEL_BORDER     = PAL_BROWN
Q_TEXT_COL       = (40, 30, 15)       # coklat sangat gelap — max kontras di panel terang

# ── DRAWING HELPERS ─────────────────────────────────────────────────────
def grad_rect(surf, top_col, bot_col, rect):
    x, y, w, h = rect
    for i in range(h):
        r = int(top_col[0] + (bot_col[0] - top_col[0]) * i / h)
        g = int(top_col[1] + (bot_col[1] - top_col[1]) * i / h)
        b = int(top_col[2] + (bot_col[2] - top_col[2]) * i / h)
        pygame.draw.line(surf, (r, g, b), (x, y + i), (x + w, y + i))


def draw_rounded_panel(surf, rect, color, radius=20, border_color=None, border_w=3):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border_color and border_w:
        pygame.draw.rect(surf, border_color, rect, border_w, border_radius=radius)


def draw_text_outline(surf, text, font, col, cx, cy, outline_col=(0,0,0), outline_w=2):
    """Render teks dengan outline untuk keterbacaan di background busy."""
    rendered = font.render(text, True, col)
    outline  = font.render(text, True, outline_col)
    r = rendered.get_rect(center=(cx, cy))
    for dx in range(-outline_w, outline_w + 1):
        for dy in range(-outline_w, outline_w + 1):
            if dx == 0 and dy == 0:
                continue
            if abs(dx) + abs(dy) > outline_w + 1:
                continue
            surf.blit(outline, (r.x + dx, r.y + dy))
    surf.blit(rendered, r)


def draw_text_center(surf, text, font, col, cx, cy, shadow=True, shadow_col=(15, 25, 45)):
    """
    Teks dengan outline tebal — untuk teks di atas background gambar/gelap.
    Gunakan shadow=False untuk teks di atas panel berwarna cerah.
    """
    if shadow:
        draw_text_outline(surf, text, font, col, cx, cy,
                          outline_col=shadow_col, outline_w=2)
    else:
        rendered = font.render(text, True, col)
        surf.blit(rendered, rendered.get_rect(center=(cx, cy)))


def draw_text_left(surf, text, font, col, x, y):
    """Render teks rata kiri tanpa outline (untuk panel terang)."""
    rendered = font.render(text, True, col)
    surf.blit(rendered, (x, y))


def wrap_text(font, text, max_w):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if font.size(test)[0] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines if lines else [text]


# ── FALLBACK BACKGROUND ──────────────────────────────────────────────────
BG_STARS = [(random.randint(0, W), random.randint(0, H // 2),
             random.randint(1, 3), random.random()) for _ in range(80)]


def draw_scenery_fallback(surf, t):
    grad_rect(surf, SKY_TOP, SKY_BOT, (0, 0, W, H))
    for sx, sy, sr, sp in BG_STARS:
        bright = int(150 + 105 * math.sin(t * 1.5 + sp * 5))
        pygame.draw.circle(surf, (bright, bright, bright), (sx, sy), sr)
    pygame.draw.polygon(surf, MTN_DARK,  [(-50, H), (150, 200), (400, H)])
    pygame.draw.polygon(surf, MTN_DARK,  [(W + 50, H), (W - 150, 180), (W - 450, H)])
    pygame.draw.polygon(surf, MTN_LIGHT, [(-100, H), (80, 280), (350, H)])
    pygame.draw.polygon(surf, MTN_LIGHT, [(W + 100, H), (W - 250, 250), (W - 500, H)])
    pygame.draw.ellipse(surf, GRASS_BACK,  (-100, H - 250, W + 200, 300))
    pygame.draw.ellipse(surf, GRASS_FRONT, (-200, H - 150, W + 400, 300))


# ── RED PANDA (Player 1) ─────────────────────────────────────────────────
def draw_redpanda_avatar(surf, cx, cy, state="idle", anim_t=0, scale=1.0):
    s = scale
    bob = math.sin(anim_t * 5) * 5 if state == "idle" else 0
    shake_x = math.sin(anim_t * 25) * 6 if state == "hit" else 0
    cx = int(cx + shake_x)
    cy = int(cy + bob)
    RED_FUR    = (200, 70, 30)
    DARK_BROWN = (80, 40, 20)
    pygame.draw.ellipse(surf, (0, 0, 0), (cx-int(40*s), cy+int(55*s), int(80*s), int(15*s)))
    pygame.draw.ellipse(surf, RED_FUR,   (cx-int(60*s), cy+int(10*s), int(45*s), int(40*s)))
    pygame.draw.arc(surf, DARK_BROWN,    (cx-int(60*s), cy+int(10*s), int(45*s), int(40*s)),
                    math.pi/2, 3*math.pi/2, int(8*s))
    pygame.draw.ellipse(surf, DARK_BROWN, (cx-int(28*s), cy, int(56*s), int(60*s)))
    pygame.draw.rect(surf, (220,30,40), (cx-int(32*s), cy-int(5*s), int(64*s), int(20*s)), border_radius=8)
    pygame.draw.polygon(surf, (220,30,40), [(cx-int(25*s), cy+int(10*s)),(cx-int(40*s), cy+int(25*s)),(cx-int(20*s), cy+int(15*s))])
    pygame.draw.circle(surf, RED_FUR, (cx, cy-int(25*s)), int(32*s))
    pygame.draw.polygon(surf, WHITE,   [(cx-int(25*s), cy-int(20*s)),(cx-int(35*s), cy-int(50*s)),(cx-int(10*s), cy-int(45*s))])
    pygame.draw.polygon(surf, WHITE,   [(cx+int(25*s), cy-int(20*s)),(cx+int(35*s), cy-int(50*s)),(cx+int(10*s), cy-int(45*s))])
    pygame.draw.polygon(surf, RED_FUR, [(cx-int(23*s), cy-int(25*s)),(cx-int(28*s), cy-int(42*s)),(cx-int(12*s), cy-int(40*s))])
    pygame.draw.polygon(surf, RED_FUR, [(cx+int(23*s), cy-int(25*s)),(cx+int(28*s), cy-int(42*s)),(cx+int(12*s), cy-int(40*s))])
    pygame.draw.ellipse(surf, WHITE,   (cx-int(35*s), cy-int(25*s), int(25*s), int(20*s)))
    pygame.draw.ellipse(surf, WHITE,   (cx+int(10*s), cy-int(25*s), int(25*s), int(20*s)))
    pygame.draw.ellipse(surf, WHITE,   (cx-int(15*s), cy-int(15*s), int(30*s), int(15*s)))
    pygame.draw.circle(surf, BLACK, (cx, cy-int(12*s)), int(4*s))
    if state == "hit":
        pygame.draw.ellipse(surf, BLACK, (cx-int(5*s), cy-int(4*s), int(10*s), int(8*s)))
    else:
        pygame.draw.arc(surf, BLACK, (cx-int(8*s), cy-int(8*s), int(16*s), int(10*s)), math.pi, 2*math.pi, int(2*s))
    pygame.draw.circle(surf, BLACK, (cx-int(12*s), cy-int(20*s)), int(5*s))
    pygame.draw.circle(surf, BLACK, (cx+int(12*s), cy-int(20*s)), int(5*s))
    pygame.draw.circle(surf, WHITE, (cx-int(10*s), cy-int(22*s)), int(2*s))
    pygame.draw.circle(surf, WHITE, (cx+int(14*s), cy-int(22*s)), int(2*s))
    if state in ("attack","win") or (state=="idle" and math.sin(anim_t*2)>0):
        pygame.draw.ellipse(surf, DARK_BROWN, (cx+int(25*s), cy-int(15*s), int(20*s), int(25*s)))
        pygame.draw.circle(surf, (220,100,80), (cx+int(35*s), cy-int(5*s)), int(4*s))
    else:
        pygame.draw.circle(surf, DARK_BROWN, (cx-int(20*s), cy+int(40*s)), int(10*s))
        pygame.draw.circle(surf, DARK_BROWN, (cx+int(20*s), cy+int(40*s)), int(10*s))


# ── SLIME (Player 2) ─────────────────────────────────────────────────────
def draw_slime_avatar(surf, cx, cy, state="idle", anim_t=0, scale=1.0):
    s = scale
    bob = math.sin(anim_t * 5) * 6 if state == "idle" else 0
    shake_x = math.sin(anim_t * 25) * 6 if state == "hit" else 0
    cx = int(cx + shake_x)
    cy = int(cy + bob)
    pygame.draw.ellipse(surf, (0,0,0), (cx-int(42*s), cy+int(30*s), int(84*s), int(16*s)))
    pygame.draw.ellipse(surf, (150,60,220), (cx-int(40*s), cy-int(22*s), int(80*s), int(60*s)))
    pygame.draw.ellipse(surf, (190,120,255), (cx-int(20*s), cy-int(16*s), int(26*s), int(12*s)))
    pygame.draw.polygon(surf, GOLD, [
        (cx+int(5*s), cy-int(20*s)),(cx+int(15*s), cy-int(35*s)),
        (cx+int(25*s), cy-int(22*s)),(cx+int(35*s), cy-int(30*s)),(cx+int(35*s), cy-int(15*s))
    ])
    pygame.draw.circle(surf, BLACK, (cx-int(12*s), cy+int(4*s)), int(4*s))
    pygame.draw.circle(surf, BLACK, (cx+int(12*s), cy+int(4*s)), int(4*s))
    pygame.draw.circle(surf, WHITE, (cx-int(10*s), cy+int(2*s)), int(2*s))
    pygame.draw.circle(surf, WHITE, (cx+int(14*s), cy+int(2*s)), int(2*s))
    if state == "hit":
        pygame.draw.arc(surf, BLACK, (cx-int(6*s), cy+int(12*s), int(12*s), int(8*s)), 0, math.pi, int(3*s))
    else:
        pygame.draw.arc(surf, BLACK, (cx-int(6*s), cy+int(8*s), int(12*s), int(10*s)), math.pi, 2*math.pi, int(2*s))
