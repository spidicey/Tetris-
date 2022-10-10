import pygame, sys
import pygame.color

# Global variable

score = 0
level = 1
pygame.init()
s_width = 720
s_height = 700
col = 10
x_ps, y_ps, ps_width, ps_height = 200, 100, 280, 560  # play screen width, height
x_line, y_line, line_width, line_height = 200, 30, 280, 50
x_score, y_score, score_width, score_height = 500, 30, 130, 130
x_lv, y_lv, lv_width, lv_height = 500, 200, 100, 20
pixel = ps_width // col
tide = []
for i in range(8):
    tide.append(pygame.transform.scale(pygame.image.load(f'images/T_{i}.gif'), (pixel, pixel)))


def UI():
    pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(x_ps, y_ps, ps_width, ps_height), width=3)
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_line, y_line, line_width, line_height), width=3)
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_score, y_score, score_width, score_height),
                     width=3)
    pygame.draw.rect(screen, pygame.Color("Green"), pygame.Rect(x_lv, y_lv, lv_width, lv_height), width=3)
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Score: {score:06d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (x_score + x_score + score_width) // 2 - textsurface.get_width() // 2, y_score + 2 * score_height // 3))
    textsurface = pygame.font.SysFont('consolas', 17).render(f'Level {level:02d}', False, (255, 255, 255))
    screen.blit(textsurface, (
        (x_lv + x_lv + lv_width) // 2 - textsurface.get_width() // 2, y_lv + 3))


def createGrid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]


if __name__ == "__main__":
    screen = pygame.display.set_mode((s_width, s_height))
    title = pygame.display.set_caption("Tetris")
    icon = pygame.image.load("images/Tetris.png")
    pygame.display.set_icon(icon)
    bg = pygame.transform.scale(pygame.image.load("images/start.gif"), (s_height, s_width))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        screen.fill((0, 0, 0))
        # screen.blit(bg,(0,0))
        UI()
        pygame.display.flip()
