"""
scenes.py — Render semua scene dengan UI premium
"""

import pygame
import math
import os
from constants import *
from visuals import (draw_rounded_panel, draw_text_center, draw_scenery_fallback,
                     draw_redpanda_avatar, draw_slime_avatar, wrap_text,
                     fXL, fL, fM, fS, fXS, fKEY, fOPT,
                     PAL_ORANGE, PAL_CREAM, PAL_NAVY, PAL_RED, PAL_PURPLE_DARK,
                     PAL_PURPLE_LIGHT, PAL_OLIVE, PAL_BEIGE, PAL_GOLD, PAL_BROWN,
                     OPT_TEXT_DEFAULT, OPT_TEXT_CORRECT, OPT_TEXT_WRONG,
                     OPT_BG_DEFAULT, OPT_BG_CORRECT, OPT_BG_WRONG,
                     OPT_BORDER_DEFAULT, OPT_BORDER_CORRECT, OPT_BORDER_WRONG,
                     PANEL_BG, PANEL_BORDER, Q_TEXT_COL)

# ── PATH HELPER ──────────────────────────────────────────────────────────
def _ap(*parts):
    """Absolute path relatif ke folder game ini."""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, *parts)

# ── GLOBALS ──────────────────────────────────────────────────────────────
logo_img      = None
bg_menu_img   = None
bg_battle_img = None
bg_result_img = None
char_p1_img   = None
char_p2_img   = None
HAS_LOGO      = HAS_BG_MENU = HAS_BG_BATTLE = HAS_BG_RESULT = False
HAS_CHAR_P1   = HAS_CHAR_P2 = False

sfx_correct = sfx_wrong = sfx_hit = sfx_click = sfx_tick = None
_current_music = None

# ── SURFACE CACHE ─────────────────────────────────────────────────────────
_overlay_cache = {}

# ── CONFETTI SYSTEM ───────────────────────────────────────────────────────
import random as _rnd

class Confetti:
    """Partikel confetti untuk layar result."""
    COLORS = [
        (255, 215, 0),    # Gold
        (255, 100, 60),   # Orange
        (100, 200, 255),  # Cyan
        (255, 100, 200),  # Pink
        (100, 255, 140),  # Green
        (200, 140, 255),  # Purple
        (255, 255, 100),  # Yellow
        (255, 80, 80),    # Red
    ]
    def __init__(self):
        self.reset()

    def reset(self):
        self.x   = _rnd.uniform(0, W)
        self.y   = _rnd.uniform(-60, -10)
        self.vx  = _rnd.uniform(-1.5, 1.5)
        self.vy  = _rnd.uniform(80, 180)
        self.rot = _rnd.uniform(0, 360)
        self.rot_v = _rnd.uniform(-180, 180)
        self.w   = _rnd.randint(8, 16)
        self.h   = _rnd.randint(4, 9)
        self.col = _rnd.choice(Confetti.COLORS)
        self.alive = True

    def update(self, dt):
        self.x   += self.vx
        self.y   += self.vy * dt
        self.rot += self.rot_v * dt
        self.vx  += _rnd.uniform(-0.3, 0.3)
        if self.y > H + 20:
            self.reset()   # loop kembali dari atas

    def draw(self, surf):
        try:
            s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
            s.fill((*self.col, 220))
            rot_s = pygame.transform.rotate(s, self.rot)
            surf.blit(rot_s, rot_s.get_rect(center=(int(self.x), int(self.y))))
        except:
            pass

# Pool confetti (dibuat sekali, di-reset saat masuk result)
_CONFETTI_COUNT = 80
_confetti_pool  = [Confetti() for _ in range(_CONFETTI_COUNT)]
_confetti_active = False

def reset_confetti():
    global _confetti_active
    _confetti_active = True
    for i, c in enumerate(_confetti_pool):
        c.reset()
        c.y = _rnd.uniform(-200, 0)   # mulai tersebar dari atas

def update_confetti(dt):
    if not _confetti_active:
        return
    for c in _confetti_pool:
        c.update(dt)

def draw_confetti(surf):
    if not _confetti_active:
        return
    for c in _confetti_pool:
        c.draw(surf)


def _get_overlay(w, h, color_rgba):
    key = (w, h, color_rgba)
    if key not in _overlay_cache:
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        s.fill(color_rgba)
        _overlay_cache[key] = s
    return _overlay_cache[key]

# ── ASSET LOADER ──────────────────────────────────────────────────────────
def _load_img(paths, scale_to=None, convert_alpha=False):
    for p in paths:
        full = _ap(p)
        if not os.path.exists(full):
            continue
        try:
            img = pygame.image.load(full)
            img = img.convert_alpha() if (convert_alpha or p.endswith(".png")) else img.convert()
            if scale_to:
                img = pygame.transform.smoothscale(img, scale_to)
            print(f"[ASSET OK] {p}")
            return img, True
        except Exception as e:
            print(f"[ASSET ERR] {p}: {e}")
    return None, False


def _load_snd(paths):
    for p in paths:
        full = _ap(p)
        if not os.path.exists(full):
            continue
        try:
            s = pygame.mixer.Sound(full)
            print(f"[SFX OK] {p}")
            return s
        except Exception as e:
            print(f"[SFX ERR] {p}: {e}")
    return None


def play_music(track):
    global _current_music
    if _current_music == track:
        return
    files = {
        "menu":   ["assets/music/music_menu.wav",   "assets/music/music_menu.mp3",   "assets/music/music_menu.ogg"],
        "battle": ["assets/music/music_battle.wav", "assets/music/music_battle.mp3", "assets/music/music_battle.ogg"],
        "result": ["assets/music/music_result.wav", "assets/music/music_result.mp3", "assets/music/music_result.ogg"],
    }
    for f in files.get(track, []):
        full = _ap(f)
        if os.path.exists(full):
            try:
                pygame.mixer.music.load(full)
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)
                _current_music = track
                print(f"[MUSIC] {f}")
                return
            except Exception as e:
                print(f"[MUSIC ERR] {f}: {e}")
    pygame.mixer.music.stop()
    _current_music = track


