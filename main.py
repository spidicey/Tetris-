import random
import sys
import time

import pygame
import pygame.color

# Pygame setup
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
KEY_DELAY = 150
KEY_INTERVAL = 50
KEY_DELAY_SPACE = 700
KEY_INTERVAL_SPACE = 600
pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
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
X_SCORE, Y_SCORE, SCORE_WIDTH, SCORE_HEIGHT = 630, 30, 150, 150
X_LV, Y_LV, LV_WIDTH, LV_HEIGHT = 630, 190, 100, 30
X_NEXT, Y_NEXT, NEXT_WIDTH, NEXT_HEIGHT = 630, 250, 200, 200
X_STA, Y_STA, STA_WIDTH, STA_HEIGHT = 10, 100, 250, 560
PIXEL = PS_WIDTH // BOARD_WIDTH  #

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
YELLOW = (255, 255, 0)
LIGHTYELLOW = (175, 175, 20)
ORANGE = (255, 165, 0)
PURPLE = (191, 64, 191)

# Tetromino

S = [['.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '...O.',
      '.....']]

Z = [['.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']]

I = [['.....',
      '.OOOO.',
      '.....',
      '.....'],
     ['..O..',
      '..O..',
      '..O..',
      '..O..', ]]

O = [['.OO.',
      '.OO.', ]]

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

T = [['..O..',
      '.OOO.',
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
# Next piece
NEXT_PIECE_IMG = pygame.transform.scale(pygame.image.load(f'images/next_piece.png'), (NEXT_WIDTH, NEXT_HEIGHT))
# Play screen
PLAY_SCEEN_IMG = pygame.transform.scale(pygame.image.load(f'images/play_screen.png'), (30, PS_HEIGHT + 4))
# Score
SCORE_IMG = pygame.transform.scale(pygame.image.load(f'images/score.png'), (SCORE_WIDTH, SCORE_HEIGHT))
# Line
LINE_IMG = pygame.transform.scale(pygame.image.load('images/line.png'), (LINE_WIDTH, LINE_HEIGHT))
# Statistics
STATISTICS_IMG = pygame.transform.scale(pygame.image.load('images/play_screen_1.png'), (STA_WIDTH, STA_HEIGHT))
# Data tile
SPRITES = []
for i in range(9):
    SPRITES.append(pygame.transform.scale(pygame.image.load(f'images/T_{i}.png'), (PIXEL, PIXEL)))

TETROMINOS = [S, Z, J, L, I, O, T]
tetrominos_colors = [PURPLE, ORANGE, BLUE, RED, LIGHTRED, YELLOW, GREEN]
LOOKUP_TILE = {
    WHITE: SPRITES[8],
    BLACK: SPRITES[0],
    PURPLE: SPRITES[7],
    ORANGE: SPRITES[5],
    BLUE: SPRITES[4],
    RED: SPRITES[1],
    LIGHTRED: SPRITES[2],
    YELLOW: SPRITES[3],
    GREEN: SPRITES[6]
}
# Score cal
SCORE_CLEAR_LINE_LOOKUP = {  # ALL LEVEL 0       FORMULA = SCORE_LOOKUP[LINE_CLEAR] * (LEVEL+1)
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 400
}
# Statictis
STATISTICS = {
    TETROMINOS.index(S): 0,
    TETROMINOS.index(Z): 0,
    TETROMINOS.index(J): 0,
    TETROMINOS.index(L): 0,
    TETROMINOS.index(I): 0,
    TETROMINOS.index(O): 0,
    TETROMINOS.index(T): 0
}
# Font
FONT_PATH = 'font/ARCADECLASSIC.TTF'
# Sound effect
TETRIS_SFX = pygame.mixer.Sound('soundtrack/1-01 - Tetris!.mp3')
CLEAR_SFX = pygame.mixer.Sound('soundtrack/clear.wav')
ROTATION_SFX = pygame.mixer.Sound('soundtrack/rotation sfx.wav')
GAME_OVER_SFX = pygame.mixer.Sound('soundtrack/1-18 - Game Over.mp3')
SAMPLE_SFX = pygame.mixer.Sound('soundtrack/sfx_point.wav')
SAMPLE_SFX.set_volume(1.0)
ROTATION_SFX.set_volume(1.0)


class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = tetrominos_colors[TETROMINOS.index(shape)]
        self.rotation = 0  # number from 0-3
        self.pixel = SPRITES[TETROMINOS.index(shape)]


TEMPLATEWIDTH = TEMPLATEHEIGHT = 5


def UI(line, level, score):
    screen.blit(PLAY_SCEEN_IMG, (X_PS - 30, Y_PS - 4))
    screen.blit(PLAY_SCEEN_IMG, (X_PS + PS_WIDTH, Y_PS - 4))
    ui_lines(line)
    ui_score(score)
    ui_level(level)


def ui_lines(Lines=0):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT), width=3)
    # screen.blit(LINE_IMG, (X_LINE, Y_LINE))
    textsurface = pygame.font.SysFont(FONT_PATH, 30, bold=True).render(f'Lines {Lines:03d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LINE + X_LINE + LINE_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LINE + Y_LINE + LINE_HEIGHT) // 2 - textsurface.get_height() // 2))


def ui_level(level=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LV, Y_LV, LV_WIDTH, LV_HEIGHT), width=3)
    textsurface = pygame.font.SysFont(FONT_PATH, 30, bold=True).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LV + X_LV + LV_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LV + Y_LV + LV_HEIGHT) // 2 - textsurface.get_height() // 2))


