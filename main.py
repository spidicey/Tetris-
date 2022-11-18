import random
import sys
import time
import pygame
from header.Piece import Piece
from header.color import WHITE, BLACK, YELLOW
from header.coordinate import *
from header.data_game import TETROMINOS, LOOKUP_TILE, LEVEL_SPRITE
# from header.coordinate import S_WIDTH, S_HEIGHT, PIXEL
from header.delay import KEY_DELAY, KEY_INTERVAL
from header.loaded_image import START_SCREEB_IMG, NEXT_PIECE_IMG, PLAY_SCEEN_IMG, SCORE_IMG, LEVEL_IMG
from header.scoring import SCORE_CLEAR_LINE_LOOKUP
# from header.a import TETRIS_SFX, CLEAR_SFX, ROTATION_SFX, GAME_OVER_SFX, SAMPLE_SFX
from header.tetrominos import S, Z, I, O, J, L, T

# Pygame setup
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.key.set_repeat(KEY_DELAY, KEY_INTERVAL)
# Global variable
SCORE = 0
LEVEL = 0

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
TETRIS_SFX = pygame.mixer.Sound('soundtrack/Tetris!.mp3')
CLEAR_SFX = pygame.mixer.Sound('soundtrack/clear.wav')
ROTATION_SFX = pygame.mixer.Sound('soundtrack/rotation sfx.wav')
GAME_OVER_SFX = pygame.mixer.Sound('soundtrack/Game Over.mp3')
SAMPLE_SFX = pygame.mixer.Sound('soundtrack/sfx_point.wav')
SAMPLE_SFX.set_volume(1.0)
ROTATION_SFX.set_volume(1.0)

TEMPLATEWIDTH = TEMPLATEHEIGHT = 5


def UI(line, level, score):
    screen.blit(PLAY_SCEEN_IMG, (X_PS - 30, Y_PS - 4))
    screen.blit(PLAY_SCEEN_IMG, (X_PS + PS_WIDTH, Y_PS - 4))
    draw_lines(line)
    draw_score(score)
    draw_level(level)


