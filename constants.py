"""
constants.py — Semua konstanta warna, ukuran layar, dan konfigurasi game
"""

import pygame

# ── SCREEN ──────────────────────────────────────────────────────────────
W, H = 960, 640
FPS  = 60

# ── COLOURS ─────────────────────────────────────────────────────────────
SKY_TOP      = (20, 35, 75)
SKY_BOT      = (60, 100, 150)
MTN_DARK     = (15, 70, 75)
MTN_LIGHT    = (25, 105, 100)
GRASS_BACK   = (90, 160, 75)
GRASS_FRONT  = (65, 130, 55)

GOLD         = (255, 205, 40)
GOLD_DK      = (200, 140, 15)
UI_BLUE      = (25, 55, 120)
UI_BLUE_LT   = (50, 100, 200)
UI_GREEN     = (110, 210, 60)
UI_ORANGE    = (250, 150, 40)
UI_RED       = (240, 70, 60)
WHITE        = (255, 255, 255)
CREAM        = (255, 245, 220)
BLACK        = (0, 0, 0)
NEON_CYAN    = (50, 255, 255)
NEON_PINK    = (255, 100, 220)

# Player colour accents
P1_COL       = (80, 180, 255)   # Biru muda  — Player 1 (Red Panda)
P2_COL       = (255, 120, 60)   # Oranye     — Player 2 (Slime)

TIMER_OK     = (80, 220, 80)
TIMER_WARN   = (255, 200, 40)
TIMER_CRIT   = (240, 70, 60)

# ── CONTROLS (KEY CONSTANTS — diisi setelah pygame.init()) ───────────────
# P1: Z=opt0, X=opt1, C=opt2, V=opt3
P1_KEYS = None   # diisi di main.py setelah pygame.init()
# P2: UP=opt0, DOWN=opt1, LEFT=opt2, RIGHT=opt3
P2_KEYS = None

# ── GAMEPLAY ────────────────────────────────────────────────────────────
ROUND_TIMER   = 15.0    # detik per soal
TOTAL_HP      = 5
QUESTIONS_PER_MATCH = 10

def init_controls():
    """Harus dipanggil setelah pygame.init()"""
    global P1_KEYS, P2_KEYS
    P1_KEYS = [pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v]
    P2_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