def ui_score(score=0):
    # pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_SCORE, Y_SCORE, SCORE_WIDTH, SCORE_HEIGHT),
    #                  width=3)
    screen.blit(SCORE_IMG, (X_SCORE, Y_SCORE))
    textsurface = pygame.font.SysFont(FONT_PATH, 25, bold=True).render(f'Score: {score:06d}', False, (255, 255, 255))
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
    return Piece(5, 2, random.choice(TETROMINOS))


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
            if pos[1] > -1 or pos[0] < -1 or pos[0] >= 10:
                return False
    return True


def draw_grid(surface, col, row):
    for i in range(1, col):
        pygame.draw.line(surface, YELLOW, (X_PS + i * PIXEL, Y_PS), (X_PS + i * PIXEL, Y_PS + PS_HEIGHT - 4), width=0)
        for j in range(1, row):
            pygame.draw.line(surface, YELLOW, (X_PS, Y_PS + j * PIXEL), (X_PS + PS_WIDTH - 4, Y_PS + j * PIXEL),
                             width=0)


def draw_shape(piece, x, y):
    format = piece.shape[0]
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            color = piece.color
            tile = LOOKUP_TILE[color]
            if col == 'O':
                # screen.blit(tile, (
                #     ((X_STA + X_STA + STA_WIDTH) // 2 - 70) + j * PIXEL, Y_STA + 45 + i * PIXEL))
                screen.blit(tile, (x + j * PIXEL, y + i * PIXEL))


