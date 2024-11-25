# game setup
import pygame

WIDTH    = 1280
HEIGHT   = 720
FPS      = 60
TILESIZE = 128

SPEED = 5
DIFFICULTY = 'medium'  # 'easy', 'medium', or 'hard'
# Key bindings
MOVE_UP = pygame.K_UP
MOVE_DOWN = pygame.K_DOWN
MOVE_LEFT = pygame.K_LEFT
MOVE_RIGHT = pygame.K_RIGHT
ATTACK = pygame.K_SPACE
SPRINT = pygame.K_LSHIFT

MOVE_UP1 = pygame.K_w
MOVE_DOWN1 = pygame.K_s
MOVE_LEFT1 = pygame.K_a
MOVE_RIGHT1 = pygame.K_d
ATTACK1 = pygame.K_SPACE
SPRINT1 = pygame.K_LSHIFT

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (170, 170, 170)
VIOLET = (86, 55, 103)
PURPLE = (54, 13, 45)

TEXT_COLOR = (255, 255, 255)  # Default text color
TEXT_COLOR_SELECTED = (0, 255, 0)  # Color for the first selected number
TEXT_COLOR_SECOND_SELECTED = (0, 255, 200)  # Color for the second selected number

# Outras configurações
UI_FONT = '../graphics/font/Daydream.ttf' # ou defina um caminho para a sua fonte personalizada

UI_FONT_SIZE = 24  # Tamanho padrão
UI_FONT_SIZE_MENU = 48  # Tamanho maior para o menu
