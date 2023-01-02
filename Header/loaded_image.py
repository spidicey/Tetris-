import pygame
from Header.coordinate import S_WIDTH, S_HEIGHT, NEXT_WIDTH, NEXT_HEIGHT, PS_HEIGHT, SCORE_WIDTH, SCORE_HEIGHT, \
    LINE_WIDTH, LINE_HEIGHT, STA_WIDTH, STA_HEIGHT,HOLD_WIDTH,HOLD_HEIGHT
# BackGround
# Next piece
# Play screen
# Score
# Line
# Statistics
START_SCREEB_IMG = pygame.transform.scale(pygame.image.load(f'Images/start.gif'), (S_WIDTH, S_HEIGHT))
NEXT_PIECE_IMG = pygame.transform.scale(pygame.image.load(f'Images/next_piece.png'), (NEXT_WIDTH, NEXT_HEIGHT))
PLAY_SCEEN_IMG = pygame.transform.scale(pygame.image.load(f'Images/play_screen.png'), (30, PS_HEIGHT + 4))
SCORE_IMG = pygame.transform.scale(pygame.image.load(f'Images/score.png'), (SCORE_WIDTH, SCORE_HEIGHT))
LINE_IMG = pygame.transform.scale(pygame.image.load('Images/line.png'), (LINE_WIDTH, LINE_HEIGHT))
STATISTICS_IMG = pygame.transform.scale(pygame.image.load('Images/play_screen_1.png'), (STA_WIDTH, STA_HEIGHT))
LEVEL_IMG = pygame.transform.scale(pygame.image.load('Images/level-1.png'), (S_WIDTH, S_HEIGHT))
