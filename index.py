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
        self.__rotation_angle = -90
        self.__surface_rotated = pygame.transform.rotate(self.__surface, self.__rotation_angle)

    def __set_dir(self):
        angle = math.radians(self.__rotation_angle + 90)
        self.__dir = pygame.math.Vector2(math.cos(angle), math.sin(angle))

    def move(self):
        self.__rect.move_ip(self.x - self.__rect.w / 2, self.y - self.__rect.h / 2)

    def handle_input(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_w:
                self.__rotation_angle += 15

    def update(self):
        self.__surface_rotated = pygame.transform.rotate(self.__surface, self.__rotation_angle)
        self.__rect = self.__surface_rotated.get_rect()
        self.move()

    def draw(self):
        screen.blit(self.__surface_rotated, self.__rect)

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

player = Player(100, 100)

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            player.handle_input(event)

        player.update()

        screen.fill(COLOR_BROWN)
        # screen.blit(rotated_surface, player_rect)
        player.draw()

        pygame.display.update()

        Clock.tick(60)