def draw_next_shape(surface, next_piece):
    surface.blit(NEXT_PIECE_IMG, (X_NEXT, Y_NEXT))
    format = next_piece.shape[0]
    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            color = next_piece.color
            tile = LOOKUP_TILE[color]
            if col == 'O':
                # pygame.draw.rect(surface, next_.color, (
                #     ((X_NEXT + X_NEXT + NEXT_WIDTH) // 2 - 60) + j * PIXEL, Y_NEXT + 40 + i * PIXEL, PIXEL, PIXEL))
                screen.blit(tile, (
                    ((X_NEXT + X_NEXT + NEXT_WIDTH) // 2 - 70) + j * PIXEL, Y_NEXT + 45 + i * PIXEL))


def draw_text(font, size, text):
    pass


def draw_statistic(STATISTIC):
    pygame.draw.rect(screen, YELLOW, pygame.Rect(X_STA, Y_STA, STA_WIDTH, STA_HEIGHT))
    # screen.blit(STATISTICS_IMG, (X_STA, Y_STA))
    for ind, tetromino in enumerate(TETROMINOS):
        draw_shape(Piece(0, 0, tetromino), (X_STA + X_STA + STA_WIDTH) // 3 - 70, Y_STA + ind * 80)
        textsurface = pygame.font.SysFont(FONT_PATH, 45, bold=True).render(f'{STATISTIC[ind]:03d}', False, BLACK)
        screen.blit(textsurface, ((X_STA + X_STA + STA_WIDTH) * 2 / 3, Y_STA + 36 + ind * 80))

    # draw_shape(Piece(0, 0, T),(X_STA + X_STA + STA_WIDTH) // 3 -70,Y_STA)
    # draw_shape(Piece(0, 0, O),(X_STA + X_STA + STA_WIDTH) // 3 -70,Y_STA+75)
    # draw_shape(Piece(0, 0, I),(X_STA + X_STA + STA_WIDTH) // 3 -70,Y_STA+160)


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one
    index = []
    inc = 0
    flag_ef = False
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            flag_ef = True
            inc += 1
            # add positions to remove from locked
            ind = i
            index.append(ind)
            print(index)
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    for ind in index:
        tile = LOOKUP_TILE[WHITE]
        for i in range(10):
            screen.blit(tile, (X_PS + i * PIXEL, Y_PS + ind * PIXEL))
        pygame.display.update()

    if flag_ef:
        for _ in range(2):
            draw_game(grid, level, next_piece, score, screen, total_line)
            for ind in index:
                tile = LOOKUP_TILE[WHITE]
                for i in range(10):
                    screen.blit(tile, (X_PS + i * PIXEL, Y_PS + ind * PIXEL))
                pygame.display.update()
                draw_game(grid, level, next_piece, score, screen, total_line)
            pygame.time.wait(100)
            draw_game(grid, level, next_piece, score, screen, total_line)
            pygame.display.update()

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    if inc == 4:
        pygame.mixer.Sound.play(TETRIS_SFX)
    elif inc > 0:
        pygame.mixer.Sound.play(CLEAR_SFX)
    return inc


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def draw_play_screen(screen, grid):
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
                pygame.draw.rect(screen, YELLOW, (X_PS + j * PIXEL, Y_PS + i * PIXEL, PIXEL, PIXEL), 0)
            else:
                screen.blit(tile, (X_PS + j * PIXEL, Y_PS + i * PIXEL))


def game_over():
    textsurface = pygame.font.SysFont(FONT_PATH, 45, bold=True).render(f'GAME OVER', False, BLACK)
    screen.blit(textsurface, ((X_PS + X_PS + PS_WIDTH) // 2 - textsurface.get_width() // 2,
                              (Y_PS + Y_PS + PS_HEIGHT) // 2 - textsurface.get_height() // 2))
    pygame.mixer.music.stop()
    GAME_OVER_SFX.play()
    pygame.display.flip()
    pygame.time.delay(2000)


def run_game():
    global screen, run_game, current_piece, level, next_piece, score, total_line
    screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
    screen.fill(BLACK)
    title = pygame.display.set_caption("Tetris")
    icon = pygame.image.load("images/Tetris.png")
    pygame.display.set_icon(icon)
    bg = pygame.transform.scale(pygame.image.load("images/olga-buiilova-9.jpg"), (S_WIDTH, S_HEIGHT))
    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False
    current_piece = get_piece()
    next_piece = get_piece()
    STATISTICS[TETROMINOS.index(current_piece.shape)] += 1
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27  # formula fallspeed = 1 - level * 0.1
    total_line = 0
    score = 0
    level = 1
    music = pygame.mixer.music.load("soundtrack/Tetris.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(bg, (0, 0))
        grid = create_grid(locked_pos)
        fall_time += clock.get_rawtime()
        clock.tick()
        last_move_sideways_time = time.time()
        lastFallTime = time.time()
        moves_speed = 0.27
        line_clear = 0
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (is_valid(grid, current_piece)) and current_piece.y > 0:
                score += 10
                current_piece.y -= 1
                change_piece = True
        key_input = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
                    current_piece.x -= 1
                    if not is_valid(grid, current_piece):
                        current_piece.x += 1
                    else:
                        pygame.mixer.Sound.play(ROTATION_SFX)
                elif event.key == pygame.K_RIGHT:
                    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
                    current_piece.x += 1
                    if not is_valid(grid, current_piece):
                        current_piece.x -= 1
                    else:
                        pygame.mixer.Sound.play(ROTATION_SFX)
                elif event.key == pygame.K_DOWN:
                    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
                    current_piece.y += 1
                    if not is_valid(grid, current_piece):
                        current_piece.y -= 1
                    else:
                        pygame.mixer.Sound.play(ROTATION_SFX)
                elif event.key == pygame.K_UP:
                    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
                    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    if not is_valid(grid, current_piece):
                        current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                    else:
                        pygame.mixer.Sound.play(ROTATION_SFX)
                elif event.key == pygame.K_z:
                    pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
                    current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
                    if not is_valid(grid, current_piece):
                        current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                    else:
                        pygame.mixer.Sound.play(ROTATION_SFX)
                elif event.key == pygame.K_SPACE:
                    pygame.key.set_repeat(KEY_DELAY_SPACE, KEY_INTERVAL_SPACE)
                    if is_valid(grid, current_piece) and current_piece.y > 0:
                        for i in range(20):
                            if not is_valid(grid, current_piece):
                                current_piece.y -= 1
                                break
                            else:
                                current_piece.y += 1
                        score += 10
                        pygame.mixer.Sound.play(SAMPLE_SFX)

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                try:
                    grid[y][x] = current_piece.color
                except:
                    continue
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_pos[p] = current_piece.color
            current_piece = next_piece
            STATISTICS[TETROMINOS.index(current_piece.shape)] += 1
            next_piece = get_piece()
            change_piece = False
            line_clear += clear_rows(grid, locked_pos)
            total_line += line_clear
        score += SCORE_CLEAR_LINE_LOOKUP[line_clear] * (level + 1)
        draw_game(grid, level, next_piece, score, screen, total_line)
        pygame.display.flip()
        if check_lost(locked_pos):
            run_game = False
    game_over()


def draw_game(grid, level, next_piece, score, screen, total_line):
    draw_next_shape(screen, next_piece)
    UI(total_line, level, score)
    draw_play_screen(screen, grid)
    draw_statistic(STATISTICS)


if __name__ == "__main__":
    run_game()
