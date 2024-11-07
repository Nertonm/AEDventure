import pygame
from settings import *

class OpeningScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)
        self.start_button = pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 2 - 50), (200, 100))
        self.exit_button = pygame.Rect((screen.get_width() // 2 - 100, screen.get_height() // 2 + 60), (200, 100))

        self.difficulty_buttons = {
            'easy': pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 120, 320, 70),
            'medium': pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 - 40, 320, 70),
            'hard': pygame.Rect(screen.get_width() // 2 - 150, screen.get_height() // 2 + 40, 320, 70)
        }
        self.selected_difficulty = 'hard'
        self.show_difficulty_selection = False
        self.selected_button = 'start'

    def display(self):
        self.screen.fill(BLACK)
        title_surf = self.font.render("AEDventure", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 4))
        self.screen.blit(title_surf, title_rect)

        if self.show_difficulty_selection:
            for difficulty, rect in self.difficulty_buttons.items():
                color = TEXT_COLOR_SELECTED if difficulty == self.selected_difficulty else WHITE
                pygame.draw.rect(self.screen, color, rect)
                text_surf = self.font.render(difficulty.capitalize(), True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                self.screen.blit(text_surf, text_rect)
        else:
            start_color = TEXT_COLOR_SELECTED if self.selected_button == 'start' else TEXT_COLOR
            start_surf = self.font.render("Start", True, start_color)
            start_rect = start_surf.get_rect(center=self.start_button.center)
            self.screen.blit(start_surf, start_rect)

            exit_color = TEXT_COLOR_SELECTED if self.selected_button == 'exit' else TEXT_COLOR
            exit_surf = self.font.render("Exit", True, exit_color)
            exit_rect = exit_surf.get_rect(center=self.exit_button.center)
            self.screen.blit(exit_surf, exit_rect)

        pygame.display.flip()

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.show_difficulty_selection:
                for difficulty, rect in self.difficulty_buttons.items():
                    if rect.collidepoint(event.pos):
                        self.selected_difficulty = difficulty
                        return "start_game"
            else:
                if self.start_button.collidepoint(event.pos):
                    self.show_difficulty_selection = True
                elif self.exit_button.collidepoint(event.pos):
                    return "exit"
        return None

    def check_key(self, event):
        if event.type == pygame.KEYDOWN:
            if self.show_difficulty_selection:
                if event.key in (MOVE_UP, MOVE_UP1, pygame.K_w):
                    self.selected_difficulty = 'easy' if self.selected_difficulty == 'medium' else 'medium' if self.selected_difficulty == 'hard' else 'hard'
                elif event.key in (MOVE_DOWN, MOVE_DOWN1, pygame.K_s):
                    self.selected_difficulty = 'hard' if self.selected_difficulty == 'medium' else 'medium' if self.selected_difficulty == 'easy' else 'easy'
                elif event.key == pygame.K_RETURN:
                    return "start_game"
            else:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                    self.selected_button = 'start' if self.selected_button == 'exit' else 'exit'
                elif event.key == pygame.K_RETURN:
                    if self.selected_button == 'start':
                        self.show_difficulty_selection = True
                    elif self.selected_button == 'exit':
                        return "exit"
        return None