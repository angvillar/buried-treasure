import sys, os, pygame, math
from pygame.locals import *

# set up pygame
pygame.init()

# set up screen data
SCREEN_TITLE = "Buried treasure"

SCREEN_WIDTH = 1024;
SCREEN_WIDTH_HALF = SCREEN_WIDTH / 2;

SCREEN_HEIGHT = 768;
SCREEN_HEIGHT_HALF = SCREEN_HEIGHT / 2;

# set up the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption(SCREEN_TITLE)

# set up the clock
Clock = pygame.time.Clock()

# set up the colors
COLOR_BLACK = (000, 000, 000)
COLOR_WHITE = (255, 255, 255)
COLOR_RED   = (255, 000, 000)
COLOR_GREEN = (000, 255, 000)
COLOR_BLUE  = (000, 000, 255)
COLOR_BROWN = (222, 184, 135)

# set up tile map
TILE_MAP_POS_CENTER = pygame.math.Vector2(SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF)
TILE_SIZE = 32
COLS_NUM = 32
ROWS_NUM = 24

# set up assets base dir
ASSETS_BASE_DIR = 'assets/dst/'

class Player(object):

    def __init__(self, x = 0, y = 0):
        self.__surface = pygame.image.load(os.path.join(ASSETS_BASE_DIR, 'player.png')).convert_alpha()
        self.__rect = self.__surface.get_rect()
        self.x = x
        self.y = y
        self.__rotation_angle = 0
        self.__surface_rotated = pygame.transform.rotate(self.__surface, self.__rotation_angle)

    def move(self):
        x = self.x - self.__rect.w / 2
        y = self.y - self.__rect.h / 2
        self.__rect.move_ip(x, y)
        # self.points.append((x, y))

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_w:
                self.__rotation_angle += 15
            if event.key == pygame.K_s:
                self.__rotation_angle -= 15
            if event.key == pygame.K_SPACE:
                angle = math.radians(self.__rotation_angle)
                direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)).normalize()
                self.x += direction.x * 10
                self.y += direction.y * 10

    def update(self):
        self.__surface_rotated = pygame.transform.rotate(self.__surface, -self.__rotation_angle -90)
        self.__rect = self.__surface_rotated.get_rect()
        self.move()

    def draw(self):
        # draw path
        # pygame.draw.lines(screen, COLOR_RED, False, self.points, 5)
        # draw image
        screen.blit(self.__surface_rotated, self.__rect)

    def draw_rect_bounding(self):
        min_x = self.__rect.x
        min_y = self.__rect.y
        max_x = min_x + self.__rect.w
        max_y = min_y + self.__rect.h

        pygame.draw.lines(screen, COLOR_RED, True, [
          (min_x, min_y),
          (max_x, min_y),
          (max_x, max_y),
          (min_x, max_y)
        ])

# set up the player
player_surface = pygame.image.load(os.path.join(ASSETS_BASE_DIR, 'player.png')).convert_alpha()
player_rect = player_surface.get_rect()
player_rect.move_ip(200, 300)
player_dir = pygame.math.Vector2(player_rect.x, player_rect.y)

# set up target position where player should look at at beginning
target_pos = pygame.math.Vector2(SCREEN_WIDTH_HALF, SCREEN_HEIGHT_HALF)

# work the angle
angle = math.atan2(target_pos.y - player_rect.centery, target_pos.x - player_rect.centerx)
angle = math.degrees(angle)

rotated_surface = pygame.transform.rotate(player_surface, -angle - 90)

player = Player(600, 300)

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player.handle_input(event)

        player.update()

        screen.fill(COLOR_BROWN)
        player.draw()
        player.draw_rect_bounding()

        pygame.display.update()

        Clock.tick(60)
