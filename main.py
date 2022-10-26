import random

import pygame, sys
import pygame.color
from dataclasses import dataclass

pygame.init()

# Tetromino

S = [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....']]

Z = [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']]

I = [['..O..',
      '..O..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      'OOOO.',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.OO..',
      '.OO..',
      '.....']]

J = [['.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..OO.',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....']]

L = [['.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '..OO.',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....'],
     ['.....',
      '.OO..',
      '..O..',
      '..O..',
      '.....']]

T = [['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....']]

TETROMINOS = [S, Z, J, L, I, O, T]
tetrominos_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = tetrominos_colors[TETROMINOS.index(shape)]
        self.rotation = 0  # number from 0-3
        self.pixel = TIDE[TETROMINOS.index(shape)]


TEMPLATEWIDTH = TEMPLATEHEIGHT = 5
#               R    G    B
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
RED = (155, 0, 0)
LIGHTRED = (175, 20, 20)
GREEN = (0, 155, 0)
LIGHTGREEN = (20, 175, 20)
BLUE = (0, 0, 155)
LIGHTBLUE = (20, 20, 175)
YELLOW = (155, 155, 0)
LIGHTYELLOW = (175, 175, 20)

# Global variable

SCORE = 0
LEVEL = 1
S_WIDTH = 720
S_HEIGHT = 700
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = '.'
X_PS, Y_PS, PS_WIDTH, PS_HEIGHT = 200, 100, 280, 560  # play screen width, height
X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT = 200, 30, 280, 50
X_SCORE, Y_SCORE, SCORE_WIDTH, SCORE_HEIGHT = 500, 30, 130, 130
X_LV, Y_LV, LV_WIDTH, LV_HEIGHT = 500, 200, 100, 20
X_NEXT, Y_NEXT, NEXT_WIDTH, NEXT_HEIGHT= 500,250,200,200

# tetrominos = ['s': S, 'Z': Z, I, O, J, L, T]
PIXEL = PS_WIDTH // BOARD_WIDTH
TIDE = []
for i in range(8):
    TIDE.append(pygame.transform.scale(pygame.image.load(f'images/T_{i}.gif'), (PIXEL, PIXEL)))

piece_colors = {'S': 1,
                'Z': 2,
                'J': 3,
                'L': 4,
                'I': 5,
                'O': 6,
                'T': 7}



def UI():
    pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(X_PS, Y_PS, PS_WIDTH, PS_HEIGHT), width=3)
    ui_lines()
    ui_score()
    ui_level()


def ui_lines(Lines=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Lines {LEVEL:03d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LINE + X_LINE + LINE_WIDTH) // 2 - textsurface.get_width() // 2, Y_LINE + 3))


def ui_level(level=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LV, Y_LV, LV_WIDTH, LV_HEIGHT), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LV + X_LV + LV_WIDTH) // 2 - textsurface.get_width() // 2, Y_LV + 3))


def ui_score(score=0):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_SCORE, Y_SCORE, SCORE_WIDTH, SCORE_HEIGHT),
                     width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Score: {score:06d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_SCORE + X_SCORE + SCORE_WIDTH) // 2 - textsurface.get_width() // 2, Y_SCORE + 2 * SCORE_HEIGHT // 3))


def create_grid(locked_pos={}):
    # create and return a new blank board data structure
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(20):
        for j in range(10):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c
    return grid


def get_piece():
    return Piece(5, 0, random.choice(TETROMINOS))


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    print(format)
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == 'O':
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


def is_valid(grid, shape):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True


def draw_grid(surface, col, row):
    for i in range(1, col):
        pygame.draw.line(surface, WHITE, (X_PS + i * PIXEL, Y_PS), (X_PS + i * PIXEL, Y_PS + PS_HEIGHT - 4), width=1)
        for j in range(1, row):
            pygame.draw.line(surface, WHITE, (X_PS, Y_PS + j * PIXEL), (X_PS + PS_WIDTH - 4, Y_PS + j * PIXEL), width=1)


def draw_next_shape(grid):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_NEXT, Y_NEXT, NEXT_WIDTH, NEXT_HEIGHT),
                     width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Next Piece', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_NEXT+ NEXT_WIDTH) // 2 - textsurface.get_width() // 2, Y_NEXT))


def flash():
    for _ in range(5):
        screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.wait(10)
        screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.time.wait(2000)
    UI()
    pygame.time.wait(2000)


if __name__ == "__main__":
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    screen.fill(BLACK)
    title = pygame.display.set_caption("Tetris")
    icon = pygame.image.load("images/Tetris.png")
    pygame.display.set_icon(icon)
    bg = pygame.transform.scale(pygame.image.load("images/start.gif"), (S_HEIGHT, S_WIDTH))

    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False
    current_piece = get_piece()
    next_piece = get_piece()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    while 1:
        screen.fill(BLACK)
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (is_valid(grid, current_piece)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not is_valid(grid, current_piece):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not is_valid(grid, current_piece):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not is_valid(grid, current_piece):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not is_valid(grid, current_piece):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
        shape_pos = convert_shape_format(current_piece)
        print(shape_pos)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_piece()
            change_piece = False
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(screen, grid[i][j], (X_PS + j * PIXEL, Y_PS + i * PIXEL, PIXEL, PIXEL), 0)
                # if grid[i][j]!=(0,0,0):
                #     screen.blit(current_piece.pixel,(x_ps+j*pixel,y_ps+i*pixel))
        # screen.blit(bg,(0,0))
        draw_next_shape(grid)
        draw_grid(screen, 10, 20)
        UI()
        pygame.display.flip()
