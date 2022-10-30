import random
import time
import pygame, sys
import pygame.color
from dataclasses import dataclass

pygame.init()
# Global variable

SCORE = 0
LEVEL = 1
S_WIDTH = 900
S_HEIGHT = 700
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLANK = '.'
X_PS, Y_PS, PS_WIDTH, PS_HEIGHT = 300, 100, 280, 560  # play screen width, height
X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT = 300, 30, 280, 50
X_SCORE, Y_SCORE, SCORE_WIDTH, SCORE_HEIGHT = 600, 30, 130, 130
X_LV, Y_LV, LV_WIDTH, LV_HEIGHT = 600, 190, 100, 30
X_NEXT, Y_NEXT, NEXT_WIDTH, NEXT_HEIGHT = 600, 250, 200, 200
PIXEL = PS_WIDTH // BOARD_WIDTH

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
ORANGE = (255, 165, 0)
PURPLE = (191, 64, 191)

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

# Data tile
TILE = []
for i in range(7):
    TILE.append(pygame.transform.scale(pygame.image.load(f'images/T_{i}.png'), (PIXEL, PIXEL)))

TETROMINOS = [S, Z, J, L, I, O, T]
tetrominos_colors = [PURPLE, ORANGE, BLUE, RED, LIGHTRED, YELLOW, GREEN]
LOOKUP_TILE = {
    BLACK: BLACK,
    PURPLE: TILE[6],
    ORANGE: TILE[5],
    BLUE: TILE[4],
    RED: TILE[1],
    LIGHTRED: TILE[2],
    YELLOW: TILE[3],
    GREEN: TILE[6]
}


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = tetrominos_colors[TETROMINOS.index(shape)]
        self.rotation = 0  # number from 0-3
        self.pixel = TILE[TETROMINOS.index(shape)]


TEMPLATEWIDTH = TEMPLATEHEIGHT = 5


def UI(line, level, socre):
    pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(X_PS, Y_PS, PS_WIDTH, PS_HEIGHT), width=3)
    ui_lines(line)
    ui_score(score)
    ui_level(level)


def ui_lines(Lines=0):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Lines {Lines:03d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LINE + X_LINE + LINE_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LINE + Y_LINE + LINE_HEIGHT) // 2 - textsurface.get_height() // 2))


def ui_level(level=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LV, Y_LV, LV_WIDTH, LV_HEIGHT), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LV + X_LV + LV_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LV + Y_LV + LV_HEIGHT) // 2 - textsurface.get_height() // 2))


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


def draw_next_shape(surface, grid, next_piece):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_NEXT, Y_NEXT, NEXT_WIDTH, NEXT_HEIGHT),
                     width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Next Piece', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_NEXT + X_NEXT + NEXT_WIDTH) // 2 - textsurface.get_width() // 2, Y_NEXT + 20))
    format = next_piece.shape[0]
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            color = next_piece.color
            tile = LOOKUP_TILE[color]
            if col == 'O':
                # pygame.draw.rect(surface, next_piece.color, (
                #     ((X_NEXT + X_NEXT + NEXT_WIDTH) // 2 - 60) + j * PIXEL, Y_NEXT + 40 + i * PIXEL, PIXEL, PIXEL))
                screen.blit(tile,(
                    ((X_NEXT + X_NEXT + NEXT_WIDTH) // 2 - 60) + j * PIXEL, Y_NEXT + 40 + i * PIXEL))


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


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_game(screen, grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(screen, grid[i][j], (X_PS + j * PIXEL, Y_PS + i * PIXEL, PIXEL, PIXEL), 0)
            # if grid[i][j]!=(0,0,0):
            #     screen.blit(current_piece.pixel,(x_ps+j*pixel,y_ps+i*pixel))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            color = grid[i][j]
            tile = LOOKUP_TILE[color]
            if grid[i][j] == (0, 0, 0):
                screen.blit(TILE[0], (X_PS + j * PIXEL, Y_PS + i * PIXEL))
            else:
                screen.blit(tile, (X_PS + j * PIXEL, Y_PS + i * PIXEL))


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
    line = 0
    score = 0
    level = 1
    while 1:
        screen.fill(BLACK)
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()
        moving_left = False
        moving_right = False
        moving_down = False
        last_move_sideways_time = time.time()
        lastFallTime = time.time()
        moves_speed = 0.27
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (is_valid(grid, current_piece)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        key_input = pygame.key.get_pressed()
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
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not is_valid(grid, current_piece):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                elif event.key == pygame.K_z:
                    current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                    if not is_valid(grid, current_piece):
                        current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    for i in range(20):
                        if not is_valid(grid, current_piece):
                            current_piece.y -= 1
                            break
                        else:
                            current_piece.y += 1

        shape_pos = convert_shape_format(current_piece)
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
            line += clear_rows(grid, locked_pos)
        draw_game(screen, grid)
        # screen.blit(bg,(0,0))
        draw_next_shape(screen, grid, next_piece)
        draw_grid(screen, 10, 20)
        UI(line, level, score)
        pygame.display.flip()
