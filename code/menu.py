import pygame
from settings import *

class Menu:
    def __init__(self, level):
        # Setup inicial
        self.level = level  # Referência à instância de Level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)  # Usar fonte maior para o menu
        self.options = ["Resume", "Quit"]
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True
        self.background_color = (0, 0, 0, 150)  # Preto com transparência (RGBA)
        self.option_rects = []  # Lista para armazenar os retângulos das opções

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < len(self.options) - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_RETURN]:
                self.select_option()

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 200:
                self.can_move = True

    def select_option(self):
        if self.options[self.selection_index] == "Resume":
            self.level.toggle_menu()  # Chama o método para alternar a pausa
        # elif self.options[self.selection_index] == "Config":
        #     # Implementar lógica para abrir configuração
        #     pass
        elif self.options[self.selection_index] == "Quit":
            pygame.quit()
            exit()

    def check_mouse_hover(self):
        mouse_pos = pygame.mouse.get_pos()
        for index, option_rect in enumerate(self.option_rects):
            if option_rect.collidepoint(mouse_pos):
                self.selection_index = index

    def check_mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, option_rect in enumerate(self.option_rects):
                if option_rect.collidepoint(event.pos):
                    self.selection_index = index
                    self.select_option()

    def display(self):
        self.input()
        self.selection_cooldown()
        self.check_mouse_hover()

        # Desenhar um fundo escuro e transparente
        surface = pygame.Surface(self.display_surface.get_size(), pygame.SRCALPHA)  # Cria uma superfície com suporte a alpha
        surface.fill(self.background_color)  # Preenche com a cor de fundo
        self.display_surface.blit(surface, (0, 0))  # Desenha o fundo na tela

        self.option_rects = []  # Limpa a lista de retângulos das opções

        for index, option in enumerate(self.options):
            # Definindo cor com base na seleção
            color = TEXT_COLOR_SELECTED if index == self.selection_index else TEXT_COLOR
            option_surf = self.font.render(option, True, color)
            # Ajuste de centralização e espaçamento vertical
            option_rect = option_surf.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() // 2 - (len(self.options) * 30 // 2) + index * 80))
            self.display_surface.blit(option_surf, option_rect)
            self.option_rects.append(option_rect)  # Adiciona o retângulo da opção à lista


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
        self.selected_difficulty = 'easy'
        self.show_difficulty_selection = False
        self.selected_button = 'start'

    def display(self):
        self.screen.fill(BLACK)
        background = pygame.image.load('../graphics/background/background.png')
        self.screen.blit(background, (0,0))
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