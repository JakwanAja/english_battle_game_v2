"""
objects.py — Game objects: Particle, Projectile, UI_IconButton
"""

import pygame
import math
import random
from constants import *
from visuals import draw_rounded_panel, draw_text_center


# ── PARTICLE ────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, col):
        self.x, self.y = float(x), float(y)
        self.col = col
        self.vx  = random.uniform(-4, 4)
        self.vy  = random.uniform(-6, -1)
        self.life = self.max_life = random.uniform(0.4, 1.0)
        self.size = random.uniform(4, 8)

    def update(self, dt):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += 0.2          # gravity
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        ratio = max(0, self.life / self.max_life)
        sz    = max(1, int(self.size * ratio))
        pygame.draw.circle(surf, self.col, (int(self.x), int(self.y)), sz)


# ── PROJECTILE ───────────────────────────────────────────────────────────
class Projectile:
    def __init__(self, x, y, tx, ty, col):
        self.x,  self.y  = float(x), float(y)
        self.tx, self.ty = float(tx), float(ty)
        self.col  = col
        self.hit  = False
        self.trail = []

        dx, dy = tx - x, ty - y
        dist   = math.hypot(dx, dy) or 1
        speed  = 600.0
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def update(self, dt):
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:
            self.trail.pop(0)
        self.x += self.vx * dt
        self.y += self.vy * dt
        if math.hypot(self.tx - self.x, self.ty - self.y) < 25:
            self.hit = True

    def draw(self, surf):
        from visuals import fXS
        for i, (ptx, pty) in enumerate(self.trail):
            ratio = i / max(1, len(self.trail))
            sz    = max(1, int(7 * ratio))
            c     = tuple(int(v * ratio * 0.5) for v in self.col)
            pygame.draw.circle(surf, c, (ptx, pty), sz)
        bx, by = int(self.x), int(self.y)
        draw_rounded_panel(surf, (bx - 12, by - 14, 24, 22), self.col,
                           radius=4, border_color=WHITE, border_w=2)
        draw_text_center(surf, "A", fXS, WHITE, bx, by - 3, shadow=False)


# ── UI BUTTON ────────────────────────────────────────────────────────────
class UI_IconButton:
    def __init__(self, rect, label, base_col, icon_type, font=None):
        self.r         = pygame.Rect(rect)
        self.label     = label
        self.base_col  = base_col
        self.icon_type = icon_type
        self._font     = font   # None = use fM lazily
        self.hover     = False
        self.scale     = 1.0

    @property
    def font(self):
        if self._font:
            return self._font
        from visuals import fM
        return fM

    def update(self, mx, my):
        self.hover  = self.r.collidepoint(mx, my)
        self.scale += ((1.05 if self.hover else 1.0) - self.scale) * 0.2

    def draw(self, surf):
        w  = int(self.r.w * self.scale)
        h  = int(self.r.h * self.scale)
        dr = pygame.Rect(self.r.centerx - w // 2, self.r.centery - h // 2, w, h)

        # Shadow
        pygame.draw.rect(surf, (15, 30, 20),
                         (dr.x, dr.y + 4, dr.w, dr.h), border_radius=20)
        col = tuple(min(255, v + 30) for v in self.base_col) if self.hover else self.base_col
        pygame.draw.rect(surf, col, dr, border_radius=20)

        # Shine
        shine = pygame.Surface((dr.w, dr.h // 2), pygame.SRCALPHA)
        shine.fill((255, 255, 255, 40))
        surf.blit(shine, dr.topleft)
        pygame.draw.rect(surf, WHITE, dr, 2, border_radius=20)

        draw_text_center(surf, self.label, self.font, WHITE, dr.centerx + 10, dr.centery)

        # Icon
        ix, iy = dr.x + 30, dr.centery
        pygame.draw.circle(surf, CREAM, (ix, iy), 14)
        if self.icon_type == "sword":
            pygame.draw.line(surf, BLACK,   (ix - 6, iy + 6), (ix + 6, iy - 6), 3)
            pygame.draw.line(surf, GOLD_DK, (ix - 8, iy + 2), (ix - 2, iy + 8), 3)
        elif self.icon_type == "info":
            pygame.draw.line(surf, BLACK, (ix, iy - 2), (ix, iy + 6), 3)
            pygame.draw.circle(surf, BLACK, (ix, iy - 6), 2)
        elif self.icon_type == "door":
            pygame.draw.rect(surf, BLACK, (ix - 6, iy - 8, 12, 16), 2)
            pygame.draw.circle(surf, BLACK, (ix + 2, iy), 2)
        elif self.icon_type == "person":
            pygame.draw.circle(surf, BLACK, (ix, iy - 5), 4)
            pygame.draw.line(surf, BLACK, (ix, iy - 1), (ix, iy + 6), 2)
            pygame.draw.line(surf, BLACK, (ix - 4, iy + 2), (ix + 4, iy + 2), 2)

    def is_clicked(self, ev):
        return (ev.type == pygame.MOUSEBUTTONDOWN
                and ev.button == 1
                and self.r.collidepoint(ev.pos))
