from header.color import PURPLE, ORANGE, BLUE, RED, LIGHTRED, YELLOW, GREEN, WHITE, BLACK
from header.tetrominos import S, Z, J, L, I, O, T
from header.coordinate import PIXEL
import pygame
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
