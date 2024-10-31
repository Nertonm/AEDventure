import pygame
from settings import *

class Hanoi:
    steps = 0
    n_disks = 3
    disks = []
    towers_midx = [120, 320, 520]
    pointing_at = 0
    floating = False
    floater = 0

    def make_text(screen, text, font=None, font_name = None, size = None, color=(255,0,0)):
        if font is None:
            font = pygame.font.Font(font_name, size)
        font_surface  = font.render(text, True, color)
        font_rect = font_surface.get_rect()

    def draw_towers():
        global screen
        for xpos in range(40, 460 + 1, 200):
            pygame.draw.rect(screen, green, pygame.Rect(xpos, 400, 160, 20))
            pygame.draw.rect(screen, grey, pygame.Rect(xpos + 75, 200, 10, 200))
        blit_text(screen, 'Start', (towers_midx[0], 403), font_name='mono', size=14, color=black)
        blit_text(screen, 'Finish', (towers_midx[2], 403), font_name='mono', size=14, color=black)

    def display(self):
        # Exibe o desafio de ordenação na tela
        if not self.is_active:
            return

        self.input()

        # Desenha o fundo semi-transparente
        surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 150))
        self.display_surface.blit(surface, (0, 0))

        # Desenha os elementos do array
        total_width = len(self.array) * 100
        start_x = (self.display_surface.get_width() - total_width) // 2

        for index, value in enumerate(self.array):
            color = TEXT_COLOR_SELECTED if index == self.selection_index and not self.button_selected else TEXT_COLOR
            value_surf = self.font.render(str(value), True, color)
            value_rect = value_surf.get_rect(
                center=(start_x + index * 100 + 50, self.display_surface.get_height() // 2))
            self.display_surface.blit(value_surf, value_rect)

        # Desenha o botão de fechar
        button_color = (0, 255, 0) if self.button_hovered or self.button_selected else (255, 0, 0)
        pygame.draw.rect(self.display_surface, button_color, self.button_rect)
        button_text = self.font.render("Close", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        self.display_surface.blit(button_text, button_text_rect)

        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Torres de Hanoi')
    clock = pygame.time.Clock()
    hanoi = Hanoi()
    hanoi.run()
    pygame.quit()
    quit()