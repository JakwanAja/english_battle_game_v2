"""
main.py — Entry point English Battle Pets 2 Player
Jalankan: python main.py
"""

import pygame
import sys

# ── INIT ────────────────────────────────────────────────────────────────
pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

from constants import W, H, FPS, UI_GREEN, UI_ORANGE, UI_RED, UI_BLUE_LT
from constants import P1_COL, P2_COL, GOLD, TOTAL_HP, init_controls
init_controls()

from visuals import init_fonts
init_fonts()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("English Battle Pets — 2 Player")
clock  = pygame.time.Clock()

# ── ASSETS ──────────────────────────────────────────────────────────────
from scenes import load_assets, play_music, play_sfx, FancyButton, reset_confetti, update_confetti
load_assets()
play_music("menu")

from game_state import GameStateManager
from constants  import P1_KEYS, P2_KEYS

gs = GameStateManager()

# ── BUTTONS ─────────────────────────────────────────────────────────────
# Menu buttons — posisi disesuaikan dengan logo portrait (tinggi ~420px)
btn_menu = [
    FancyButton((W//2 - 130, 418, 260, 52), "PLAY",         (30,140,60),  "sword"),
    FancyButton((W//2 - 130, 480, 260, 52), "HOW TO PLAY",  (30,90,170),  "info"),
    FancyButton((W//2 - 130, 542, 260, 52), "EXIT",         (160,40,40),  "exit"),
]

# In-game buttons
btn_next         = FancyButton((W//2 - 110, H - 58, 220, 46), "NEXT  ▶",   (30,100,200), "next")
btn_exit_battle  = FancyButton((W - 145,    H - 58, 138, 40), "EXIT",      (140,40,40),  "exit")

# Howto back
btn_back = FancyButton((W//2 - 110, H - 58, 220, 46), "← BACK", (80,50,160), "home")

# Result home
btn_home = FancyButton((W//2 - 110, H - 58, 220, 46), "HOME ⌂",  (30,100,200), "home")

# ── MAIN LOOP ────────────────────────────────────────────────────────────
while True:
    dt = clock.tick(FPS) / 1000.0
    mx, my = pygame.mouse.get_pos()

    prev_scene = gs.scene
    gs.update(dt)

    # Auto-trigger result music + confetti
    if gs.scene != prev_scene and gs.scene == "result":
        play_music("result")
        reset_confetti()

    # Update confetti VFX
    if gs.scene == "result":
        update_confetti(dt)

    # ── EVENTS ──
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # ── ESC selalu tersedia ──
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if gs.scene == "game":
                gs.scene = "menu"
                play_music("menu")
            elif gs.scene in ("howto", "result"):
                gs.scene = "menu"
                play_music("menu")

        # ── MENU ──
        if gs.scene == "menu":
            for b in btn_menu:
                if b.on_click(ev):
                    if b.label == "PLAY":
                        gs.reset_match()
                        gs.scene = "game"
                        play_music("battle")
                    elif b.label == "HOW TO PLAY":
                        gs.scene = "howto"
                    elif b.label == "EXIT":
                        pygame.quit(); sys.exit()

        # ── HOW TO PLAY ──
        elif gs.scene == "howto":
            if btn_back.on_click(ev):
                gs.scene = "menu"

        # ── GAME ──
        elif gs.scene == "game":
            # Exit battle button
            if btn_exit_battle.on_click(ev):
                gs.scene = "menu"
                play_music("menu")

            if not gs.answered:
                if ev.type == pygame.KEYDOWN:
                    # P1: Z X C V
                    for idx, key in enumerate(P1_KEYS):
                        if ev.key == key:
                            gs.register_answer("p1", idx)
                            break
                    # P2: ↑↓←→
                    for idx, key in enumerate(P2_KEYS):
                        if ev.key == key:
                            gs.register_answer("p2", idx)
                            break
            else:
                # NEXT
                if gs.proj is None:
                    if btn_next.on_click(ev):
                        gs.next_question()
                    if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        gs.next_question()

        # ── RESULT ──
        elif gs.scene == "result":
            if btn_home.on_click(ev):
                gs.scene = "menu"
                play_music("menu")
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                gs.scene = "menu"
                play_music("menu")

    # ── HOVER UPDATE ──
    if gs.scene == "menu":
        for b in btn_menu: b.update(mx, my)
    elif gs.scene == "howto":
        btn_back.update(mx, my)
    elif gs.scene == "game":
        btn_exit_battle.update(mx, my)
        if gs.answered and gs.proj is None:
            btn_next.update(mx, my)
    elif gs.scene == "result":
        btn_home.update(mx, my)

    # ── RENDER ──
    from scenes import render_menu, render_howto, render_game, render_result

    if gs.scene == "menu":
        render_menu(screen, gs, btn_menu)
    elif gs.scene == "howto":
        render_howto(screen, gs, btn_back)
    elif gs.scene == "game":
        render_game(screen, gs, btn_next, btn_exit_battle)
    elif gs.scene == "result":
        render_result(screen, gs, btn_home)

    pygame.display.flip()