def play_sfx(name):
    m = {"correct": sfx_correct, "wrong": sfx_wrong, "tick": sfx_tick,
         "hit": sfx_hit, "click": sfx_click}
    s = m.get(name)
    if s:
        try: s.play()
        except: pass


def load_assets():
    global logo_img, bg_menu_img, bg_battle_img, bg_result_img
    global char_p1_img, char_p2_img
    global HAS_LOGO, HAS_BG_MENU, HAS_BG_BATTLE, HAS_BG_RESULT
    global HAS_CHAR_P1, HAS_CHAR_P2
    global sfx_correct, sfx_wrong, sfx_hit, sfx_click, sfx_tick

    # Logo — portrait (1024x1536), tampilkan dengan lebar max 280px
    logo_img, HAS_LOGO = _load_img(
        ["assets/logo_game.png", "logo_game.png"], scale_to=(280, 420))
    if not HAS_LOGO:
        logo_img = None  # akan digambar sebagai teks

    # Backgrounds
    bg_menu_img,   HAS_BG_MENU   = _load_img(
        ["assets/backgrounds/bg_menu.png",   "assets/backgrounds/bg_menu.jpg"], scale_to=(W, H))
    bg_battle_img, HAS_BG_BATTLE = _load_img(
        ["assets/backgrounds/bg_battle.png", "assets/backgrounds/bg_battle.jpg"], scale_to=(W, H))
    bg_result_img, HAS_BG_RESULT = _load_img(
        ["assets/backgrounds/bg_result.png", "assets/backgrounds/bg_result.jpg"], scale_to=(W, H))

    # Karakter — scale lebih besar
    char_p1_img, HAS_CHAR_P1 = _load_img(
        ["assets/characters/char_p1.png"], scale_to=(160, 160), convert_alpha=True)
    char_p2_img, HAS_CHAR_P2 = _load_img(
        ["assets/characters/char_p2.png"], scale_to=(160, 160), convert_alpha=True)

    # SFX
    if pygame.mixer.get_init():
        sfx_correct = _load_snd(["assets/sfx/sfx_correct.wav", "assets/sfx/sfx_correct.ogg"])
        sfx_wrong   = _load_snd(["assets/sfx/sfx_wrong.wav",   "assets/sfx/sfx_wrong.ogg"])
        sfx_hit     = _load_snd(["assets/sfx/sfx_hit.wav",     "assets/sfx/sfx_hit.ogg"])
        sfx_click   = _load_snd(["assets/sfx/sfx_click.wav",   "assets/sfx/sfx_click.ogg"])


# ── BACKGROUND ────────────────────────────────────────────────────────────
def _draw_bg(screen, scene, anim_t):
    drawn = False
    if scene == "menu" and HAS_BG_MENU:
        screen.blit(bg_menu_img, (0, 0)); drawn = True
    elif scene in ("game",) and HAS_BG_BATTLE:
        screen.blit(bg_battle_img, (0, 0)); drawn = True
    elif scene == "result":
        if HAS_BG_RESULT:
            screen.blit(bg_result_img, (0, 0)); drawn = True
        elif HAS_BG_BATTLE:
            screen.blit(bg_battle_img, (0, 0)); drawn = True
    if not drawn:
        draw_scenery_fallback(screen, anim_t)

    # Overlay semi-transparan di atas bg supaya UI lebih terbaca
    if scene == "game":
        screen.blit(_get_overlay(W, H, (0, 0, 0, 60)), (0, 0))
    elif scene == "result":
        screen.blit(_get_overlay(W, H, (0, 0, 20, 100)), (0, 0))


