"""
Perseus — Automaton Visualizer (pygame)

Interactive 16×16 Brian's Brain CA viewer.

Controls:
  SPACE         — pause / resume
  R             — reset with current density
  Up / Down     — increase / decrease speed
  Left / Right  — step backward / forward (in history)
  Click         — toggle cell state
  ESC           — quit
"""

from __future__ import annotations

import pygame
import numpy as np

from perseus.automaton.hippocampal import HippocampalAutomaton
from perseus.automaton.grid import Automaton


# ── Palette ───────────────────────────────────────────────────────────────────

BG          = (12, 12, 20)        # deep navy background
OFF_COLOR   = (30, 32, 50)        # dim resting neuron
ON_COLOR    = (72, 210, 255)      # electric cyan — firing
DYING_COLOR = (255, 90, 70)       # ember red — refractory
BORDER      = (0, 0, 0)

TEXT_COLOR  = (200, 205, 225)
DIM_COLOR   = (100, 105, 130)
BAR_COLOR   = (72, 210, 255)
BAR_BG      = (35, 37, 58)
POS_COLOR   = (100, 255, 140)     # positive momentum
NEG_COLOR   = (255, 100, 100)     # negative momentum


class AutomatonVisualizer:
    """
    Standalone pygame visualizer for a single Perseus Automaton.

    Usage:
        AutomatonVisualizer().run()
    """

    SIDEBAR_W = 300
    CELL_SIZE = 44       # 16 * 44 = 704px height

    def __init__(self, width: int = 16, height: int = 16, density: float = 0.20) -> None:
        self.ha = HippocampalAutomaton("default", width=width, height=height, density=density)
        self.automaton = self.ha.automaton
        self.cell_size = self.CELL_SIZE
        self.cols = width
        self.rows = height

        grid_px_w = width  * self.cell_size
        grid_px_h = height * self.cell_size

        self.win_w = grid_px_w + self.SIDEBAR_W
        self.win_h = grid_px_h

        pygame.init()
        self.screen = pygame.display.set_mode((self.win_w, self.win_h))
        pygame.display.set_caption("Perseus — Automaton")
        self.clock = pygame.time.Clock()

        self.font_md = pygame.font.SysFont("monospace", 16, bold=True)
        self.font_sm = pygame.font.SysFont("monospace", 14)

        self.running  = True
        self.paused   = True
        self.fps      = 10
        self.state: AutomatonState | None = None

        self.history: list[tuple[np.ndarray, AutomatonState]] = []
        self.history_index = -1
        self._record_current_state()

    def _record_current_state(self):
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        self.history.append((self.automaton.grid.copy(), self.ha.get_state()))
        self.history_index += 1
        self.state = self.history[self.history_index][1]

    def _restore_history(self):
        grid, state = self.history[self.history_index]
        self.automaton.grid[:] = grid
        self.state = state

    def run(self) -> None:
        while self.running:
            self._handle_events()
            if not self.paused:
                self.state = self.ha.step()
                self._record_current_state()
            self._render()
            self.clock.tick(self.fps)
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.ha = HippocampalAutomaton("default", width=self.cols, height=self.rows)
                    self.automaton = self.ha.automaton
                    self.history = []
                    self.history_index = -1
                    self._record_current_state()
                elif event.key == pygame.K_UP:
                    self.fps = min(60, self.fps + 1)
                elif event.key == pygame.K_DOWN:
                    self.fps = max(1, self.fps - 1)
                elif event.key == pygame.K_RIGHT:
                    if self.history_index < len(self.history) - 1:
                        self.history_index += 1
                        self._restore_history()
                    else:
                        self.state = self.ha.step()
                        self._record_current_state()
                elif event.key == pygame.K_LEFT:
                    if self.history_index > 0:
                        self.history_index -= 1
                        self._restore_history()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                gx, gy = x // self.cell_size, y // self.cell_size
                if x < self.cols * self.cell_size and 0 <= gx < self.cols and 0 <= gy < self.rows:
                    self.automaton.toggle_cell(gx, gy)
                    self._record_current_state()

    def _render(self) -> None:
        self.screen.fill(BG)
        self._draw_grid()
        self._draw_sidebar()
        pygame.display.flip()

    def _draw_grid(self) -> None:
        cs = self.cell_size
        for row in range(self.rows):
            for col in range(self.cols):
                state = self.automaton.grid[row, col]
                color = (ON_COLOR if state == Automaton.ON else DYING_COLOR if state == Automaton.DYING else OFF_COLOR)
                rect = pygame.Rect(col * cs, row * cs, cs, cs)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BORDER, rect, 1)

    def _draw_sidebar(self) -> None:
        if self.state is None: return
        sx, y = self.cols * self.cell_size + 20, 25

        def label(text: str, color=TEXT_COLOR, space=6):
            nonlocal y
            surf = self.font_md.render(text, True, color)
            self.screen.blit(surf, (sx, y))
            y += surf.get_height() + space

        def small(text: str, color=DIM_COLOR, space=4):
            nonlocal y
            surf = self.font_sm.render(text, True, color)
            self.screen.blit(surf, (sx, y))
            y += surf.get_height() + space

        def bar(name: str, value: float, color=BAR_COLOR):
            nonlocal y
            small(name, TEXT_COLOR, space=2)
            bw = self.SIDEBAR_W - 40
            pygame.draw.rect(self.screen, BAR_BG, (sx, y, bw, 12), border_radius=4)
            if value > 0:
                pygame.draw.rect(self.screen, color, (sx, y, int(bw * min(1, value)), 12), border_radius=4)
            val_txt = self.font_sm.render(f"{value:.3f}", True, DIM_COLOR)
            self.screen.blit(val_txt, (sx + bw - val_txt.get_width(), y - 2))
            y += 22

        label("PERSEUS", TEXT_COLOR)
        small("Automaton 16×16", DIM_COLOR, space=15)

        status_col = (255, 100, 80) if self.paused else (100, 255, 140)
        label("PAUSED" if self.paused else "RUNNING", status_col)
        small(f"Gen  {self.state.generation:>6}")
        small(f"FPS  {self.fps:>6}")
        small(f"Hist {self.history_index + 1}/{len(self.history)}", space=20)

        label("─ Metrics ─", DIM_COLOR, space=10)
        bar("Activation", self.state.activation)
        bar("Refractory", self.state.refractory)
        bar("Occupancy",  self.ha.occupancy)
        bar("Entropy",    self.ha.entropy)
        bar("Cost",       self.state.cost, color=(200, 180, 255))
        
        y += 10
        mom = self.state.momentum
        label(f"Momentum {mom:+.4f}", POS_COLOR if mom >= 0 else NEG_COLOR, space=20)

        label("─ Legend ─", DIM_COLOR, space=10)
        for c, t in [(ON_COLOR, "■ ON (firing)"), (DYING_COLOR, "■ DYING (refractory)"), (OFF_COLOR, "■ OFF (resting)")]:
            small(t, c, space=6)

        y += 15
        label("─ Controls ─", DIM_COLOR, space=10)
        for h in ["SPACE pause", "R     reset", "↑/↓   speed", "←/→   history", "Click toggle", "ESC   quit"]:
            small(h, DIM_COLOR, space=4)


def main() -> None:
    AutomatonVisualizer().run()


if __name__ == "__main__":
    main()
