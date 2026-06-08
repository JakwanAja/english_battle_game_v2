"""
game_state.py — GameStateManager untuk 2-player English Battle Pets
"""

import random
from constants import *
from questions import ALL_QUESTIONS_POOL
from objects import Particle, Projectile

def _sfx(name):
    """Safe SFX caller — lazy import to avoid circular imports."""
    try:
        from scenes import play_sfx
        play_sfx(name)
    except Exception:
        pass


class GameStateManager:
    def __init__(self):
        self.reset_match()

    def reset_match(self):
        self.scene      = "menu"
        self.anim_time  = 0.0

        # HP
        self.p1_hp = TOTAL_HP
        self.p2_hp = TOTAL_HP
        self._pending_gameover = False

        # Soal
        self.questions  = random.sample(ALL_QUESTIONS_POOL,
                                        min(QUESTIONS_PER_MATCH, len(ALL_QUESTIONS_POOL)))
        self.current_q  = 0

        # Round state
        self.answered   = False     # True setelah ada yang menjawab / timer habis
        self.winner     = None      # "p1" / "p2" / "none" (timer habis tanpa benar)
        self.p1_choice  = None      # index jawaban P1 (0–3 atau None)
        self.p2_choice  = None      # index jawaban P2

        # Timer
        self.round_timer = ROUND_TIMER

        # Animasi
        self.proj       = None
        self.particles  = []
        self.p1_state   = "idle"
        self.p2_state   = "idle"
        self.state_timer = 0.0

        # Score (soal benar)
        self.p1_score   = 0
        self.p2_score   = 0

    # ── ROUND LOGIC ──────────────────────────────────────────────────────
    def register_answer(self, player, choice_idx):
        """
        Dipanggil saat P1 atau P2 menekan tombol.
        Hanya berlaku jika ronde belum berakhir.
        """
        if self.answered:
            return

        # Simpan pilihan
        if player == "p1" and self.p1_choice is None:
            self.p1_choice = choice_idx
        elif player == "p2" and self.p2_choice is None:
            self.p2_choice = choice_idx

        correct_ans = self.questions[self.current_q]["ans"]

        # Cek apakah pemain yang baru menjawab benar
        if player == "p1" and self.p1_choice == correct_ans:
            self._resolve_round("p1")
        elif player == "p2" and self.p2_choice == correct_ans:
            self._resolve_round("p2")
        # Jika salah dua-duanya sudah menjawab dan keduanya salah
        elif self.p1_choice is not None and self.p2_choice is not None:
            self._resolve_round("none")

    def timer_expired(self):
        """Dipanggil dari main loop saat round_timer <= 0."""
        if not self.answered:
            self._resolve_round("none")

    def _resolve_round(self, winner):
        """
        winner = "p1" → P1 menyerang P2
        winner = "p2" → P2 menyerang P1
        winner = "none" → tidak ada yang menyerang
        """
        self.answered     = True
        self.winner       = winner
        self.round_timer  = 0.0

        if winner == "p1":
            self.p1_score  += 1
            self.p1_state   = "attack"
            self.p2_state   = "idle"
            self.proj       = Projectile(220, 380, 740, 340, GOLD)
            self.state_timer = 0.6
            _sfx("correct")
        elif winner == "p2":
            self.p2_score  += 1
            self.p2_state   = "attack"
            self.p1_state   = "idle"
            self.proj       = Projectile(740, 340, 220, 380, (150, 60, 220))
            self.state_timer = 0.6
            _sfx("correct")
        else:
            # Tidak ada yang menyerang
            _sfx("wrong")
            self.state_timer = 0.3

    def update(self, dt):
        """Dipanggil tiap frame dari main loop."""
        self.anim_time   += dt
        self.state_timer  = max(0.0, self.state_timer - dt)

        if self.scene != "game":
            return

        # Hitung mundur timer soal
        if not self.answered:
            prev_timer = self.round_timer
            self.round_timer -= dt
            if self.round_timer <= 0:
                self.timer_expired()
            # Tick SFX setiap detik saat timer kritis (< 5s)
            elif self.round_timer < 5.0 and int(prev_timer) > int(self.round_timer):
                _sfx("tick")

        # Update proyektil
        if self.proj:
            self.proj.update(dt)
            if self.proj.hit:
                # Ledakan partikel
                col = GOLD if self.winner == "p1" else (150, 60, 220)
                for _ in range(20):
                    self.particles.append(Particle(self.proj.tx, self.proj.ty, col))

                # Kurangi HP
                _sfx("hit")
                if self.winner == "p1":
                    self.p2_hp      -= 1
                    self.p2_state    = "hit"
                elif self.winner == "p2":
                    self.p1_hp      -= 1
                    self.p1_state    = "hit"

                self.proj         = None
                self.state_timer  = 0.5

                # Langsung ke result jika HP habis
                if self.p1_hp <= 0 or self.p2_hp <= 0:
                    self.state_timer = 1.2   # jeda dramatis sebelum layar gameover
                    self._pending_gameover = True

        # Reset state ke idle setelah timer habis
        if self.state_timer <= 0:
            if getattr(self, '_pending_gameover', False):
                self._pending_gameover = False
                self.scene = "gameover"
            self.p1_state = "idle"
            self.p2_state = "idle"

        # Update partikel
        self.particles = [p for p in self.particles if p.update(dt)]

    def next_question(self):
        """Maju ke soal berikutnya atau pindah ke result."""
        if self.p1_hp <= 0 or self.p2_hp <= 0:
            self.scene = "result"
            return

        self.current_q   = (self.current_q + 1) % len(self.questions)
        self.answered    = False
        self.winner      = None
        self.p1_choice   = None
        self.p2_choice   = None
        self.round_timer = ROUND_TIMER
        self.proj        = None
        self.p1_state    = "idle"
        self.p2_state    = "idle"
        self.state_timer = 0.0

    def get_overall_winner(self):
        """Kembalikan 'p1', 'p2', atau 'draw'."""
        if self.p1_hp <= 0 and self.p2_hp <= 0:
            return "draw"
        if self.p1_hp <= 0:
            return "p2"
        if self.p2_hp <= 0:
            return "p1"
        # Habis soal (tidak ada HP 0) → bandingkan score
        if self.p1_score > self.p2_score:
            return "p1"
        if self.p2_score > self.p1_score:
            return "p2"
        return "draw"