# ── CHARACTER RENDER ──────────────────────────────────────────────────────
def _draw_char(surf, is_p1, cx, cy, state, anim_t, scale=1.0):
    import math
    img = char_p1_img if is_p1 else char_p2_img
    has = HAS_CHAR_P1 if is_p1 else HAS_CHAR_P2

    if has and img:
        bob = int(math.sin(anim_t * 4) * 6) if state == "idle" else 0
        shk = int(math.sin(anim_t * 28) * 8) if state == "hit" else 0
        # Win: sedikit bounce
        if state == "win":
            bob = int(abs(math.sin(anim_t * 6)) * -12)
        sw, sh = img.get_size()

        # Shadow elips di bawah karakter
        shadow_surf = pygame.Surface((sw, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0,0,0,60), (0, 0, sw, 20))
        surf.blit(shadow_surf, (cx - sw//2 + shk, cy - sh//2 + sh - 8 + bob))

        surf.blit(img, (cx - sw//2 + shk, cy - sh//2 + bob))
    else:
        if is_p1:
            draw_redpanda_avatar(surf, cx, cy, state, anim_t, scale)
        else:
            draw_slime_avatar(surf, cx, cy, state, anim_t, scale)


# ── UI HELPERS ────────────────────────────────────────────────────────────
def _draw_glass_panel(surf, rect, tint=(255,255,255), alpha=30, radius=18,
                      border_col=None, border_w=2, glow=False):
    """Panel kaca semi-transparan dengan glow opsional."""
    x, y, w, h = rect
    # Glow effect
    if glow:
        for i in range(4, 0, -1):
            glow_s = pygame.Surface((w + i*6, h + i*6), pygame.SRCALPHA)
            gc = (*border_col[:3], 20) if border_col else (255,220,50,15)
            pygame.draw.rect(glow_s, gc, (0,0,w+i*6,h+i*6), border_radius=radius+i*2)
            surf.blit(glow_s, (x - i*3, y - i*3))

    panel = pygame.Surface((w, h), pygame.SRCALPHA)
    panel.fill((*tint, alpha))
    surf.blit(panel, (x, y))
    pygame.draw.rect(surf, (255,255,255,40), (x,y,w,h), border_radius=radius)

    if border_col:
        pygame.draw.rect(surf, border_col, rect, border_w, border_radius=radius)

    # Shine strip di atas panel
    shine = pygame.Surface((w, h//4), pygame.SRCALPHA)
    pygame.draw.rect(shine, (255,255,255,25), (0,0,w,h//4), border_radius=radius)
    surf.blit(shine, (x, y))


def _draw_fancy_hp(surf, x, y, hp, max_hp, label, accent):
    """HP bar bergaya RPG dengan glow."""
    bw, bh = 190, 26
    pw = bw + 50  # panel width
    ph = 50

    # Panel background
    _draw_glass_panel(surf, (x, y, pw, ph), tint=(10,20,50),
                      alpha=180, radius=12, border_col=accent, border_w=2)

    # Label
    lbl = fXS.render(label, True, accent)
    surf.blit(lbl, (x+10, y+6))

    # Bar track
    pygame.draw.rect(surf, (20,20,40), (x+10, y+28, bw, bh-8), border_radius=5)

    # Bar fill dengan gradient warna
    filled = int(bw * max(0, hp) / max_hp)
    if filled > 0:
        ratio = hp / max_hp
        if ratio > 0.5:
            col = (60, 220, 80)
        elif ratio > 0.25:
            col = (255, 190, 30)
        else:
            col = (240, 60, 60)
        pygame.draw.rect(surf, col, (x+10, y+28, filled, bh-8), border_radius=5)
        # Highlight strip
        pygame.draw.rect(surf, (255,255,255,80), (x+10, y+28, filled, 4), border_radius=5)

    # HP text
    hp_t = fXS.render(f"❤ {hp}/{max_hp}", True, WHITE)
    surf.blit(hp_t, (x+bw-20, y+28))


def _draw_timer(surf, val, max_val):
    bw = 420
    cx = W//2
    bx = cx - bw//2
    ratio = max(0.0, val/max_val)

    # Background bar
    _draw_glass_panel(surf, (bx-4, 6, bw+8, 30), tint=(0,0,30), alpha=160,
                      radius=10, border_col=(100,100,160), border_w=1)

    # Fill bar
    if ratio > 0:
        filled = int(bw * ratio)
        col = (60,220,80) if ratio > 0.5 else ((255,190,30) if ratio > 0.25 else (240,60,60))
        pygame.draw.rect(surf, col, (bx, 9, filled, 24), border_radius=8)

        # Pulse effect saat kritis
        if ratio < 0.25:
            pulse = abs(math.sin(val * 8)) * 60
            pygame.draw.rect(surf, (*col, int(pulse)),
                             (bx, 9, filled, 24), border_radius=8)

    secs = math.ceil(val)
    t = fS.render(f"⏱ {secs}s", True, WHITE)
    surf.blit(t, t.get_rect(center=(cx, 21)))



def _draw_arrow_badge(surf, direction, cx, cy, col):
    """Gambar badge dengan panah vector. direction: 0=atas,1=bawah,2=kiri,3=kanan"""
    size = 22
    pygame.draw.rect(surf, col, (cx-size//2, cy-size//2, size, size), border_radius=6)
    pygame.draw.rect(surf, WHITE, (cx-size//2, cy-size//2, size, size), 2, border_radius=6)
    # Gambar panah
    if direction == 0:    # atas
        pygame.draw.polygon(surf, WHITE, [(cx, cy-7),(cx-5,cy+4),(cx+5,cy+4)])
    elif direction == 1:  # bawah
        pygame.draw.polygon(surf, WHITE, [(cx, cy+7),(cx-5,cy-4),(cx+5,cy-4)])
    elif direction == 2:  # kiri
        pygame.draw.polygon(surf, WHITE, [(cx-7,cy),(cx+4,cy-5),(cx+4,cy+5)])
    elif direction == 3:  # kanan
        pygame.draw.polygon(surf, WHITE, [(cx+7,cy),(cx-4,cy-5),(cx-4,cy+5)])

def _draw_key_badge(surf, key_str, cx, cy, col, size=36):
    """Key badge premium dengan inner glow."""
    r = pygame.Rect(cx - size//2, cy - size//2, size, size)
    # Shadow
    sh = pygame.Surface((r.w+4, r.h+4), pygame.SRCALPHA)
    pygame.draw.rect(sh, (0,0,0,80), (0,0,r.w+4,r.h+4), border_radius=10)
    surf.blit(sh, (r.x-1, r.y+3))
    # Body
    pygame.draw.rect(surf, col, r, border_radius=8)
    # Top shine
    shine = pygame.Surface((r.w, r.h//2), pygame.SRCALPHA)
    pygame.draw.rect(shine, (255,255,255,60), (0,0,r.w,r.h//2), border_radius=8)
    surf.blit(shine, r.topleft)
    # Border bright
    bright = tuple(min(255, v+80) for v in col[:3])
    pygame.draw.rect(surf, bright, r, 2, border_radius=8)
    # Key label — font khusus badge, bold & compact
    # Untuk arrow symbols, gunakan ukuran yang lebih besar
    is_arrow = key_str in ("↑","↓","←","→")
    font = fKEY if fKEY else fS
    draw_text_center(surf, key_str, font, WHITE, cx, cy, shadow=True)


# ── FANCY BUTTON CLASS ────────────────────────────────────────────────────
class FancyButton:
    def __init__(self, rect, label, color, icon=None):
        self.rect  = pygame.Rect(rect)
        self.label = label
        self.color = color
        self.icon  = icon
        self._hover = False
        self._scale = 1.0
        self._press = 0.0

    def update(self, mx, my):
        self._hover = self.rect.collidepoint(mx, my)
        target = 1.06 if self._hover else 1.0
        self._scale += (target - self._scale) * 0.15
        self._press  = max(0.0, self._press - 0.08)

    def on_click(self, ev):
        if (ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1
                and self.rect.collidepoint(ev.pos)):
            self._press = 1.0
            play_sfx("click")
            return True
        return False

    def draw(self, surf):
        w = int(self.rect.w * self._scale)
        h = int(self.rect.h * self._scale)
        dr = pygame.Rect(self.rect.centerx - w//2,
                         self.rect.centery - h//2 + int(self._press*3), w, h)

        # Glow
        if self._hover:
            for i in range(3, 0, -1):
                gs = pygame.Surface((w+i*8, h+i*8), pygame.SRCALPHA)
                gc = (*self.color[:3], 30//i)
                pygame.draw.rect(gs, gc, (0,0,w+i*8,h+i*8), border_radius=22+i*2)
                surf.blit(gs, (dr.x-i*4, dr.y-i*4))

        # Shadow
        shadow_r = pygame.Rect(dr.x+3, dr.y+5, dr.w, dr.h)
        pygame.draw.rect(surf, (0,0,0,80), shadow_r, border_radius=20)

        # Body gradient (dua rect untuk efek gradient)
        pygame.draw.rect(surf, self.color, dr, border_radius=20)
        dark = tuple(max(0, v-40) for v in self.color[:3])
        grad_top = pygame.Surface((w, h//2), pygame.SRCALPHA)
        pygame.draw.rect(grad_top, (255,255,255,35), (0,0,w,h//2), border_radius=20)
        surf.blit(grad_top, dr.topleft)

        # Border
        bright = tuple(min(255, v+60) for v in self.color[:3])
        pygame.draw.rect(surf, bright, dr, 2, border_radius=20)

        # ── Icon (pygame.draw murni, tidak pakai unicode/emoji) ──
        # Untuk tombol kecil (pause dll) tidak perlu icon
        has_icon = self.icon not in (None, "pause") and dr.w > 140
        if has_icon:
            ix = dr.x + 28
            iy = dr.centery
            # Lingkaran background icon
            pygame.draw.circle(surf, (255,255,255,80), (ix, iy), 14)
            pygame.draw.circle(surf, WHITE, (ix, iy), 14, 2)

            if self.icon == "sword":
                # Pedang diagonal
                pygame.draw.line(surf, (255,230,60), (ix-7,iy+7),(ix+7,iy-7), 3)
                pygame.draw.line(surf, (255,230,60), (ix-7,iy+7),(ix-4,iy+4), 2)
                pygame.draw.rect(surf, WHITE, (ix+3,iy-9,4,4))
            elif self.icon == "info":
                # Huruf i
                pygame.draw.circle(surf, WHITE, (ix, iy-5), 2)
                pygame.draw.rect(surf, WHITE, (ix-2, iy-1, 4, 9))
            elif self.icon == "home":
                # Rumah sederhana
                pygame.draw.polygon(surf, WHITE, [(ix,iy-8),(ix-8,iy-1),(ix+8,iy-1)], 0)
                pygame.draw.rect(surf, WHITE, (ix-5,iy-1,10,9))
                pygame.draw.rect(surf, self.color, (ix-2,iy+1,4,7))
            elif self.icon == "exit":
                # X
                pygame.draw.line(surf, WHITE, (ix-5,iy-5),(ix+5,iy+5), 3)
                pygame.draw.line(surf, WHITE, (ix+5,iy-5),(ix-5,iy+5), 3)
            elif self.icon == "next":
                # Segitiga play kanan
                pygame.draw.polygon(surf, WHITE, [(ix-5,iy-7),(ix-5,iy+7),(ix+8,iy)])
            elif self.icon == "restart":
                # Lingkaran panah restart
                import math as _m
                for a in range(30, 300, 20):
                    ra = _m.radians(a)
                    pygame.draw.circle(surf, WHITE,
                        (ix+int(8*_m.cos(ra)), iy+int(8*_m.sin(ra))), 2)
                pygame.draw.polygon(surf, WHITE, [(ix+8,iy-5),(ix+8,iy+5),(ix+14,iy)])

        # Untuk tombol pause (kecil, hanya ikon)
        if self.icon == "pause":
            ix, iy = dr.centerx, dr.centery
            pygame.draw.rect(surf, WHITE, (ix-6, iy-8, 4, 16))
            pygame.draw.rect(surf, WHITE, (ix+2, iy-8, 4, 16))
            lx = dr.centerx
        else:
            lx = dr.centerx + (14 if has_icon else 0)

        # ── Label ──
        draw_text_center(surf, self.label, fM, WHITE, lx, dr.centery)


# ── SCENE: MENU ───────────────────────────────────────────────────────────
def render_menu(screen, gs, buttons):
    _draw_bg(screen, "menu", gs.anim_time)

    # Overlay gelap di bagian tengah bawah
    screen.blit(_get_overlay(W, 220, (0,0,20,140)), (0, H-220))

    # Karakter di kiri dan kanan
    _draw_char(screen, True,  160, H-130, "idle", gs.anim_time, 1.3)
    _draw_char(screen, False, W-160, H-130, "idle", gs.anim_time, 1.3)

    # Logo / Title
    if HAS_LOGO and logo_img:
        lr = logo_img.get_rect(center=(W//2, 185))
        screen.blit(logo_img, lr)
    else:
        # Teks judul fancy
        _draw_glass_panel(screen, (W//2-260, 60, 520, 110),
                          tint=(10,20,80), alpha=200, radius=20,
                          border_col=GOLD, border_w=3, glow=True)
        draw_text_center(screen, "ENGLISH", fXL, GOLD, W//2, 100)
        draw_text_center(screen, "BATTLE PETS", fXL, WHITE, W//2, 145)

    # Subtitle badge
    sub_surf = fS.render("✦  2 PLAYER EDITION  ✦", True, NEON_CYAN)
    sub_r = sub_surf.get_rect(center=(W//2, 368))
    _draw_glass_panel(screen, (sub_r.x-16, sub_r.y-6, sub_r.w+32, sub_r.h+12),
                      tint=(0,40,80), alpha=180, radius=10, border_col=NEON_CYAN, border_w=1)
    screen.blit(sub_surf, sub_r)

    # Key hint mini di bawah subtitle
    hint = fXS.render("P1: Z X C V  │  P2: ↑ ↓ ← →", True, CREAM)
    screen.blit(hint, hint.get_rect(center=(W//2, 393)))

    # Buttons
    for b in buttons:
        b.draw(screen)


# ── SCENE: HOW TO PLAY ────────────────────────────────────────────────────
def render_howto(screen, gs, btn_back):
    _draw_bg(screen, "menu", gs.anim_time)

    # Panel utama
    px, py, pw, ph = W//2-330, 40, 660, 550
    _draw_glass_panel(screen, (px,py,pw,ph), tint=(5,15,50),
                      alpha=220, radius=22, border_col=GOLD, border_w=3, glow=True)

    draw_text_center(screen, "⚔  HOW TO PLAY  ⚔", fL, GOLD, W//2, 88)

    # Divider
    pygame.draw.line(screen, GOLD, (px+30, 112), (px+pw-30, 112), 2)

    sections = [
        ("RULES", [
            ("Jawab soal Bahasa Inggris lebih cepat & benar!", CREAM),
            ("Siapa PERTAMA jawab benar → serang musuh  -1 ❤", CREAM),
            ("Keduanya salah → tidak ada yang diserang", (200,200,100)),
            ("Timer 15 detik — habis tanpa jawaban → lanjut soal", (200,200,100)),
            ("HP habis duluan = KALAH!", UI_RED),
        ]),
    ]

    y = 132
    for title, items in sections:
        _draw_glass_panel(screen, (px+20, y, pw-40, 26),
                          tint=(50,30,0), alpha=140, radius=8, border_col=GOLD_DK, border_w=1)
        draw_text_center(screen, title, fS, GOLD, W//2, y+13, shadow=False)
        y += 36
        for text, col in items:
            t = fXS.render(f"  •  {text}", True, col)
            screen.blit(t, (px+40, y))
            y += 24
        y += 10

    # Control cards P1 & P2
    for pi, (pname, pcol, keys, arrows) in enumerate([
        ("PLAYER 1 — LEXI", P1_COL, ["Z","X","C","V"], ["A","B","C","D"]),
        ("PLAYER 2 — SLIME", P2_COL, ["↑","↓","←","→"], ["A","B","C","D"]),
    ]):
        cx = px + 30 + pi * (pw//2 - 20)
        _draw_glass_panel(screen, (cx, y, pw//2-50, 100),
                          tint=(20,20,60), alpha=180, radius=14, border_col=pcol, border_w=2)
        draw_text_center(screen, pname, fXS, pcol, cx + (pw//2-50)//2, y+16, shadow=False)
        for ki, (k, a) in enumerate(zip(keys, arrows)):
            kx = cx + 18 + ki * 36
            _draw_key_badge(screen, k, kx+18, y+56, pcol, size=30)
            t = fXS.render(a, True, CREAM)
            screen.blit(t, t.get_rect(center=(kx+18, y+82)))

    btn_back.draw(screen)


# ── SCENE: GAME ───────────────────────────────────────────────────────────
def render_game(screen, gs, btn_next, btn_pause):
    from constants import TOTAL_HP, ROUND_TIMER

    _draw_bg(screen, "game", gs.anim_time)

    # ── Karakter ──
    _draw_char(screen, True,  145, H-108, gs.p1_state, gs.anim_time, 1.6)
    _draw_char(screen, False, W-145, H-108, gs.p2_state, gs.anim_time, 1.6)

    # ── Proyektil & Partikel ──
    if gs.proj:
        gs.proj.draw(screen)
    for p in gs.particles:
        p.draw(screen)

    # ── HP Bars ──
    _draw_fancy_hp(screen, 6, 40, gs.p1_hp, TOTAL_HP, "P1  LEXI", P1_COL)
    _draw_fancy_hp(screen, W-246, 40, gs.p2_hp, TOTAL_HP, "P2  SLIME", P2_COL)

    # ── Score chips ──
    for label, score, color, sx in [
        (f"★ {gs.p1_score} pts", gs.p1_score, P1_COL, 120),
        (f"★ {gs.p2_score} pts", gs.p2_score, P2_COL, W-120),
    ]:
        _draw_glass_panel(screen, (sx-48, 96, 96, 26),
                          tint=color, alpha=160, radius=8, border_col=color, border_w=1)
        draw_text_center(screen, label, fXS, WHITE, sx, 109, shadow=False)

    # ── Q counter ──
    qtext = f"Q {gs.current_q+1} / {len(gs.questions)}"
    qt = fS.render(qtext, True, WHITE)
    qr = qt.get_rect(center=(W//2, 46))
    _draw_glass_panel(screen, (qr.x-12, qr.y-4, qr.w+24, qr.h+8),
                      tint=(0,0,30), alpha=160, radius=10)
    screen.blit(qt, qr)

    # ── Timer ──
    if not gs.answered:
        _draw_timer(screen, gs.round_timer, ROUND_TIMER)

    # ── Panel Soal ──
    PANEL_W = 500
    PANEL_X = W//2 - PANEL_W//2
    PANEL_Y = 100
    PANEL_H = 395

    # Panel soal — background solid terang supaya teks opsi terbaca
    pygame.draw.rect(screen, PANEL_BG, (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), border_radius=18)
    pygame.draw.rect(screen, PANEL_BORDER, (PANEL_X, PANEL_Y, PANEL_W, PANEL_H), 3, border_radius=18)

    # Teks soal
    q_data  = gs.questions[gs.current_q]
    q_lines = wrap_text(fM, q_data["q"], PANEL_W - 40)
    for i, line in enumerate(q_lines):
        draw_text_center(screen, line, fM, Q_TEXT_COL, W//2, PANEL_Y+34 + i*30, shadow=False)

    # ── Opsi Jawaban ──
    P1_KEYS_LABELS = ["Z","X","C","V"]
    P2_KEYS_LABELS = ["UP","DN","LT","RT"]

    OPT_W   = 330
    OPT_X   = W//2 - OPT_W//2
    OPT_H   = 44
    BADGE_W = 44
    GAP     = 8

    for i, opt in enumerate(q_data["opts"]):
        oy = PANEL_Y + 105 + i * 56
        r  = pygame.Rect(OPT_X, oy, OPT_W, OPT_H)

        # Warna opsi — solid background terang supaya teks gelap terbaca jelas
        if gs.answered:
            correct = q_data["ans"]
            if i == correct:
                bg_col, border_col, txt_col = OPT_BG_CORRECT, OPT_BORDER_CORRECT, OPT_TEXT_CORRECT
            else:
                bg_col, border_col, txt_col = OPT_BG_WRONG, OPT_BORDER_WRONG, OPT_TEXT_WRONG
        else:
            bg_col, border_col, txt_col = OPT_BG_DEFAULT, OPT_BORDER_DEFAULT, OPT_TEXT_DEFAULT

        pygame.draw.rect(screen, bg_col, r, border_radius=12)
        pygame.draw.rect(screen, border_col, r, 2, border_radius=12)

        # Highlight border P1/P2
        if gs.p1_choice == i:
            pygame.draw.rect(screen, P1_COL, r.inflate(6,6), 3, border_radius=14)
        if gs.p2_choice == i:
            pygame.draw.rect(screen, P2_COL, r.inflate(6,6), 3, border_radius=14)

        # Teks opsi — font tidak bold, warna gelap, tanpa outline (panel sudah terang)
        opt_clean = opt[3:] if len(opt)>3 and opt[1]=="." else opt
        draw_text_center(screen, opt_clean, fOPT, txt_col, W//2, oy + OPT_H//2, shadow=False)

        # Badge P1 kiri
        bx1 = OPT_X - BADGE_W - GAP
        bcol1 = P1_COL
        if gs.answered:
            bcol1 = UI_GREEN if i==q_data["ans"] else (40,60,120)
        _draw_key_badge(screen, P1_KEYS_LABELS[i], bx1 + BADGE_W//2, oy + OPT_H//2, bcol1)

        # Badge P2 kanan — gambar panah vector
        bx2 = OPT_X + OPT_W + GAP
        bcol2 = P2_COL
        if gs.answered:
            bcol2 = UI_GREEN if i==q_data["ans"] else (120,60,20)
        _draw_arrow_badge(screen, i, bx2 + BADGE_W//2, oy + OPT_H//2, bcol2)

    # ── Banner & Penjelasan setelah dijawab ──
    if gs.answered and gs.proj is None:
        if gs.winner == "p1":
            banner, bcol = "P1 CORRECT!", P1_COL
        elif gs.winner == "p2":
            banner, bcol = "P2 CORRECT!", P2_COL
        else:
            banner, bcol = "TIME UP / NO ANSWER", (160, 140, 30)

        # ── Penjelasan di dalam panel, setelah opsi ──
        exp_y = PANEL_Y + PANEL_H - 62

        # Strip tipis explanation di bagian bawah panel
        exp_bg = pygame.Surface((PANEL_W - 20, 52), pygame.SRCALPHA)
        exp_bg.fill((*bcol[:3], 28))
        screen.blit(exp_bg, (PANEL_X + 10, exp_y))
        pygame.draw.rect(screen, bcol, (PANEL_X+10, exp_y, PANEL_W-20, 52), 2, border_radius=8)

        # Nama pemenang kecil di kiri strip
        winner_t = fXS.render(banner, True, bcol)
        screen.blit(winner_t, (PANEL_X+18, exp_y+4))

        # Teks penjelasan
        exp_clean = q_data["exp"] if q_data["exp"] else ""
        exp_lines = wrap_text(fXS, exp_clean, PANEL_W - 30)
        for li, line in enumerate(exp_lines[:2]):   # max 2 baris
            draw_text_center(screen, line, fXS, Q_TEXT_COL,
                             W//2, exp_y + 20 + li*16, shadow=False)

        btn_next.draw(screen)

    # ── Exit battle button (pojok kanan bawah) ──
    btn_pause.draw(screen)

    # ── Key hint strip bawah ──
    hint_y = H - 18
    for i, lbl in enumerate(["Z","X","C","V"]):
        _draw_key_badge(screen, lbl, 22 + i*38, hint_y, P1_COL, size=30)
    for i in range(4):
        _draw_arrow_badge(screen, i, W-136 + i*38, hint_y, P2_COL)


# ── SCENE: RESULT ─────────────────────────────────────────────────────────
# ── PAUSE MENU ────────────────────────────────────────────────────────────
def render_pause(screen, gs, btn_resume, btn_restart_pause, btn_quit_pause):
    """Overlay pause menu di atas game."""
    # Dim overlay
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    # Panel
    pw, ph = 340, 280
    px, py = W//2 - pw//2, H//2 - ph//2
    pygame.draw.rect(screen, (30, 22, 12), (px, py, pw, ph), border_radius=20)
    pygame.draw.rect(screen, PAL_GOLD, (px, py, pw, ph), 3, border_radius=20)

    # Header
    pygame.draw.rect(screen, PAL_BROWN, (px, py, pw, 56), border_radius=20)
    pygame.draw.rect(screen, PAL_BROWN, (px, py+36, pw, 20))
    # Ikon pause (dua garis vertikal)
    pix, piy = W//2 - 52, py+28
    pygame.draw.rect(screen, PAL_GOLD, (pix,    piy-12, 7, 24))
    pygame.draw.rect(screen, PAL_GOLD, (pix+11, piy-12, 7, 24))
    draw_text_center(screen, "PAUSED", fL, PAL_GOLD, W//2+10, py+28)

    draw_text_center(screen, "Game is paused", fXS, (200, 190, 170), W//2, py+80)

    btn_resume.draw(screen)
    btn_restart_pause.draw(screen)
    btn_quit_pause.draw(screen)


def render_gameover(screen, gs, btn_restart_go, btn_home_go):
    """Layar Game Over ketika HP salah satu habis."""
    _draw_bg(screen, "result", gs.anim_time)
    draw_confetti(screen)

    overall = gs.get_overall_winner()
    t = gs.anim_time

    if overall == "p1":
        win_col, win_label, win_char = P1_COL, "Player 1 Wins!", True
    elif overall == "p2":
        win_col, win_label, win_char = P2_COL, "Player 2 Wins!", False
    else:
        win_col, win_label, win_char = PAL_GOLD, "It's a Draw!", None

    # Panel
    px, py, pw, ph = W//2 - 270, 45, 540, 570
    pygame.draw.rect(screen, (255, 252, 240), (px, py, pw, ph), border_radius=22)
    pygame.draw.rect(screen, win_col, (px, py, pw, ph), 4, border_radius=22)

    # Glow
    for gi in range(3, 0, -1):
        gs2 = pygame.Surface((pw+gi*10, ph+gi*10), pygame.SRCALPHA)
        pygame.draw.rect(gs2, (*win_col[:3], 22*gi), (0,0,pw+gi*10,ph+gi*10), border_radius=24+gi*3)
        screen.blit(gs2, (px-gi*5, py-gi*5))

    # Header strip
    pygame.draw.rect(screen, win_col, (px, py, pw, 94), border_radius=22)
    pygame.draw.rect(screen, win_col, (px, py+22, pw, 72))

    # Teks header
    draw_text_center(screen, "GAME OVER!", fXL, WHITE, W//2, py+38)
    draw_text_center(screen, win_label,    fL,  (255,245,180), W//2, py+74)

    # Karakter
    char_y = py + 258
    bounce = int(abs(math.sin(t * 4)) * 16)
    if win_char is None:
        _draw_char(screen, True,  W//2-90, char_y-bounce, "win", t, 1.3)
        _draw_char(screen, False, W//2+90, char_y-bounce, "win", t, 1.3)
    else:
        _draw_char(screen, win_char, W//2, char_y-bounce, "win", t, 1.7)

    # Stars
    for si in range(5):
        angle = t*2.5 + si*(2*math.pi/5)
        sx = W//2 + int(math.cos(angle)*78)
        sy = char_y-30 + int(math.sin(angle)*32)
        sa = int(180+75*math.sin(t*3+si))
        ss = pygame.Surface((14,14), pygame.SRCALPHA)
        pygame.draw.circle(ss, (*PAL_GOLD, sa), (7,7), 6)
        screen.blit(ss, (sx-7, sy-7))

    # Divider
    div_y = py + 340
    pygame.draw.line(screen, win_col, (px+30, div_y), (px+pw-30, div_y), 2)
    lbl = fXS.render("S C O R E B O A R D", True, win_col)
    screen.blit(lbl, lbl.get_rect(center=(W//2, div_y-14)))

    # Score cards
    cards = [
        ("P1  LEXI",  gs.p1_hp, gs.p1_score, P1_COL, overall=="p1"),
        ("P2  SLIME", gs.p2_hp, gs.p2_score, P2_COL, overall=="p2"),
    ]
    for row, (name, hp, score, col, is_winner) in enumerate(cards):
        ry = div_y + 18 + row*72
        rw = pw - 60; rx = px + 30
        bg_c = (255,250,225) if is_winner else (245,242,230)
        pygame.draw.rect(screen, bg_c, (rx, ry, rw, 58), border_radius=12)
        bc = col if is_winner else (180,170,150)
        pygame.draw.rect(screen, bc, (rx, ry, rw, 58), 3 if is_winner else 1, border_radius=12)
        if is_winner:
            cr = fL.render("👑", True, PAL_GOLD)
            screen.blit(cr, (rx+8, ry+10))
        nt = fS.render(name, True, col)
        screen.blit(nt, (rx+(44 if is_winner else 12), ry+8))
        pip_x = rx+(44 if is_winner else 12)
        for i in range(TOTAL_HP):
            from constants import TOTAL_HP as THP
            pip_c = col if i < hp else (200,190,180)
            pygame.draw.circle(screen, pip_c, (pip_x+i*22, ry+38), 8)
            if i < hp:
                pygame.draw.circle(screen, WHITE, (pip_x+i*22-3, ry+35), 3)
        st = fL.render(f"{score} pts", True, (40,30,20))
        screen.blit(st, st.get_rect(right=rx+rw-14, centery=ry+29))

    btn_restart_go.draw(screen)
    btn_home_go.draw(screen)


def render_result(screen, gs, btn_home, btn_restart_result):
    _draw_bg(screen, "result", gs.anim_time)

    # ── Confetti VFX di belakang panel ──
    draw_confetti(screen)

    overall = gs.get_overall_winner()
    t       = gs.anim_time

    # Tentukan warna tema & nama pemenang
    if overall == "p1":
        win_col   = P1_COL
        win_label = "Player 1 Wins!"
        win_char  = True    # is_p1
        is_draw   = False
    elif overall == "p2":
        win_col   = P2_COL
        win_label = "Player 2 Wins!"
        win_char  = False
        is_draw   = False
    else:
        win_col   = PAL_GOLD
        win_label = "Great Match!"
        win_char  = None
        is_draw   = True

    # ── Panel utama — putih hangat dengan border warna pemenang ──
    px, py, pw, ph = W//2 - 260, 50, 520, 560
    pygame.draw.rect(screen, (255, 252, 240), (px, py, pw, ph), border_radius=22)
    pygame.draw.rect(screen, win_col, (px, py, pw, ph), 4, border_radius=22)

    # Glow panel border
    for gi in range(3, 0, -1):
        gs_surf = pygame.Surface((pw+gi*10, ph+gi*10), pygame.SRCALPHA)
        gc = (*win_col[:3], 25 * gi)
        pygame.draw.rect(gs_surf, gc, (0,0,pw+gi*10,ph+gi*10), border_radius=24+gi*3)
        screen.blit(gs_surf, (px-gi*5, py-gi*5))

    # ── Header strip warna pemenang di atas panel ──
    header_h = 90
    header_surf = pygame.Surface((pw, header_h), pygame.SRCALPHA)
    header_surf.fill((*win_col[:3], 40))
    screen.blit(header_surf, (px, py))
    pygame.draw.rect(screen, win_col, (px, py, pw, header_h), 0, border_radius=22)
    # Rounded hanya sudut atas
    pygame.draw.rect(screen, win_col, (px, py+22, pw, header_h-22))

    # ── Teks VICTORY / DRAW ──
    if is_draw:
        draw_text_center(screen, "DRAW!", fXL, WHITE, W//2, py+38)
        draw_text_center(screen, win_label, fL, (255,245,180), W//2, py+72)
    else:
        draw_text_center(screen, "VICTORY!", fXL, WHITE, W//2, py+38)
        draw_text_center(screen, win_label, fL, (255,245,180), W//2, py+72)

    # ── Karakter pemenang (lebih besar, bouncing animasi) ──
    char_y = py + 250
    bounce  = int(abs(math.sin(t * 4)) * 18)
    if is_draw:
        _draw_char(screen, True,  W//2 - 90, char_y - bounce, "win", t, 1.3)
        _draw_char(screen, False, W//2 + 90, char_y - bounce, "win", t, 1.3)
    else:
        _draw_char(screen, win_char, W//2, char_y - bounce, "win", t, 1.7)

    # ── Stars animasi berputar di sekitar karakter ──
    for si in range(5):
        angle  = t * 2.5 + si * (2 * math.pi / 5)
        sx     = W//2 + int(math.cos(angle) * 75)
        sy     = char_y - 30 + int(math.sin(angle) * 30)
        star_a = int(180 + 75 * math.sin(t * 3 + si))
        star_s = pygame.Surface((14, 14), pygame.SRCALPHA)
        pygame.draw.circle(star_s, (*PAL_GOLD, star_a), (7, 7), 6)
        screen.blit(star_s, (sx - 7, sy - 7))

    # ── Divider ──
    div_y = py + 330
    pygame.draw.line(screen, win_col, (px+30, div_y), (px+pw-30, div_y), 2)
    div_label = fXS.render("S C O R E B O A R D", True, win_col)
    screen.blit(div_label, div_label.get_rect(center=(W//2, div_y - 14)))

    # ── Score cards — solid dengan teks gelap ──
    cards = [
        ("P1  LEXI",  gs.p1_hp, gs.p1_score, P1_COL,  overall == "p1"),
        ("P2  SLIME", gs.p2_hp, gs.p2_score, P2_COL,  overall == "p2"),
    ]
    for row, (name, hp, score, col, is_winner) in enumerate(cards):
        ry  = div_y + 18 + row * 72
        rw  = pw - 60
        rx  = px + 30

        # Background card
        bg_c = (245, 242, 230) if not is_winner else (255, 250, 225)
        pygame.draw.rect(screen, bg_c, (rx, ry, rw, 58), border_radius=12)
        border_c = col if is_winner else (180, 170, 150)
        bw = 3 if is_winner else 1
        pygame.draw.rect(screen, border_c, (rx, ry, rw, 58), bw, border_radius=12)

        # Crown emoji kalau menang
        if is_winner:
            crown = fL.render("👑", True, PAL_GOLD)
            screen.blit(crown, (rx + 8, ry + 10))

        # Nama player
        name_t = fS.render(name, True, col)
        screen.blit(name_t, (rx + (44 if is_winner else 12), ry + 8))

        # HP pips
        pip_x = rx + (44 if is_winner else 12)
        pip_y = ry + 34
        for i in range(TOTAL_HP):
            pip_col = col if i < hp else (200, 190, 180)
            pygame.draw.circle(screen, pip_col, (pip_x + i * 22, pip_y), 8)
            if i < hp:
                pygame.draw.circle(screen, WHITE, (pip_x + i * 22 - 3, pip_y - 3), 3)

        # Score pts
        score_t = fL.render(f"{score} pts", True, (40, 30, 20))
        screen.blit(score_t, score_t.get_rect(right=rx+rw-14, centery=ry+29))

    btn_restart_result.draw(screen)
    btn_home.draw(screen)
