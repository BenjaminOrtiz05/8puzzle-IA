# main.py
import pygame
import sys
import time
from puzzle import Puzzle, GOAL_STATE
from solver import bfs, astar

# Configuración
WIDTH, HEIGHT = 300, 450
TILE_SIZE = 90
MARGIN = 5

WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
BLUE = (40, 120, 200)
DARK_GRAY = (100, 100, 100)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Puzzle Solver")
font = pygame.font.SysFont("Arial", 36)
small_font = pygame.font.SysFont("Arial", 20)

# Botones
class Button:
    def __init__(self, label, x, y, w, h):
        self.label = label
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, border_radius=6)
        text = small_font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

buttons = {
    "a_star": Button("Resolver A*", 30, 290, 110, 40),
    "bfs": Button("Resolver BFS", 160, 290, 110, 40),
    "reset": Button("Reset", 95, 350, 110, 40)
}

puzzle = Puzzle()

def draw_board(board):
    screen.fill(WHITE)
    for i in range(3):
        for j in range(3):
            value = board[i][j]
            x = j * TILE_SIZE + MARGIN * (j + 1)
            y = i * TILE_SIZE + MARGIN * (i + 1)
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            if value != 0:
                pygame.draw.rect(screen, DARK_GRAY, rect, border_radius=6)
                text = font.render(str(value), True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)

def animate_solution(solution_path):
    for state in solution_path:
        puzzle.set_board(state)
        draw_board(puzzle.get_board())
        for btn in buttons.values():
            btn.draw(screen)
        pygame.display.flip()
        time.sleep(0.4)

def get_clicked_tile(pos):
    x, y = pos
    if y > 270:
        return None
    col = x // (TILE_SIZE + MARGIN)
    row = y // (TILE_SIZE + MARGIN)
    return row, col

running = True
while running:
    draw_board(puzzle.get_board())
    for btn in buttons.values():
        btn.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            if buttons["a_star"].is_clicked(pos):
                solution = astar(puzzle.board_to_tuple(), tuple(tuple(row) for row in GOAL_STATE))
                if solution:
                    animate_solution(solution)

            elif buttons["bfs"].is_clicked(pos):
                solution = bfs(puzzle.board_to_tuple(), tuple(tuple(row) for row in GOAL_STATE))
                if solution:
                    animate_solution(solution)

            elif buttons["reset"].is_clicked(pos):
                puzzle.shuffle_board()

            else:
                tile = get_clicked_tile(pos)
                if tile:
                    puzzle.move_tile(*tile)

pygame.quit()
sys.exit()
