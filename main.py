"""
main.py — Entry point English Battle Pets 2 Player
"""

import pygame, sys, math

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
pygame.display.set_caption("English Battle Pets - 2 Player")
clock  = pygame.time.Clock()

# ── ASSETS ──────────────────────────────────────────────────────────────
from scenes import (load_assets, play_music, play_sfx,
                    FancyButton, reset_confetti, update_confetti)
load_assets()
play_music("menu")

from game_state import GameStateManager
from constants  import P1_KEYS, P2_KEYS

gs = GameStateManager()

# ── BUTTONS ─────────────────────────────────────────────────────────────
CX = W//2

# Menu
btn_menu = [
    FancyButton((CX-130, 418, 260, 52), "PLAY",        (30,140,60),  "sword"),
    FancyButton((CX-130, 480, 260, 52), "HOW TO PLAY", (30,90,170),  "info"),
    FancyButton((CX-130, 542, 260, 52), "EXIT",        (160,40,40),  "exit"),
]

# Howto
btn_back = FancyButton((CX-110, H-58, 220, 46), "BACK", (80,50,160), "home")

# Battle in-game
btn_next        = FancyButton((CX-110, H-58, 220, 46), "NEXT",  (30,100,200), "next")
btn_pause       = FancyButton((W-58,   10,    46,  40), "",         (60,55,45),   "pause")

# Pause overlay
btn_resume      = FancyButton((CX-120, H//2- 30, 240, 48), "RESUME",  (30,140,60),  "sword")
btn_restart_p   = FancyButton((CX-120, H//2+ 30, 240, 48), "RESTART", (30,90,170),  "home")
btn_quit_pause  = FancyButton((CX-120, H//2+ 90, 240, 48), "QUIT",    (160,40,40),  "exit")

# Result
btn_home           = FancyButton((CX+10,  H-58, 160, 46), "HOME",    (30,100,200), "home")
btn_restart_result = FancyButton((CX-175, H-58, 160, 46), "RESTART", (30,140,60),  "sword")

# Game Over
btn_restart_go  = FancyButton((CX+10,  H-58, 160, 46), "RESTART", (30,140,60),  "sword")
btn_home_go     = FancyButton((CX-175, H-58, 160, 46), "HOME",    (30,100,200), "home")

# ── SCENE: "menu","howto","game","pause","gameover","result" ─────────────
paused = False   # flag pause overlay

def do_restart():
    """Reset match dan kembali ke game."""
    global paused
    paused = False
    gs.reset_match()
    gs.scene = "game"
    play_music("battle")
    reset_confetti()   # clear confetti kalau ada sisa

def do_home():
    global paused
    paused = False
    gs.scene = "menu"
    play_music("menu")

# ── MAIN LOOP ────────────────────────────────────────────────────────────
prev_scene = gs.scene

while True:
    dt = clock.tick(FPS) / 1000.0
    if paused:
        dt = 0.0   # freeze game logic saat pause

    mx, my = pygame.mouse.get_pos()

    prev_scene = gs.scene
    if not paused:
        gs.update(dt)

    # Trigger music/confetti saat masuk result atau gameover
    if gs.scene != prev_scene:
        if gs.scene in ("result", "gameover"):
            play_music("result")
            reset_confetti()

    # Update confetti VFX
    if gs.scene in ("result", "gameover") and not paused:
        update_confetti(dt)

    # ── EVENTS ──────────────────────────────────────────────────────────
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # ESC: toggle pause saat game, atau back ke menu
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if gs.scene == "game":
                paused = not paused
                if paused:
                    play_sfx("click")
            elif gs.scene in ("howto",):
                gs.scene = "menu"
            elif gs.scene in ("result", "gameover"):
                do_home()

        # ── MENU ──
        if not paused and gs.scene == "menu":
            for b in btn_menu:
                if b.on_click(ev):
                    play_sfx("click")
                    if b.label == "PLAY":
                        gs.reset_match()
                        gs.scene = "game"
                        play_music("battle")
                    elif b.label == "HOW TO PLAY":
                        gs.scene = "howto"
                    elif b.label == "EXIT":
                        pygame.quit(); sys.exit()

        # ── HOWTO ──
        elif not paused and gs.scene == "howto":
            if btn_back.on_click(ev):
                play_sfx("click"); gs.scene = "menu"

        # ── GAME ──
        elif gs.scene == "game" and not paused:
            # Pause button
            if btn_pause.on_click(ev):
                paused = True; play_sfx("click")

            if not gs.answered:
                if ev.type == pygame.KEYDOWN:
                    for idx, key in enumerate(P1_KEYS):
                        if ev.key == key:
                            gs.register_answer("p1", idx); break
                    for idx, key in enumerate(P2_KEYS):
                        if ev.key == key:
                            gs.register_answer("p2", idx); break
            else:
                if gs.proj is None:
                    if btn_next.on_click(ev):
                        gs.next_question()
                    if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                        gs.next_question()

        # ── PAUSE OVERLAY ──
        elif gs.scene == "game" and paused:
            if btn_resume.on_click(ev):
                paused = False; play_sfx("click")
            if btn_restart_p.on_click(ev):
                play_sfx("click"); do_restart()
            if btn_quit_pause.on_click(ev):
                play_sfx("click"); do_home()

        # ── RESULT ──
        elif not paused and gs.scene == "result":
            if btn_restart_result.on_click(ev):
                play_sfx("click"); do_restart()
            if btn_home.on_click(ev):
                play_sfx("click"); do_home()
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                do_home()

        # ── GAME OVER ──
        elif not paused and gs.scene == "gameover":
            if btn_restart_go.on_click(ev):
                play_sfx("click"); do_restart()
            if btn_home_go.on_click(ev):
                play_sfx("click"); do_home()
            if ev.type == pygame.KEYDOWN and ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                do_home()

    # ── HOVER UPDATE ────────────────────────────────────────────────────
    if gs.scene == "menu":
        for b in btn_menu: b.update(mx, my)
    elif gs.scene == "howto":
        btn_back.update(mx, my)
    elif gs.scene == "game":
        btn_pause.update(mx, my)
        if paused:
            btn_resume.update(mx, my)
            btn_restart_p.update(mx, my)
            btn_quit_pause.update(mx, my)
        elif gs.answered and gs.proj is None:
            btn_next.update(mx, my)
    elif gs.scene == "result":
        btn_restart_result.update(mx, my)
        btn_home.update(mx, my)
    elif gs.scene == "gameover":
        btn_restart_go.update(mx, my)
        btn_home_go.update(mx, my)

    # ── RENDER ──────────────────────────────────────────────────────────
    from scenes import (render_menu, render_howto, render_game,
                        render_result, render_pause, render_gameover)

    if gs.scene == "menu":
        render_menu(screen, gs, btn_menu)
    elif gs.scene == "howto":
        render_howto(screen, gs, btn_back)
    elif gs.scene == "game":
        render_game(screen, gs, btn_next, btn_pause)
        if paused:
            render_pause(screen, gs, btn_resume, btn_restart_p, btn_quit_pause)
    elif gs.scene == "result":
        render_result(screen, gs, btn_home, btn_restart_result)
    elif gs.scene == "gameover":
        render_gameover(screen, gs, btn_restart_go, btn_home_go)

    pygame.display.flip()
