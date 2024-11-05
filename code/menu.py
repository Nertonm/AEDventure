import pygame
from settings import *

class Menu:
    def __init__(self, level):
        # Setup inicial
        self.level = level  # Referência à instância de Level
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE_MENU)  # Usar fonte maior para o menu
        self.options = ["Resume", "Config", "Quit"]
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
        elif self.options[self.selection_index] == "Config":
            # Implementar lógica para abrir configuração
            pass
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