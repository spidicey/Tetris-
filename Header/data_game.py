from Header.color import PURPLE, ORANGE, BLUE, RED, LIGHTRED, YELLOW, GREEN, WHITE, BLACK
from Header.tetrominos import S, Z, J, L, I, O, T
from Header.coordinate import PIXEL, LEVEL_SELECT_WIDTH, LEVEL_SELECT_HEIGHT
import pygame
# Data tile
SPRITES = [pygame.transform.scale(pygame.image.load(f'Images/T_{i}.png'), (PIXEL, PIXEL)) for i in range(9)]
# for i in range(9):
    # SPRITES.append(pygame.transform.scale(pygame.image.load(f'Images/T_{i}.png'), (PIXEL, PIXEL)))
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
LEVEL_SPRITE=[pygame.transform.scale(pygame.image.load(f'Images/level_{i}.png'), (LEVEL_SELECT_WIDTH, LEVEL_SELECT_HEIGHT)) for i in range(10)]