def draw_lines(Lines=0):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LINE, Y_LINE, LINE_WIDTH, LINE_HEIGHT), width=3)
    # screen.blit(LINE_IMG, (X_LINE, Y_LINE))
    textsurface = pygame.font.SysFont(FONT_PATH, 30, bold=True).render(f'Lines {Lines:03d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LINE + X_LINE + LINE_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LINE + Y_LINE + LINE_HEIGHT) // 2 - textsurface.get_height() // 2))


def draw_level(level=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(X_LV, Y_LV, LV_WIDTH, LV_HEIGHT), width=3)
    textsurface = pygame.font.SysFont(FONT_PATH, 30, bold=True).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (X_LV + X_LV + LV_WIDTH) // 2 - textsurface.get_width() // 2,
        (Y_LV + Y_LV + LV_HEIGHT) // 2 - textsurface.get_height() // 2))


def draw_score(score=0):
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
        draw_shape(Piece(0, 0, tetromino), (X_STA + X_STA + STA_WIDTH) // 3 - 70, Y_STA - 15 + ind * 80)
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
        clear_row_sfx(inc)
        clear_row_effect(grid, ind, index)
        # last_k=time.time()+1
        # else:
        #     clear_row_sfx(inc)

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def clear_row_effect(grid, ind, index):
    draw_game(grid, LEVEL, next_piece, score, screen, total_line)
    # global LEVEL
    for _ in range(3):
        draw_game(grid, LEVEL, next_piece, score, screen, total_line)
        for ind in index:
            tile = LOOKUP_TILE[WHITE]
            for i in range(10):
                screen.blit(tile, (X_PS + i * PIXEL, Y_PS + ind * PIXEL))
            pygame.display.update()
            # draw_game(grid, level, next_piece, score, screen, total_line)
        pygame.time.delay(150)
        draw_game(grid, LEVEL, next_piece, score, screen, total_line)
        pygame.display.update()
        pygame.time.delay(150)
        pygame.display.update()


def clear_row_sfx(inc):
    if inc == 4:
        pygame.mixer.Sound.play(TETRIS_SFX)
    elif inc > 0:
        pygame.mixer.Sound.play(CLEAR_SFX)


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
    textsurface = pygame.font.SysFont(FONT_PATH, 45, bold=True).render(f'GAME OVER', False, WHITE)
    screen.blit(textsurface, ((X_PS + X_PS + PS_WIDTH) // 2 - textsurface.get_width() // 2,
                              (Y_PS + Y_PS + PS_HEIGHT) // 2 - textsurface.get_height() // 2))
    pygame.mixer.music.stop()
    GAME_OVER_SFX.play()
    pygame.display.flip()
    pygame.time.delay(5000)


def pause_game():
    draw_game(grid, level, next_piece, score, screen, total_line)
    textsurface = pygame.font.SysFont(FONT_PATH, 45, bold=True).render(f'PAUSE', False, WHITE)
    screen.blit(textsurface, ((X_PS + X_PS + PS_WIDTH) // 2 - textsurface.get_width() // 2,
                              (Y_PS + Y_PS + PS_HEIGHT) // 2 - textsurface.get_height() // 2))
    pygame.display.flip()


def run_game(level):
    global screen, current_piece, next_piece, score, total_line, grid, last_k
    space_freq = 0.8
    last_k = time.time()
    screen.fill(BLACK)
    BACKGROUND_IMG = pygame.transform.scale(pygame.image.load("images/olga-buiilova-9.jpg"), (S_WIDTH, S_HEIGHT))
    locked_pos = {}
    grid = create_grid(locked_pos)
    change_piece = False
    current_piece = get_piece()
    next_piece = get_piece()
    STATISTICS[TETROMINOS.index(current_piece.shape)] += 1
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 1 - LEVEL * 0.1  # formula fallspeed = 1 - level * 0.1
    total_line = 0
    score = 0
    music = pygame.mixer.music.load("soundtrack/Tetris.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    run_game = True
    while run_game:
        screen.fill(BLACK)
        screen.blit(BACKGROUND_IMG, (0, 0))
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
                    if (time.time() - last_k > space_freq):
                        # pygame.key.set_repeat(KEY_DELAY_SPACE, KEY_INTERVAL_SPACE)
                        last_k = time.time()
                        if is_valid(grid, current_piece) and current_piece.y > 2:
                            for i in range(20):
                                if not is_valid(grid,
                                                current_piece) or current_piece.y > 21:  # there are 20 row each tetromino at form 0 take 2 space at the bottom of the board so the y cor have to < 22
                                    current_piece.y -= 1
                                    break
                                else:
                                    current_piece.y += 1
                            score += 10
                            pygame.mixer.Sound.play(SAMPLE_SFX)

                elif event.key == pygame.K_p:
                    pause = True
                    while pause:
                        pause_game()
                        pygame.mixer.music.pause()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = False
                    pygame.mixer.music.unpause()
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
            # if line_clear>0:
            #     last_k=
            total_line += line_clear
        score += SCORE_CLEAR_LINE_LOOKUP[line_clear] * (level + 1)
        draw_game(grid, level, next_piece, score, screen, total_line)
        pygame.display.flip()
        if check_lost(locked_pos):
            run_game = False
    game_over()


class Menu:
    index = 0
    row = 0
    col = 0
    def __int__(self):
        self.index=0
        self.row=0
        self.col=0
def menu():
    global LEVEL
    screen.blit(LEVEL_IMG, (0, 0))
    pygame.draw.rect(screen,WHITE,pygame.Rect(172+(menu_manage.col*60),242+(menu_manage.row*50),50,40))
    screen.blit(LEVEL_SPRITE[LEVEL],(172+(menu_manage.col*60),242+(menu_manage.row*50)))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                menu_manage.row -=1
                LEVEL-=5
                if menu_manage.row < 0:
                    menu_manage.row += 1
                    LEVEL += 5
            elif event.key == pygame.K_DOWN:
                menu_manage.row += 1
                LEVEL+=5
                if menu_manage.row > 1:
                    menu_manage.row -= 1
                    LEVEL -= 5
            elif event.key == pygame.K_LEFT:
                menu_manage.col -=1
                LEVEL-=1
                if menu_manage.col<0:
                    menu_manage.col+=1
                    LEVEL+=1
            elif event.key == pygame.K_RIGHT:
                menu_manage.col += 1
                LEVEL += 1
                if menu_manage.col > 4:
                    menu_manage.col -= 1
                    LEVEL-=1
            elif event.key == pygame.K_RETURN:
                run_game(LEVEL)

def draw_game(grid, level, next_piece, score, screen, total_line):
    draw_next_shape(screen, next_piece)
    UI(total_line, level, score)
    draw_play_screen(screen, grid)
    draw_statistic(STATISTICS)


screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))
screen.fill(WHITE)
title = pygame.display.set_caption("Tetris")
icon = pygame.image.load("images/Tetris.png")
pygame.display.set_icon(icon)
menu_manage = Menu()
if __name__ == "__main__":
    while 1:
        screen.blit(START_SCREEB_IMG, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                while 1:
                    menu()


        pygame.display.flip()
