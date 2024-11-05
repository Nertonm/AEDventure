import pygame
from settings import *
class OpeningScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.start_button = pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 2 - 50), (200, 100))
        self.exit_button = pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 2 + 60), (200, 100))

    def display(self):
        self.screen.fill((0, 0, 0))
        title_surf = self.font.render("AEDventure", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(title_surf, title_rect)

        #pygame.draw.rect(self.screen, (0, 255, 0), self.start_button)
        start_surf = self.font.render("Start", True, TEXT_COLOR)
        start_rect = start_surf.get_rect(center=self.start_button.center)
        self.screen.blit(start_surf, start_rect)

        exit_surf = self.font.render("Exit", True, TEXT_COLOR)
        exit_rect = exit_surf.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_surf, exit_rect)

        pygame.display.flip()

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                return "start"
            elif self.exit_button.collidepoint(event.pos):
                return "exit"
        return None