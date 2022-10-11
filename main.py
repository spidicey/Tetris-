import random

import pygame, sys
import pygame.color
from dataclasses import dataclass

pygame.init()

# Tetromino

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']
     ]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Global variable

score = 0
level = 1
s_width = 720
s_height = 700
col = 10
x_ps, y_ps, ps_width, ps_height = 200, 100, 280, 560  # play screen width, height
x_line, y_line, line_width, line_height = 200, 30, 280, 50
x_score, y_score, score_width, score_height = 500, 30, 130, 130
x_lv, y_lv, lv_width, lv_height = 500, 200, 100, 20

white, black = (255, 255, 255), (0, 0, 0)

tetrominos = [S, Z, I, O, J, L, T]
tetrominos_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
pixel = ps_width // col
tide = []
for i in range(8):
    tide.append(pygame.transform.scale(pygame.image.load(f'images/T_{i}.gif'), (pixel, pixel)))


class tetromino():
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, tetromnino):
        self.x = column
        self.y = row
        self.tetromino = tetromino
        self.color = tetrominos_colors[tetrominos.index(tetromnino)]
        self.rotation = 0  # number from 0-3


def UI():
    pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(x_ps, y_ps, ps_width, ps_height), width=3)
    ui_lines()
    ui_score()
    ui_level()


def ui_lines(Lines=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_line, y_line, line_width, line_height), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Lines {level:03d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (x_line + x_line + line_width) // 2 - textsurface.get_width() // 2, y_line + 3))


def ui_level(level=1):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_lv, y_lv, lv_width, lv_height), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (x_lv + x_lv + lv_width) // 2 - textsurface.get_width() // 2, y_lv + 3))


def ui_score(score=0):
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_score, y_score, score_width, score_height),
                     width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Score: {score:06d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (x_score + x_score + score_width) // 2 - textsurface.get_width() // 2, y_score + 2 * score_height // 3))


def createGrid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def get_teromino():
    random.choices(tetrominos)


def draw_grid(surface, col, row):
    for i in range(1, col):
        pygame.draw.line(surface, white, (x_ps + i * pixel, y_ps), (x_ps + i * pixel, y_ps + ps_height-4),width=1)
        for j in range(1, row):
            pygame.draw.line(surface, white, (x_ps, y_ps + j * pixel), (x_ps + ps_width-4, y_ps + j * pixel),width=1)


def flash():
    for _ in range(5):
        screen.fill(black)
        pygame.display.flip()
        pygame.time.wait(10)
        screen.fill(white)
        pygame.display.flip()
        pygame.time.wait(10)
    pygame.time.wait(2000)
    UI()
    pygame.time.wait(2000)


if __name__ == "__main__":
    screen = pygame.display.set_mode((s_width, s_height))
    title = pygame.display.set_caption("Tetris")
    icon = pygame.image.load("images/Tetris.png")
    pygame.display.set_icon(icon)
    bg = pygame.transform.scale(pygame.image.load("images/start.gif"), (s_height, s_width))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        screen.fill(black)
        # screen.blit(bg,(0,0))
        draw_grid(screen,10,20)
        UI()
        # flash()
        pygame.display.flip()
